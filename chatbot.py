from openai import OpenAI
import os
from dotenv import load_dotenv
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionUserMessageParam,
    ChatCompletionSystemMessageParam,
)

# Load environment variables from a .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Get the API key from environment variables
def get_openai_response(prompt: str) -> str:
    """
    Function to get a response from OpenAI API based on the given prompt.
    """
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            ChatCompletionSystemMessageParam(
                role="system", 
                content="You are a helpful assistant."
            ),
            ChatCompletionUserMessageParam(
                role="user", 
                content=prompt
            )
        ],
        max_tokens=150,
        temperature=0.7)
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

def main():
    print("Welcome to the OpenAI Chatbot. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        response = get_openai_response(user_input)
        print(f"Bot: {response}")

if __name__ == "__main__":
    main()
