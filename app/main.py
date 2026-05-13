from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import communities
from app.routers import communities, access, requests, pitches, waitlist

app = FastAPI(title="Questin API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
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