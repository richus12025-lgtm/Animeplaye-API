import asyncio
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from sources.animepahe import AnimePahe
from models.anime import SearchResult, Anime, Episode, Source

app = FastAPI(title="AnimePahe API", description="API for AnimePahe", version="1.0.0")

# ========== ADD CORS MIDDLEWARE (Fixes frontend connection) ==========
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Allows all origins (ok for school project)
    allow_credentials=True,
    allow_methods=["*"],           # Allows all HTTP methods
    allow_headers=["*"],           # Allows all headers
)
# ====================================================================

animepahe = AnimePahe()

@app.get("/")
async def root():
    return {"message": "AnimePahe API is running. Visit /docs for documentation."}

@app.get("/search", response_model=SearchResult)
async def search_anime(q: str = Query(..., description="Search query"), page: int = Query(1, ge=1)):
    """Search for anime by title."""
    result = await animepahe.search(q, page)
    return result

@app.get("/anime/{anime_id}", response_model=Anime)
async def get_anime_info(anime_id: str, session: Optional[str] = Query(None)):
    """Get detailed information about a specific anime."""
    info = await animepahe.get_anime(anime_id, session)
    return info

@app.get("/episodes")
async def get_episodes(session: str = Query(..., description="Anime session ID"), page: int = Query(1, ge=1)):
    """Get list of episodes for an anime."""
    episodes = await animepahe.get_episodes(session, page)
    return episodes

@app.get("/sources")
async def get_sources(anime_session: str = Query(...), episode_session: str = Query(...)):
    """Get download sources for a specific episode."""
    sources = await animepahe.get_sources(anime_session, episode_session)
    return sources
