import logging
from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from .auth_provider import AuthProvider

logger = logging.getLogger(__name__)

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, auth_provider: AuthProvider):
        super().__init__(app)
        self.auth_provider = auth_provider
        logger.debug("AuthMiddleware initialized")

    async def dispatch(self, request: Request, call_next):
        logger.debug(f"AuthMiddleware: Processing request to {request.url}")
        if not hasattr(request.state, 'user'):
            try:
                user_info = await self.auth_provider.authenticate(request)
                logger.debug(f"AuthMiddleware: Authentication successful. User info: {user_info}")
                request.state.user = user_info
            except HTTPException as e:
                logger.debug(f"AuthMiddleware: Authentication failed. Error: {e.detail}")
                request.state.user = None
        
        response = await call_next(request)
        return response