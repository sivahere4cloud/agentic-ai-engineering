import os
from dotenv import load_dotenv

load_dotenv(override=True)

for name in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_API_KEY", "GROQ_API_KEY", "HF_TOKEN"]:
    print(f"{name}: {'loaded' if os.getenv(name) else 'MISSING'}")