import requests
import asyncio
from functools import lru_cache

URL_FILE = "cornjob/.env"
SLEEP = 5


@lru_cache()
def get_url_list():
    with open(URL_FILE) as f:
        return f.read().splitlines()


async def main():
    while True:
        for url in get_url_list():
            result = requests.get(url)
            print(f"GET {url} {result.status_code}")
        await asyncio.sleep(SLEEP)


if __name__ == "__main__":
    asyncio.run(main())
