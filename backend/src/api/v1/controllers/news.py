from typing import Dict, Any
from fastapi import HTTPException

from src.api.v1.services.news import NewsService
from src.api.v1.schemas.news import NewsRequest
from src.utils.logger import get_logger

logger = get_logger(__name__)


class NewsController:
   
    
    def __init__(self):
        self.service = NewsService()
    
    async def get_headlines(self, request: NewsRequest) -> Dict[str, Any]:
        try:
            logger.info(
                "Processing headlines request", 
                country=request.country,
                category=request.category
            )
            
            data = await self.service.get_top_headlines(request)
            
            return {
                "success": True,
                "data": {
                    "articles": data["articles"],
                    "total_results": data["total_results"],
                    "pagination": data["pagination"],
                    "filters": data["filters"]
                },
                "cache_info": data["cache_info"],
                "message": f"Found {len(data['articles'])} headlines"
            }
            
        except ValueError as e:
            error_msg = str(e)
            logger.error(f"Headlines service error: {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)
        
        except HTTPException:
            raise
        
        except Exception as e:
            error_msg = str(e)
            error_type = type(e).__name__
            import traceback
            stack_trace = traceback.format_exc()
            logger.error(f"Unexpected headlines error ({error_type}): {error_msg}\n{stack_trace}")
            raise HTTPException(status_code=500, detail=f"Internal server error: {error_msg}")
    
    async def search_news(self, request: NewsRequest) -> Dict[str, Any]:
        try:
            if not request.query:
                raise HTTPException(
                    status_code=400,
                    detail="Search query is required"
                )
            
            logger.info("Processing news search", query=request.query)
            
            data = await self.service.search_everything(request)
            
            return {
                "success": True,
                "data": {
                    "articles": data["articles"],
                    "total_results": data["total_results"],
                    "sources_count": data["sources_count"],
                    "pagination": data["pagination"],
                    "search_params": data["search_params"]
                },
                "cache_info": data["cache_info"],
                "message": f"Found {data['total_results']} articles"
            }
            
        except ValueError as e:
            error_msg = str(e)
            logger.error(f"News search error: {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)
        
        except HTTPException:
            raise
        
        except Exception as e:
            error_msg = str(e)
            error_type = type(e).__name__
            import traceback
            stack_trace = traceback.format_exc()
            logger.error(f"Unexpected search error ({error_type}): {error_msg}\n{stack_trace}")
            raise HTTPException(status_code=500, detail=f"Internal server error: {error_msg}")
    
    async def get_sources(self, category: str = None, country: str = None) -> Dict[str, Any]:
        """Get news sources"""
        try:
            logger.info("Processing sources request", category=category, country=country)
            
            data = await self.service.get_sources(category, country)
            
            return {
                "success": True,
                "data": {
                    "sources": data["sources"],
                    "total_sources": data["total_sources"],
                    "categories": data["categories"],
                    "countries": data["countries"]
                },
                "cache_info": data["cache_info"],
                "message": f"Found {data['total_sources']} sources"
            }
            
        except HTTPException:
            raise
        
        except Exception as e:
            error_msg = str(e)
            error_type = type(e).__name__
            import traceback
            stack_trace = traceback.format_exc()
            logger.error(f"Sources error ({error_type}): {error_msg}\n{stack_trace}")
            raise HTTPException(status_code=500, detail=f"Internal server error: {error_msg}")


news_controller = NewsController()
