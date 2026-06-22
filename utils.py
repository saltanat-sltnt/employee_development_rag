import os
from dotenv import load_dotenv


def setup_openai_key():
    load_dotenv()

    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY not found. Add it to your .env file.")
