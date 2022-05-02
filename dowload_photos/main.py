import asyncio
import collections
import imghdr
import io
import sys
from pathlib import Path

import aiofiles
import aiohttp
from loguru import logger

from dowload_photos.config import db
from dowload_photos.db.db import init_tortoise
from dowload_photos.db.models import Users

BASE_DIR = Path(__file__).parent.parent
IMAGE_DIR = BASE_DIR / 'images'
IMAGE_DIR.mkdir(exist_ok=True)
logger.remove()
logger.add(
    sink=sys.stdout,
    level="TRACE",
    enqueue=True,
    diagnose=True,
)
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "cookie": "cf_chl_2=c6170fad80ef4cb; cf_chl_rc_ni=5; cf_chl_prog=x19; cf_clearance=sAlkKtj6nCNeS3yDtDV9mcd4WpCmJgTnnc8FPw9FpDo-1651224731-0-150"
}


async def write(name: str, content: bytes):
    image_file = IMAGE_DIR / name
    try:
        async with aiofiles.open(image_file, "wb") as f:
            await f.write(content)
    except Exception as e:
        logger.warning(e)
        image_file.unlink()


async def false_write(name, url):
    path = Path("fail.txt")
    try:
        async with aiofiles.open(path, "a") as f:
            await f.write(f"{name}: {url}\n")
    except Exception as e:
        logger.warning(e)
        path.unlink()


def write_sync(name: str, content: bytes):
    image_file = IMAGE_DIR / name
    try:
        with open(image_file, "wb") as f:
            f.write(content)
    except Exception as e:
        logger.warning(e)
        image_file.unlink()


async def proxy_get_photo(url, proxy, session):
    proxy = f"http://{proxy}"
    async with session.get(url, proxy=proxy) as res:
        content = await res.read()
        return content


async def get_photo(name: str, url: str, session: aiohttp.ClientSession):
    try:
        # while True:
        async with session.get(url) as res:
            content = await res.read()
            # logger.success(url)
            # im = Image.load(content)
            # await write(name, content)
            if imghdr.what(io.BytesIO(content)):
                await write(name, content)
            else:
                # for pr in ("45.92.169.34:8000", "194.67.200.237:8000",
                #            # "168.80.200.167:8000",
                #            ):
                #     content = await proxy_get_photo(url, pr, session)
                #     if imghdr.what(io.BytesIO(content)):
                #         await write(name, content)
                #         return
                logger.warning(f"{url}")
                await false_write(name, url)
    except Exception as e:
        logger.critical(f"{e}|{url}")


@logger.catch
async def main():
    await init_tortoise(**db.dict())
    users = await Users.all()
    # image_files = IMAGE_DIR.iterdir()
    image_files = list(map(lambda x: x.name, IMAGE_DIR.iterdir()))

    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        count = 0
        proxy_count = collections.defaultdict(int)
        for u in users:
            if u.img_src:
                name = f"{u.qr_code}{Path(u.img_src).suffix}"
                if name not in image_files:
                    # logger.debug(u.img_src)
                    # await get_photo(name, u.img_src, session)
                    # continue
                    count += 1
                    task = asyncio.create_task(get_photo(name, u.img_src, session))
                    tasks.append(task)
                    if count > 10:
                        logger.success(f"Достигнут лимит {count}. Ожидание")
                        count = 0
                        await asyncio.gather(*tasks)
                        tasks = []

        logger.success(f"Завершение")
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
