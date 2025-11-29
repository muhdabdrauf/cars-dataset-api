import os
from fastapi import Header, HTTPException, status, Depends
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
print("Loaded API_KEY =", API_KEY)

def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
    return True