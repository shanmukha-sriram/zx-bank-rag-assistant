from dotenv import load_dotenv
load_dotenv()
import os
from groq import Groq

client = Groq(api_key=os.getenv("LLM_API_KEY"))
for m in client.models.list().data:
    print(m.id)
