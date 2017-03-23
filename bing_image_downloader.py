from image_downloader import ImageDownloader, Image
from util import LockedSet
import http.client
import json
import logging
import urllib.parse

logger = logging.getLogger('bing_image_downloader')


class BingImageDownloader(ImageDownloader):

    def __init__(self, directory, pool_size, queries, max_download_per_query,
                 apikey):
        super(BingImageDownloader, self).__init__(
            directory, pool_size, queries, max_download_per_query
        )

        self.headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': apikey,
        }
        self.imageIds = LockedSet()

    def get_image_urls_from_source(self, query, offset, count):
        unencoded_parameters = {
            # Request parameters
            'q': query,
            'count': count,
            'mkt': 'en-us',
            'safeSearch': 'Moderate',
            'offset': offset
        }

        try:
            conn = http.client.HTTPSConnection('api.cognitive.microsoft.com',
                                               timeout=5)
            params = urllib.parse.urlencode(unencoded_parameters)
            conn.request("GET", "/bing/v5.0/images/search?%s" % params,
                         "{body}", self.headers)
            response = conn.getresponse()
            data = response.read().decode('utf-8')
            parsed_data = json.loads(data)
            conn.close()

            return [Image(value["contentUrl"], value["imageId"])
                    for value in parsed_data["value"]
                    if self.imageIds.insert_if_not_contains(value["imageId"])]
        except KeyError as e:
            logger.debug(parsed_data)
            return self.get_image_urls_from_source(query, offset, count)
        except Exception as e:
            logger.debug(e)
            logger.debug("[Errno {0}] {1} -- Retrying...".format(
                e.errno, e.strerror))
            return self.get_image_urls_from_source(query, offset, count)
