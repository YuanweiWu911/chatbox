# Chat Application README

## 1. Project Overview
This chat application combines a FastAPI backend service with a graphical user interface (GUI) built using Tkinter, providing users with a convenient interactive environment. Users can enter queries in the GUI. The application first checks the Redis cache for corresponding results. If not found, it searches the web for relevant information, then invokes the local Ollama model to generate responses, and caches the results for future queries.

## 2. Features

### 2.1 Backend Features
- **Caching Mechanism**: Utilizes Redis as a cache to effectively improve query efficiency and reduce the overhead of repeated queries.
- **Web Search**: Performs web searches using the Serper API to accurately obtain relevant web page links.
- **Content Parsing**: Intelligently parses the content of the searched web pages to extract useful information.
- **Model Invocation**: Calls the local Ollama model to generate professional responses.

### 2.2 Frontend Features
- **Graphical User Interface (GUI)**: Built with Tkinter, it offers an intuitive and user - friendly interface for users to input queries and view responses.
- **Conversation Display**: Clearly shows user queries and bot responses, distinguishing different types of content.
- **Error Handling**: Displays corresponding error message boxes when the input is empty, there is a network connection failure, or the server returns an error.

## 3. Installation Steps

### 3.1 Clone the Repository
```bash
git clone https://github.com/YuanweiWu911/chatbox.git
cd chatbox
```

### 3.2 Create and Activate a Virtual Environment (Optional but Recommended)
```bash
python -m venv chatbox
source chatbox/bin/activate  # For Linux/Mac
.\chatbox\Scripts\activate  # For Windows
```

### 3.3 Install Dependencies
```bash
pip install -r requirements.txt
```

### 3.4 Configure Environment Variables
Create a `.env` file in the project root directory and add the following content:
```plaintext
REDIS_URL=redis://localhost:6379
SERPER_API_KEY=your_serper_api_key
PROXY_URL=your_proxy_url  # Set this value if a proxy is required
```
Replace `your_serper_api_key` with your own Serper API key, and `your_proxy_url` with the actual proxy address (leave it blank if no proxy is needed).

### 3.5 Start the Redis Service
Ensure that the Redis service is started. You can start Redis using the following command:
```bash
redis-server
```

### 3.6 Start the Ollama Service
Make sure the Ollama service is running and listening on the `http://localhost:11434` port.

## 4. Usage

### 4.1 Start the Backend Service
```bash
uvicorn app.main:app --reload
```

### 4.2 Start the Frontend GUI
Run the Python file containing the GUI code, usually by directly executing the file:
```bash
python gui/gui.py  # Assuming the GUI code file is named gui.py and located in the gui directory
```

### 4.3 Interact with the Application
- Enter your query in the input box of the GUI.
- Click the "Send Query" button to send the query request.
- View the user queries and bot responses displayed in the chat area.

## 5. Code Structure
```plaintext
chatbox/
├── app/
│   ├── __init__.py
│   ├── cache.py
│   ├── main.py
│   ├── parser.py
│   └── search.py
├── gui/
│   └── gui.py
├── tests/
│   ├── test_functions.py
│   └── test_main.py
├── .env
├── requirements.txt
├── test_functions.py
├── test_main.py
└── README.md
```
- `app/`: Contains the core backend code of the application.
  - `__init__.py`: Marks the directory as a Python package.
  - `cache.py`: Implements the Redis cache management function.
  - `main.py`: The main entry file of the application, defining the FastAPI application and routes.
  - `parser.py`: Responsible for parsing web page content.
  - `search.py`: Performs web searches through the Serper API.
- `gui/`: Contains the frontend GUI code.
  - `gui.py`: A graphical user interface built using Tkinter.
- `tests/`: Contains test code.
- `.env`: Environment variable configuration file.
- `requirements.txt`: Project dependency file.

## 6. Error Handling and Logging

### 6.1 Backend
The application uses Python's `logging` module for logging. All error messages and important events are recorded in the console for easy debugging and monitoring.

### 6.2 Frontend
In the GUI, when the input is empty, there is a network connection failure, or the server returns an error, corresponding error message boxes will pop up to help users understand the problem in a timely manner.

## 7. Notes
- Ensure that your Serper API key is valid; otherwise, the web search function will not work properly.
- Make sure the Redis service and Ollama service are running normally; otherwise, the caching and model invocation functions will be affected.
- If you modify the running port of the backend service, you need to modify the URL of the request sent in the GUI code accordingly.

## 8. Contribution
If you want to contribute to this project, please submit a Pull Request or raise an Issue.

## 9. License
This project is licensed under the [Specific License Name]. Please refer to the `LICENSE` file for detailed information.
