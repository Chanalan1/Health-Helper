from flask import Flask, render_template, request, session
from dotenv import load_dotenv
from chatbot_assistant import create_thread, add_message_to_thread, run_assistant_on_thread, retrieve_run_status, list_thread_messages
import time

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.secret_key = 'VspS7GtxZY2ZaWSeMmRFF7PeuQkExvge'  # Required for session management

# Replace with your OpenAI assistant's model ID
model_id = "asst_N2jeiYSprp2QuKmRxifggRnr"


# Home route
@app.route('/')
def home():
    return render_template('index.html')


# Chatbot route
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']

    # Handle exit command
    if user_input.lower() == 'exit':
        return "Thank you for using Mind Aid, please visit again"

    # Initialize or retrieve thread_id from session
    if 'thread_id' not in session:
        thread = create_thread()
        session['thread_id'] = thread.id

    # Add user message to thread
    add_message_to_thread(session['thread_id'], user_input)

    # Run assistant on the thread
    run = run_assistant_on_thread(session['thread_id'], model_id)

    # Poll run status until completed
    while run.status != "completed":
        time.sleep(1)
        run = retrieve_run_status(session['thread_id'], run.id)

    # Retrieve messages in the thread
    messages = list_thread_messages(session['thread_id'])

    # Find the last assistant message
    assistant_response = ""
    for msg in messages:
        if msg.role == "assistant":
            assistant_response = msg.content[0].text.value
            break

    return assistant_response


if __name__ == '__main__':
    app.run(debug=True)
