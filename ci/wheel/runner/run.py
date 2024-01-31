import asyncio

from service import check_new_task


async def main():
    while True:
        check_new_task()
        await asyncio.sleep(1)


# runner should run in root directory
if __name__ == "__main__":
    asyncio.run(main())
