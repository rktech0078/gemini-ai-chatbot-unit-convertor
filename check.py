import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if API Key is loading correctly
api_key = os.getenv("MISTRAL_API_KEY")

if not api_key:
    print("❌ Error: MISTRAL_API_KEY not found! Check your .env file.")
else:
    print("✅ API Key Loaded Successfully:", api_key[:5] + "********")  # Hide full key
