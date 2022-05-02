import asyncio

import aiohttp


async def proxy_get_photo(url, proxy):
    async with aiohttp.ClientSession() as session:
        proxy = f"http://{proxy}"
        async with session.get(url, proxy=proxy) as res:
            content = await res.text()
            print(content)

if __name__ == '__main__':
    asyncio.run(proxy_get_photo("https://2ip.ru/", "45.92.169.34:8000"))
