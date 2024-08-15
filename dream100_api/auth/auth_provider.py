from abc import ABC, abstractmethod
from fastapi import Request

class AuthProvider(ABC):
    @abstractmethod
    async def authenticate(self, request: Request) -> dict:
        """Authenticate the request and return user info"""
        pass

    @abstractmethod
    async def get_user_info(self, user_id: str) -> dict:
        """Retrieve user information"""
        pass
