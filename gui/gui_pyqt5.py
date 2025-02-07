import sys
import requests
import re
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTextEdit, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from dotenv import load_dotenv

load_dotenv()

# Function to send the query to the FastAPI backend and get the response
def send_query():
    query = entry.text()  # Get the query from the input field

    if not query:
        QMessageBox.warning(window, "Input Error", "Please enter a query.")
        return

    try:
        # Send a POST request to the FastAPI backend
        response = requests.post(
            "http://localhost:8000/chat",  # URL of your FastAPI app
            json={"query": query},
        )

        # Check if the response is successful
        if response.status_code == 200:
            result = response.json().get("response", "No response found.")
            display_conversation(query, result)
        else:
            QMessageBox.critical(window, "Error", f"Error {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        QMessageBox.critical(window, "Network Error", f"Failed to connect to the server. {str(e)}")

def display_conversation(user_query, bot_response):
    # Insert the user query into the chat display area with blue color
    chat_display.append(f'<font color="blue" size="20px"><b>User: {user_query}</b></font>')

    # Split the bot response into <think> parts and other parts
    parts = re.split(r'(<think>.*?</think>)', bot_response, flags=re.IGNORECASE | re.DOTALL)
    for part in parts:
        if part.startswith('<think>') and part.endswith('</think>'):
            # Remove the <think> and </think> tags
            think_content = part[7:-8]
            # Insert think content with grey color
            chat_display.append(f'<font color="grey" size ="20px">{think_content}</font>')
        elif part:
            # Insert other content as regular bot response with green color
            chat_display.append(f'<font color="green" size="20px">{part}</font>')

    # Clear the input field for the next query
    entry.clear()

# Create the main window
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Chat with FastAPI")

# Set window size
window.setGeometry(100, 100, 700, 500)

# Create the layout for the main window
layout = QVBoxLayout()

# Create a label for the input field
input_label = QLabel("Enter your query:", window)
input_label.setAlignment(Qt.AlignLeft)
layout.addWidget(input_label)

# Create the input field for entering queries
entry = QLineEdit(window)
entry.setPlaceholderText("Type your query here...")
layout.addWidget(entry)

# Create a send button
send_button = QPushButton("Send Query", window)
send_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px;")
send_button.clicked.connect(send_query)
layout.addWidget(send_button)
entry.returnPressed.connect(send_query)

# Create a text area to display the chat conversation
chat_display = QTextEdit(window)
chat_display.setReadOnly(True)
chat_display.setStyleSheet("background-color: #f5f5f5; font-family: Arial; font-size: 20px;")
#chat_display.setStyleSheet("background-color: #f5f5f5; font-family: Arial; font-size: 14px;")
layout.addWidget(chat_display)

# Set the layout for the window
window.setLayout(layout)

# Show the window
window.show()

# Start the application event loop
sys.exit(app.exec_())
