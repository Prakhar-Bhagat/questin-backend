from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import communities
from app.routers import communities, access, requests, pitches, waitlist
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.limiter import limiter
import os

app = FastAPI(title="Questin API", version="0.1.0")


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


origins = [
    "http://localhost:5173",
    "https://questin-alpha.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)


app.include_router(communities.router, prefix="/communities", tags=["communities"])
app.include_router(access.router,      prefix="/access-requests", tags=["access"])
app.include_router(requests.router,    prefix="/venue-requests", tags=["venue requests"])
app.include_router(pitches.router,     prefix="/pitches", tags=["pitches"])
app.include_router(waitlist.router,    prefix="/waitlist", tags=["waitlist"])
@app.get("/health")
async def health():
    return {"status": "ok"}

import logging
logging.basicConfig(level=logging.DEBUG)