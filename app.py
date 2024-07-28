from flask import Flask, request, render_template, jsonify
from openai import OpenAI
import os
import time
from dotenv import load_dotenv
from openai.types.chat import ChatCompletionUserMessageParam, ChatCompletionSystemMessageParam

# Load environment variables from a .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

model_id = "asst_N2jeiYSprp2QuKmRxifggRnr"

def create_thread():
    return client.beta.threads.create()

def add_message_to_thread(thread_id, content):
    return client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )

def run_assistant_on_thread(thread_id, assistant_id):
    return client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions="Please refer to your instructions."
    )

def retrieve_run_status(thread_id, run_id):
    return client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id
    )

def list_thread_messages(thread_id):
    return client.beta.threads.messages.list(
        thread_id=thread_id,
        order="asc"
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    thread = create_thread()
    add_message_to_thread(thread.id, user_input)
    run = run_assistant_on_thread(thread.id, model_id)
    
    while run.status != "completed":
        time.sleep(1)
        run = retrieve_run_status(thread.id, run.id)
    
    messages = list_thread_messages(thread.id)
    for msg in messages:
        if msg.role == "assistant":
            response = msg.content[0].text.value
            return jsonify({'message': response})
    
    return jsonify({'message': 'Something went wrong. Please try again.'})

if __name__ == "__main__":
    app.run(debug=True)
