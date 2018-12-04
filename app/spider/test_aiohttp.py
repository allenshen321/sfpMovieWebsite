import aiohttp
import asyncio


async def download():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://httpbin.org/get') as resp:
            print(resp.status)
            print(await resp.text())


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download())
    loop.close()


if __name__ == '__main__':
    main()
