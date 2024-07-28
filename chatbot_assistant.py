from openai import OpenAI
import os
import time
from dotenv import load_dotenv
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionUserMessageParam,
    ChatCompletionSystemMessageParam,
)

# Load environment variables from a .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create the thread needed for responses that pull from embedded files on platform
# 
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

def get_openai_response(prompt: str, model_id: str, temperature: float = 0.7, max_tokens: int = 150) -> str:
    """
    Function to get a response from your assistant's model based on the given prompt.
    variable temperature: used to determine accurate response, 0.5-0.7 recommended
    """
    try:
        response = client.chat.completions.create(model=model_id,
        messages=[
            ChatCompletionSystemMessageParam(
                role="system", 
                content="You are a knowledgeable, smart assistant who provides concise and accurate answers."
            ),
            ChatCompletionUserMessageParam(
                role="user", 
                content=prompt
            )
        ],
        max_tokens=max_tokens,
        temperature=temperature)
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error attempting to generate answer: {e}"

def main():
    # assistant ID placed here
    model_id = "asst_N2jeiYSprp2QuKmRxifggRnr"  
    thread = create_thread()
    
    print("Welcome to the OpenAI Chatbot. Type 'exit' to quit.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Thank you for using Mind Aid, please visit again")
            break
        
        add_message_to_thread(thread.id, user_input)
        run = run_assistant_on_thread(thread.id, model_id)
        
        # Poll the Run status until it is completed
        while run.status != "completed":
            time.sleep(1)
            run = retrieve_run_status(thread.id, run.id)
        
        messages = list_thread_messages(thread.id)
        
        # Find the last assistant message
        for msg in messages:
            if msg.role == "assistant":
                print(f"Bot: {msg.content[0].text.value}")

if __name__ == "__main__":
    main()