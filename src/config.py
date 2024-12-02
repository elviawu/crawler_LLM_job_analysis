# config.py
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("請在 .env 檔案中設置 OPENAI_API_KEY")

def get_headers(OPENAI_API_KEY):
        """
        獲取 API 請求標頭
        """
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
            
        return headers