import asyncio

from service import check_new_task


async def main():
    while True:
        check_new_task()
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
