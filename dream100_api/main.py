from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .auth.bearer_auth import BearerAuth
from .auth.middleware import AuthMiddleware
from .routers import projects, influencers, web_properties, content_embeddings
from .routers.content_embeddings import router as content_embeddings_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React app's address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize with Bearer token auth
auth_provider = BearerAuth()

# Add the auth middleware
app.add_middleware(AuthMiddleware, auth_provider=auth_provider)

# Include routers
app.include_router(projects.router)
app.include_router(influencers.router)
app.include_router(web_properties.router)
app.include_router(content_embeddings_router, prefix="/api", tags=["content_embeddings"])
