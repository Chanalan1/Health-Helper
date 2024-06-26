import openai
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Get the API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")



