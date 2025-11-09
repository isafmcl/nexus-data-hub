from fastapi import APIRouter, Query
from typing import Optional

from src.api.v1.controllers.news import news_controller
from src.api.v1.schemas.news import NewsRequest
from src.api.v1.schemas.base import SuccessResponse

router = APIRouter(prefix="/news", tags=["News"])


@router.get("", response_model=SuccessResponse)
@router.get("/", response_model=SuccessResponse)
async def get_news(
    category: Optional[str] = Query("general", description="Category"),
    country: str = Query("us", description="Country code"),
    page_size: int = Query(10, ge=1, le=100, description="Articles per page"),
):
    request = NewsRequest(
        country=country,
        category=category,
        page_size=page_size,
        page=1,
        language="en"
    )
    
    return await news_controller.get_headlines(request)


@router.get("/headlines", response_model=SuccessResponse)
async def top_headlines(
    country: str = Query("br", description="Country code"),
    category: Optional[str] = Query(None, description="Category"),
    query: Optional[str] = Query(None, description="Search term"),
    page_size: int = Query(10, ge=1, le=100, description="Articles per page"),
    page: int = Query(1, ge=1, description="Page number"),
    language: str = Query("pt", description="Language")
):
    request = NewsRequest(
        country=country,
        category=category,
        query=query,
        page_size=page_size,
        page=page,
        language=language
    )
    
    return await news_controller.get_headlines(request)


@router.get("/search", response_model=SuccessResponse)
async def search_news(
    query: str = Query(..., description="Search query"),
    language: str = Query("pt", description="Language"),
    sort_by: str = Query("publishedAt", description="Sort by"),
    page_size: int = Query(10, ge=1, le=100, description="Articles per page"),
    page: int = Query(1, ge=1, description="Page number")
):
    request = NewsRequest(
        query=query,
        language=language,
        sort_by=sort_by,
        page_size=page_size,
        page=page
    )
    
    return await news_controller.search_news(request)


@router.get("/sources", response_model=SuccessResponse)
async def news_sources(
    category: Optional[str] = Query(None, description="Category filter"),
    country: Optional[str] = Query(None, description="Country filter")
):

    return await news_controller.get_sources(category, country)


@router.get("/health")
async def news_health():
    """News service health check"""
    return {
        "service": "news",
        "status": "healthy",
        "provider": "NewsAPI"
    }
