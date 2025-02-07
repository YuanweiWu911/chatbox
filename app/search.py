import aiohttp
import asyncio
import os
import logging

logger = logging.getLogger(__name__)

async def search_web(query: str):
    api_key = os.getenv("SERPER_API_KEY")
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    logger.info(f"Using API key: {api_key}")

    proxy_url = os.getenv("PROXY_URL")
    async with aiohttp.ClientSession() as session:
        try:
            if proxy_url:
                async with session.post(
                        "https://google.serper.dev/search",
                        headers=headers,
                        json={"q": query, "num": 10},
                        proxy=proxy_url
                ) as response:
                    response.raise_for_status()
                    data = await response.json()
            else:
                async with session.post(
                        "https://google.serper.dev/search",
                        headers=headers,
                        json={"q": query, "num": 10}
                ) as response:
                    response.raise_for_status()
                    data = await response.json()
            return [result["link"] for result in data.get("organic", [])[:10]]
        except aiohttp.ClientError as e:
            logger.error(f"ClientError {e}")
        except ValueError as e:
            logger.error(f"JSON error: {e}")
        except Exception as e:
            logger.error(f"Unknown error: {e}")
    return []

