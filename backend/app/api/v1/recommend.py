from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import structlog

from app.core.security import get_current_user

logger = structlog.get_logger()
router = APIRouter(prefix="/recommend", tags=["recommendation"])

class MovieItem(BaseModel):
    id: str
    title: str
    poster_path: Optional[str] = None
    vote_average: float
    genres: List[str]
    match_score: float

class RecommendationResponse(BaseModel):
    algorithm: str
    movies: List[MovieItem]

@router.get("/personalized", response_model=RecommendationResponse)
async def get_personalized_recommendations(
    user_id: str = Depends(get_current_user),
    limit: int = Query(20, le=100)
):
    """Get personalized recommendations using NCF/SVD hybrid model."""
    # Placeholder for actual ML inference
    logger.info("fetch_personalized_recs", user_id=user_id, limit=limit)
    
    # Return mock data for the scaffold
    movies = [
        MovieItem(
            id="1", 
            title="Inception", 
            vote_average=8.8, 
            genres=["Action", "Sci-Fi"],
            match_score=0.95
        ),
        MovieItem(
            id="2", 
            title="Interstellar", 
            vote_average=8.6, 
            genres=["Adventure", "Sci-Fi"],
            match_score=0.92
        )
    ]
    return RecommendationResponse(algorithm="hybrid_ncf_svd", movies=movies)

@router.get("/trending", response_model=RecommendationResponse)
async def get_trending_movies(limit: int = Query(20, le=100)):
    """Get globally trending movies."""
    movies = [
        MovieItem(
            id="3", 
            title="Dune: Part Two", 
            vote_average=8.3, 
            genres=["Sci-Fi", "Adventure"],
            match_score=0.88
        )
    ]
    return RecommendationResponse(algorithm="trending", movies=movies)
