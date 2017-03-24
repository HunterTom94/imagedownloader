from downloaders.image_downloader import ImageDownloader, Image
import logging
import re
import urllib.request

logger = logging.getLogger("deviantart_image_downloader")


class DeviantArtImageDownloader(ImageDownloader):
    url_pattern = re.compile(r'data-super-full-img=([^\ ]+)')

    def get_image_urls_from_source(self, query, offset, count):
        url = ('http://deviantart.com/browse/all/digitalart/?order=9&q={}&offset={}'
               .format(query, offset))

        try:
            data = None
            with urllib.request.urlopen(url) as openurl:
                data = openurl.read().decode('utf-8')

            if data is None:
                raise Exception("Bad data!")

            images = DeviantArtImageDownloader.url_pattern.findall(data)
            return [Image(image[1:-1]) for image in images]

        except Exception as e:
            logger.debug("DeviantArtImageDownloader Error: {} -- Retrying.."
                         .format(e))
            return self.get_image_urls_from_source(query, offset, count)
