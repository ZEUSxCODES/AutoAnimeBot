import asyncio
from torrentp import TorrentDownloader

def download_magnet(link: str, path: str):
    async def download():
        torrent_file = TorrentDownloader(link, path)
        await torrent_file.start_download()

    asyncio.run(download())
