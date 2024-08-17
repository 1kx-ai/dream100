import os
import logging
from fastapi import HTTPException, Request
from .auth_provider import AuthProvider
from config import config

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class BearerAuth(AuthProvider):
    def __init__(self):
        self.api_keys = {config.API_KEY: "admin"}
        logger.debug(f"Initialized BearerAuth with API keys: {self.api_keys}")

    async def authenticate(self, request: Request) -> dict:
        auth_header = request.headers.get("Authorization")
        logger.debug(f"Received Authorization header: {auth_header}")
        if not auth_header or not auth_header.startswith("Bearer "):
            logger.debug("Invalid authorization header")
            raise HTTPException(status_code=401, detail="Invalid authorization header")
        token = auth_header.split()[1]
        logger.debug(f"Extracted token: {token}")
        if token in self.api_keys:
            logger.debug("Valid token found")
            return {"user_id": token, "role": self.api_keys[token]}
        logger.debug("Invalid token")
        raise HTTPException(status_code=401, detail="Invalid token")

    async def get_user_info(self, user_id: str) -> dict:
        if user_id in self.api_keys:
            return {"user_id": user_id, "role": self.api_keys[user_id]}
        raise HTTPException(status_code=404, detail="User not found")
