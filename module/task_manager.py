import asyncio
from cart_product import __atc__


async def runner(url):
    await asyncio.sleep(0.2)
    __atc__(url)

async def main(url):
    num_runs = 1
    await asyncio.gather(*[runner(url) for _ in range(num_runs)])


# Lancer le programme principal
asyncio.run(main('https://eu.supreme.com/products/bghi5vlnt-x1qbx_'))