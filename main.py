from dotenv import load_dotenv
import os

load_dotenv()

print("Environment loaded successfully")
print("OpenAI key present:", bool(os.getenv("OPENAI_API_KEY")))
