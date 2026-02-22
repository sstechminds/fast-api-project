from dotenv import load_dotenv
import os
from loguru import logger

load_dotenv()

api_key = os.getenv("API_KEY")
logger.info(f"API key is {api_key}")
