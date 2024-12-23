import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
CSE_ID = os.getenv('CSE_ID')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')