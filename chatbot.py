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

def get_openai_response(prompt: str, temperature: float = 0.7, max_tokens: int = 150) -> str:
    """
    Function to get a response from OpenAI API based on the given prompt.
    variable temperature: used to determine accurate response, 0.5-0.7 recommended
    """
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            ChatCompletionSystemMessageParam(
                role="system", 
                content="You are a knowledgeable, smart assistant who provideds concise and accurate answers."
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
        # gives us what type of error is being generated
        return f"Error attempting to generate answer: {e}"

def main():
    print("Welcome to the OpenAI Chatbot. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Thank you for using Mind Aid, please visit again")
            break
        response = get_openai_response(user_input, temperature=0.7, max_tokens=150)
        print(f"Bot: {response}")

if __name__ == "__main__":
    main()
