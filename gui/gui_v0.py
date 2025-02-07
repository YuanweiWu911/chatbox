# gui/gui.py
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
import requests
import re

# Function to send the query to the FastAPI backend and get the response
def send_query():
    query = entry.get()  # Get the query from the entry widget

    if not query:
        messagebox.showerror("Input Error", "Please enter a query.")
        return

    try:
        # Send a POST request to the FastAPI backend
        response = requests.post(
            "http://localhost:8000/chat",  # URL of your FastAPI app
            json={"query": query},
        )

        # Check if the response is successful
        if response.status_code == 200:
            result = "normal bot answer  <think>thinking part</think> normal bot answer"
            result = response.json().get("response", "No response found.")
            display_conversation(query, result)
        else:
            messagebox.showerror("Error", f"Error {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Network Error", f"Failed to connect to the server. {str(e)}")

def display_conversation(user_query, bot_response):
    # Enable the text widget to insert new text
    chat_display.config(state=tk.NORMAL)

    # Insert the user query in the left part (blue font)
    chat_display.insert(tk.END, f"User: {user_query}\n", 'user')

    # Split the bot response into <think> parts and other parts
    parts = re.split(r'(<think>.*?</think>)', bot_response, flags=re.IGNORECASE | re.DOTALL)
    for part in parts:
        if part.startswith('<think>') and part.endswith('</think>'):
            # Remove the <think> and </think> tags
            think_content = part[7:-8]
            # Insert think content with 'think' tag
            chat_display.insert(tk.END, f"{think_content}", 'think')
        elif part:
            # Insert other content with 'bot' tag
            chat_display.insert(tk.END, f"{part}", 'bot')
    # Add a newline after the bot response
    chat_display.insert(tk.END, "\n")

    # Scroll to the end of the conversation
    chat_display.yview(tk.END)

    # Disable the text widget to prevent manual editing
    chat_display.config(state=tk.DISABLED)

    # Clear the entry widget for the next input
    entry.delete(0, tk.END)

# Create the main window
root = tk.Tk()
root.title("Chat with FastAPI")

# Set window size and background color
root.geometry("700x1200")  # Larger window to potentially show more lines
root.config(bg="#f0f0f0")

# Create and place the chat display area with a scrollable text box
frame = tk.Frame(root)
frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

chat_display = tk.Text(frame, wrap=tk.WORD, state=tk.DISABLED, bg="#f5f5f5", font=("Arial", 14), padx=10, pady=10)
chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Add a vertical scrollbar for the text box
scrollbar = tk.Scrollbar(frame, command=chat_display.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

chat_display.config(yscrollcommand=scrollbar.set)

# Add a label for the input field
input_label = tk.Label(root, text="Enter your query:", font=("Arial", 16), bg="#f0f0f0")
input_label.pack(pady=10)

# Create and place the input field for entering queries
entry = tk.Entry(root, width=60, font=("Arial", 16))
entry.pack(pady=5)

# Create and place the send button
send_button = tk.Button(root, text="Send Query", command=send_query, font=("Arial", 16), bg="#4CAF50", fg="white")
send_button.pack(pady=10)

# Configure styles for the chat display (user's questions and bot's responses)
chat_display.tag_config('user', foreground="#1f77b4", font=("Arial", 14, "bold"))
# Set the bot response font to normal and increase the size by 1.2 times
bot_font = ("Arial", int(14),"bold")
chat_display.tag_config('bot', foreground="#2ca02c", font=bot_font)
# Set the think content font to black and normal
think_font = ("Arial", int(14))
chat_display.tag_config('think', foreground="grey", font=think_font)

# Start the Tkinter event loop
root.mainloop()
