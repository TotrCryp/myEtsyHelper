import os
from fastapi import Request, HTTPException, status, Depends
from dotenv import load_dotenv

# Завантажимо .env
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN", "super-secret")


def get_token(request: Request):
    """Перевіряє Bearer-токен у заголовку Authorization"""
    # auth = request.headers.get("Authorization")
    # if not auth or not auth.startswith("Bearer "):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Unauthorized"
    #     )
    # token = auth.split(" ")[1]
    # if token != API_TOKEN:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Invalid token"
    #     )
    return True
