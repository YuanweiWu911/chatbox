import httpx
from readability import Document
from bs4 import BeautifulSoup

async def parse_content(client: httpx.AsyncClient, url: str):
    try:
        resp = await client.get(url, timeout=10)
        doc = Document(resp.text)
        soup = BeautifulSoup(doc.summary(), "lxml")

        # Remove unnecessary content
        for element in soup(["script", "style", "nav", "footer"]):
            element.decompose()

        return {
            "url": url,
            "content": soup.get_text(separator="\n", strip=True)[:2000]  # Truncate the first 2000 characters
        }
    except Exception:
        return {"url": url, "content": "Failed to retrieve content"}

