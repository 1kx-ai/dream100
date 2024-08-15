from fastapi import HTTPException, Request
from .auth_provider import AuthProvider

class ApiKeyAuth(AuthProvider):
    def __init__(self, api_keys: dict):
        self.api_keys = api_keys

    async def authenticate(self, request: Request) -> dict:
        api_key = request.headers.get("X-API-Key")
        if api_key in self.api_keys:
            return {"user_id": api_key, "role": self.api_keys[api_key]}
        raise HTTPException(status_code=403, detail="Invalid API Key")

    async def get_user_info(self, user_id: str) -> dict:
        if user_id in self.api_keys:
            return {"user_id": user_id, "role": self.api_keys[user_id]}
        raise HTTPException(status_code=404, detail="User not found")
