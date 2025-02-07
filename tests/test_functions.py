import asyncio
import os
from dotenv import load_dotenv
from app.search import search_web
from app.parser import parse_content
from app.main import generate_with_ollama
import httpx

load_dotenv()

async def test_search_web():
    try:
        query = "What is FastAPI?"
        results = await search_web(query)
        print(f"Search results for '{query}': {results}")
        if results:
            print("Search web test passed!")
        else:
            print("Search web test failed: No results returned.")
    except Exception as e:
        print(f"Search web test failed: {e}")

async def test_parse_content():
    try:
        async with httpx.AsyncClient() as client:
            url = "https://google.serper.dev/search"
            result = await parse_content(client, url)
            print(f"Parsed content from {url}: {result}")
            if result.get("content"):
                print("Parse content test passed!")
            else:
                print("Parse content test failed: No content parsed.")
    except Exception as e:
        print(f"Parse content test failed: {e}")

async def test_generate_with_ollama():
    try:
        query = "What is FastAPI?"
        context = [{"url": "https://google.serper.dev/search", "content": "FastAPI is a modern web framework."}]
        response = await generate_with_ollama(query, context)
        print(f"Response from ollama for query '{query}': {response}")
        if response:
            print("Generate with ollama test passed!")
        else:
            print("Generate with ollama test failed: No response returned.")
    except Exception as e:
        print(f"Generate with ollama test failed: {e}")

async def main():
    await test_search_web()
    await test_parse_content()
    await test_generate_with_ollama()

if __name__ == "__main__":
    asyncio.run(main())
