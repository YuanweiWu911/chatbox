Sure! Below is a **User Manual** for using the FastAPI-based chat application from the command line. This manual explains how to interact with your app, run it, and make requests via `curl` or other tools.

---

# **ChatBox FastAPI User Manual**

## **Introduction**
The ChatBox FastAPI application allows you to interact with a chatbot that fetches information from the web and generates responses using a local AI model. The application leverages Redis for caching, which helps improve performance by storing previous responses.

This manual provides instructions on how to run the application and interact with it using the command line.

---

## **1. Prerequisites**

Before using the ChatBox app, ensure the following:

- **Redis** is installed and running.
- **Python 3.10+** is installed.
- Dependencies are installed from `requirements.txt`.

### **Installing Redis**
To install Redis on your system:

- **Ubuntu/Debian**:
  ```bash
  sudo apt update
  sudo apt install redis-server
  ```

- **macOS**:
  ```bash
  brew install redis
  ```

### **Setting Up the Environment**

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your environment**:
   - Create a `.env` file in the root of your project if it doesn't exist, and set your Redis URL and other environment variables:
   
   ```env
   REDIS_URL=redis://localhost:6379
   SERPER_API_KEY=your_serper_api_key
   ```

---

## **2. Running the Application**

### **Start the FastAPI Application**
1. **Run the app with Uvicorn**:

   Open a terminal and run the following command to start the application:
   
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

   This starts the FastAPI server at `http://localhost:8000`. The `--reload` flag allows the server to auto-reload on code changes.

2. **Verify that the application is running**:
   
   Open your browser and navigate to `http://localhost:8000/docs`. This will open the **Swagger UI** documentation, where you can test the API interactively.

---

## **3. Interacting with the API (Command Line)**

You can interact with the ChatBox app through the `/chat` endpoint, which accepts POST requests with a `query` parameter.

### **Making Requests with `curl`**

Use `curl` to send a POST request to the FastAPI app.

#### **Basic Chat Request**

1. Open a terminal and use the following `curl` command to send a chat query:

   ```bash
   curl -X 'POST' \
     'http://localhost:8000/chat' \
     -H 'Content-Type: application/json' \
     -d '{"query": "What is FastAPI?"}'
   ```

   **Response Example**:
   ```json
   {
     "response": "FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+."
   }
   ```

2. **Cached Response**:
   If the query was previously asked and cached in Redis, the cached response will be returned directly, saving time.

   Example of a cached response:
   ```json
   {
     "response": "FastAPI is a modern web framework for building APIs."
   }
   ```

---

## **4. Error Handling**

The application uses HTTP exceptions to handle errors. The most common errors are:

- **500 Internal Server Error**: This occurs when an error happens on the server side, like failing to fetch search results or generate a response.
  
  **Example response**:
  ```json
  {
    "detail": "Internal Server Error: Unable to connect to Serper API"
  }
  ```

- **422 Unprocessable Entity**: This occurs when the request payload is missing or has invalid data.
  
  **Example response**:
  ```json
  {
    "detail": "Query parameter is required"
  }
  ```

---

## **5. Example Error Cases**

1. **Search Error Example**:
   If the search function fails, such as when the external API cannot be reached:

   **Example Request**:
   ```bash
   curl -X 'POST' \
     'http://localhost:8000/chat' \
     -H 'Content-Type: application/json' \
     -d '{"query": "What is ChatGPT?"}'
   ```

   **Example Response** (if the search API fails):
   ```json
   {
     "detail": "Search error: Search API not reachable"
   }
   ```

2. **Cache Issue Example**:
   If there's a problem with the Redis server or connection:

   **Example Response** (when cache access fails):
   ```json
   {
     "detail": "Cache error: Unable to connect to Redis"
   }
   ```

---

## **6. Stopping the Application**

To stop the application, press `CTRL+C` in the terminal where the app is running. This will gracefully shut down the FastAPI server.

---

## **7. Additional Configuration (Optional)**

### **Changing Redis Connection URL**
If you want to connect to a different Redis instance (e.g., using a password or a remote server), update the `REDIS_URL` in the `.env` file.

Example:
```env
REDIS_URL=redis://:your_password@your_redis_host:6379
```

---

## **8. Troubleshooting**

- **Redis connection issue**: Make sure Redis is installed and running on your machine. Use the `redis-cli` command to connect to Redis and check if it¡¯s available.
  
- **API Errors**: Check the FastAPI application logs for more detailed error messages. You can run the app with `uvicorn app.main:app --reload --port 8000 --log-level debug` to see more detailed logs.

---

## **9. Conclusion**

You're now ready to use the ChatBox FastAPI app! This user manual covered how to run the app, make requests via the command line, handle common errors, and configure the app for different environments.

For any issues or questions, refer to the logs or consult the FastAPI documentation at [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com).

Let me know if you need further assistance! ??
