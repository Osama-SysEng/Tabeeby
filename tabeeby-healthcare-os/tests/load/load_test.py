import asyncio
import aiohttp
import time

async def make_request(session, url):
    async with session.get(url) as response:
        return response.status

async def load_test():
    url = "http://localhost:8000/health"
    concurrent = 1000
    total = 10000

    async with aiohttp.ClientSession() as session:
        start = time.time()
        tasks = [make_request(session, url) for _ in range(total)]
        results = await asyncio.gather(*tasks)
        elapsed = time.time() - start

        success = sum(1 for r in results if r == 200)
        print(f"Requests: {total}")
        print(f"Success: {success}")
        print(f"Time: {elapsed:.2f}s")
        print(f"RPS: {total/elapsed:.0f}")

if __name__ == "__main__":
    asyncio.run(load_test())
