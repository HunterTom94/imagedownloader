imagedownloader
===============
A collection of libraries used to quickly download images from various locations
based on keywords.

imagedownloader was originally created to collect a large number of unique
images for use in machine learning training data. Because of this, the libraries
may be a little "overfitted" for our needs, but maybe they will help you, too!


Some Details
------------
imagedownloader has two pecuilar behaviors that are worth noting.

1. imagedownloader downloads all images as ".jpg" files. This shortcut was out
   of pure laziness. In theory, the extension can be extracted from the URL of
   the image [Tracked in Issue #1](https://github.com/brandonio21/imagedownloader/issues/1)

2. imagedownloader attempts to keep track of the images it has downloaded on a
   past run, and uses the image's URL to do a preliminary duplicate-check. Thus,
   when images are saved, they are saved with a filename of their hashed URL.


Using A Downloader
------------------
To dive right into the code, be sure to look at `sample.py`. Otherwise, here is
a small API reference

The imagedownloader library uses inheritence to organize its various downloaders.
The base functionality is found in `image_downloader.py`, which handles
spawning threads, downloading images, and keeping track of duplicates. 

All subclasses of ImageDownloader should implement `get_image_urls_from_source`,
which takes the query string, the offset integer, and the count integer in order
to return a list of image URLs.


### BingImageDownloader ###
A `BingImageDownloader` instance may be construced using the standard 
`ImageDownloader` semantics with the addition of a 
[Bing Search API key](https://www.microsoft.com/cognitive-services/en-us/bing-image-search-api).


```python
downloader = BingImageDownloader("images", 8, ["cats", "dogs"], 10000, apiKey)
```


### DeviantArtImageDownloader ###
A `DeviantArtImageDownloader` instance may be constructed using the standard
`ImageDownloader` semantics.


```python
downloader = DeviantArtImageDownloade("images", 8, ["cats", "dogs"], 10000)
```
