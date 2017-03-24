from deviantart_image_downloader import DeviantArtImageDownloader


def main():
    pool_size = 8
    queries = ["cars", "cats", "lamps", "houses"]
    download_per_query = 10000
    directory = "pictures"

    downloader = DeviantArtImageDownloader(
        directory, pool_size, queries, download_per_query
    )

    downloader.load_directory()
    downloader.gather_urls()
    downloader.wait_for_downloads_to_complete()


if __name__ == '__main__':
    main()
