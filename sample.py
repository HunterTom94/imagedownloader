from deviantart_image_downloader import DeviantArtImageDownloader

"""
sample.py

Uses DeviantArt to find images relating to cars, cats, lamps, and houses. The
script attempts to download a maximum of 10,000 images per query (10,000 cars,
10,000 cats, 10,000 lamps, and 10,000 houses).

All images are saved into the `pictures` directory and duplicates are not saved

The script runs on 8 threads
"""


def main():
    pool_size = 8  # How many threads to use
    queries = ["cars", "cats", "lamps", "houses"]  # Which keywords to search
    download_per_query = 10000  # How many of each keyword should be downloaded
    directory = "pictures"  # The directory to download into

    # Create the DeviantArtImageDownloader
    downloader = DeviantArtImageDownloader(
        directory, pool_size, queries, download_per_query
    )

    # Load the directory. This involves creating the directory if it does not
    # exist, scanning all files in the directory, and removing any duplicates
    # that already exist in the directory.
    downloader.load_directory()

    # Begin gathering image URLs and start the download process.
    downloader.gather_urls()

    # Block the current thread until all images or downloaded or no new unique
    # images are available.
    downloader.wait_for_downloads_to_complete()


if __name__ == '__main__':
    main()
