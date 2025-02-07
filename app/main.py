from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import httpx
import os
from dotenv import load_dotenv
from app.search import search_web
from app.parser import parse_content
from app.cache import CacheManager
from pydantic import BaseModel
import logging
import asyncio
import traceback
import json

load_dotenv()

# Set up logging to log errors to the console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatQuery(BaseModel):
    query: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    global cache
    cache = CacheManager(os.getenv("REDIS_URL"))
    yield
    await cache.close()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat_endpoint(chat_query: ChatQuery):
    try:
        query = chat_query.query  # Access the query from the model
        logger.info(f"Received query: {query}")
        # Check cache
        if cached := await cache.get(query):
            logger.info(f"Cache hit for query: {query}")
            return {"response": cached}

        # Execute search
        search_results = await search_web(query)
        context = await process_results(search_results)

        # Call local model
        response = await generate_with_ollama(query, context)
        if response:
            await cache.set(query, response)  # Cache result
            logger.info(f"Query processed successfully: {query}")
        return {"response": response}

    except Exception as e:
        logger.error(f"Error processing query: {query}, Error: {e}")
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

async def process_results(results):
    # Set the timeout to 30 seconds, can adjust based on actual needs
    timeout = httpx.Timeout(30.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        tasks = [parse_content(client, url) for url in results[:3]]  # Get the top 3 results
        return await asyncio.gather(*tasks)

async def generate_with_ollama(query, context):
    messages = [
        {
            "role": "user",
            "content": f"""
Answer the question based on the following context information:
{context}

Question: {query}
Please provide a detailed answer in English and indicate the source of the reference.
"""
        }
    ]
    # Set the timeout to 60 seconds, can adjust based on actual needs
    timeout = httpx.Timeout(60.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            request_body = {
                "model": "deepseek-r1:32b",
                "messages": messages
            }
            # Validate the request body
            if "model" not in request_body or not isinstance(request_body["model"], str):
                raise ValueError("Invalid or missing 'model' field in request body")
            if "messages" not in request_body or not isinstance(request_body["messages"], list) or not request_body["messages"]:
                raise ValueError("Invalid or missing 'messages' field in request body")
            for message in request_body["messages"]:
                if "role" not in message or "content" not in message or not isinstance(message["role"], str) or not isinstance(message["content"], str):
                    raise ValueError("Invalid 'message' structure in request body")
            
            logger.info(f"Request body: {request_body}")
            response = await client.post(
                "http://localhost:11434/api/chat",
                json=request_body
            )
            logger.info(f"Response status code: {response.status_code}")
            logger.info(f"Response headers: {response.headers}")
            logger.info(f"Response text: {response.text}")
            response.raise_for_status()  # Check response status code

            # Handle streaming response
            full_response = ""
            for line in response.text.strip().split('\n'):
                if line:
                    try:
                        data = json.loads(line)  # Use json.loads instead of eval
                        if 'message' not in data:
                            raise KeyError("'message' key not found in response data")
                        message = data['message']
                        if message is None or 'content' not in message or message['content'] is None:
                            raise ValueError("Invalid 'message' structure in response data")
                        full_response += message['content']
                    except json.JSONDecodeError as je:
                        logger.error(f"JSON decoding error in response line: {line}, Error: {je}")
                        logger.error(traceback.format_exc())  # Output full error stack trace
                    except KeyError as ke:
                        logger.error(f"Key error in response line: {line}, Error: {ke}")
                        logger.error(traceback.format_exc())
                    except ValueError as ve:
                        logger.error(f"Value error in response line: {line}, Error: {ve}")
                        logger.error(traceback.format_exc())
                    except Exception as e:
                        logger.error(f"Error parsing response line: {line}, Error: {e}")
                        logger.error(traceback.format_exc())

            return full_response
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP status error: {e}")
            logger.error(traceback.format_exc())
        except ValueError as ve:
            logger.error(f"Request body validation error: {ve}")
            logger.error(traceback.format_exc())
        except KeyError as ke:
            logger.error(f"Response JSON does not contain expected keys: {ke}")
            logger.error(traceback.format_exc())
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            logger.error(traceback.format_exc())
        return None
