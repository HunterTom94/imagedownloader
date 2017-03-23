import urllib.request
from util import LockedSet
from queue import Queue
from hashlib import sha256
from threading import Thread
import logging
import os

logger = logging.getLogger('image_downloader')


class Image(object):

    def __init__(self, url, identifier=None):
        self.url = url
        self.identifier = identifier if identifier else url


class ImageDownloader(object):

    def __init__(self, directory, pool_size, queries, max_download_per_query):
        self.image_contents_set = LockedSet()
        self.image_names_set = LockedSet()
        self.image_directory = directory

        self.queries = queries
        self.current_query = None
        self.max_download_per_query = max_download_per_query

        self.done = False
        self.download_queue = Queue()
        self.threads = []
        self.pool_size = pool_size

    def get_image_urls_from_source(self, query, offset, count):
        pass

    def gather_urls(self):
        for query in self.queries:
            self.current_query = query
            counted_urls = 0
            stop_count = 0
            while counted_urls < self.max_download_per_query:
                if stop_count > 3:
                    break

                urls = self.get_image_urls_from_source(
                    query, counted_urls, self.max_download_per_query
                )

                if len(urls) == 0:
                    logger.debug("[{}]: No more URLs! (retry={})".format(
                        query, stop_count))
                    stop_count += 1
                else:
                    stop_count = 0

                counted_urls += len(urls)

                for url in urls:
                    self.download_queue.put(url)

                logger.debug("[{}]: Gathered {}/{} URLs".format(
                    query, counted_urls, self.max_download_per_query))

                if len(self.threads) == 0 and self.download_queue.qsize() > 50:
                    self.begin_downloading()

        self.download_queue.join()
        self.done = True

    def load_directory(self):
        if not os.path.isdir(self.image_directory):
            os.makedirs(self.image_directory)

        for path in os.listdir(self.image_directory):
            name, ext = os.path.splitext(path)
            name_hash = name
            image_path = os.path.join(self.image_directory, path)

            with self.image_names_set.lock:
                if name_hash in self.image_names_set.set:
                    os.remove(image_path)
                    continue

                with open(image_path, 'rb') as openImage:
                    image_data_hash = sha256(openImage.read()).digest()
                    if self.image_contents_set.insert_if_not_contains(
                            image_data_hash):
                        self.image_names_set.set.add(name_hash)
                    else:
                        os.remove(image_path)

    def download_files(self):
        while not self.done:
            image = self.download_queue.get()
            try:
                encoded_ident = image.identifier.encode('utf-8')
                hashed_url = sha256(encoded_ident).hexdigest()
                if not self.image_names_set.insert_if_not_contains(hashed_url):
                    self.download_queue.task_done()
                    continue

                data = None
                with urllib.request.urlopen(image.url) as openurl:
                    data = openurl.read()

                if data is None:
                    self.download_queue.task_done()
                    continue

                data_hash = sha256(data).digest()
                if not self.image_contents_set.insert_if_not_contains(data_hash):
                    self.download_queue.task_done()
                    continue

                filename = os.path.join(self.image_directory,
                                        hashed_url + '.jpg')
                with open(filename, 'wb') as image_file:
                    image_file.write(data)
                    self.download_queue.task_done()

            except Exception as e:
                self.download_queue.task_done()
                continue

    def begin_downloading(self):
        for i in range(self.pool_size):
            t = Thread(target=self.download_files)
            t.daemon = True
            t.start()
            self.threads.append(t)

    def wait_for_downloads_to_complete(self):
        for t in self.threads:
            t.join()
