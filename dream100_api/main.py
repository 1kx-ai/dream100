from fastapi import FastAPI
from .auth.bearer_auth import BearerAuth
from .auth.middleware import AuthMiddleware
from .routers import projects

app = FastAPI()

# Initialize with Bearer token auth
auth_provider = BearerAuth()

# Add the auth middleware
app.add_middleware(AuthMiddleware, auth_provider=auth_provider)

# Include routers
app.include_router(projects.router)

# You can add more routers here as your API grows