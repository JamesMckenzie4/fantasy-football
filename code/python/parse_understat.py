import asyncio
import json

import aiohttp
from pprint import pprint

from understat import Understat


async def main():
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        data = await understat.get_league_results(league_name='epl', season='2018')
        return data


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(main())
    print(results)
