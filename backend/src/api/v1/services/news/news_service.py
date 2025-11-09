from typing import Dict, Any
from src.utils.cache import cached
from src.utils.logger import get_logger
from src.api.v1.schemas.news import NewsRequest
from .api_client import NewsAPIClient
from .processors import NewsDataProcessor

logger = get_logger(__name__)


class NewsService:
    
    def __init__(self):
        self.api_client = NewsAPIClient()
        self.processor = NewsDataProcessor()
    
    @cached(ttl=1800, key_prefix="news_headlines")
    async def get_top_headlines(self, request_data: NewsRequest) -> Dict[str, Any]:
        params = self._build_headlines_params(request_data)
        
        response = await self.api_client.make_request(
            endpoint="top-headlines",
            params=params,
            cache_ttl=1800
        )
        
        self.api_client.validate_response(response)
        
        data = response.get("data", {})
        articles = self.processor.process_articles(data.get("articles", []))
        stats = self.processor.calculate_statistics(articles)
        
        logger.info(
            "Top headlines obtidos com sucesso",
            total=len(articles),
            cached=response["cache_info"]["cached"]
        )
        
        return {
            "articles": articles,
            "total_results": data.get("totalResults", len(articles)),
            "pagination": {
                "page": request_data.page,
                "page_size": request_data.page_size,
                "total_results": data.get("totalResults", len(articles))
            },
            "filters": {
                "country": request_data.country,
                "category": request_data.category,
                "language": request_data.language
            },
            "cache_info": response["cache_info"]
        }
    
    @cached(ttl=3600, key_prefix="news_search")
    async def search_everything(self, request_data: NewsRequest) -> Dict[str, Any]:
        if not request_data.query:
            raise ValueError("Query de busca é obrigatória")
        
        params = self._build_search_params(request_data)
        
        response = await self.api_client.make_request(
            endpoint="everything",
            params=params,
            cache_ttl=3600
        )
        
        self.api_client.validate_response(response)
        
        data = response.get("data", {})
        articles = self.processor.process_articles(data.get("articles", []))
        stats = self.processor.calculate_statistics(articles)
        
        logger.info(
            "Busca de notícias concluída",
            query=request_data.query,
            total=len(articles),
            cached=response["cache_info"]["cached"]
        )
        
        return {
            "articles": articles,
            "total_results": data.get("totalResults", len(articles)),
            "sources_count": stats.get("sources_count", 0),
            "pagination": {
                "page": request_data.page,
                "page_size": request_data.page_size,
                "total_results": data.get("totalResults", len(articles))
            },
            "search_params": {
                "query": request_data.query,
                "language": request_data.language,
                "sort_by": request_data.sort_by
            },
            "cache_info": response["cache_info"]
        }
    
    @cached(ttl=3600, key_prefix="news_sources")
    async def get_sources(
        self, 
        category: str = None, 
        country: str = None
    ) -> Dict[str, Any]:
        params = {}
        if category:
            params["category"] = category
        if country:
            params["country"] = country
        
        response = await self.api_client.make_request(
            endpoint="sources",
            params=params,
            cache_ttl=3600
        )
        
        self.api_client.validate_response(response)
        
        data = response.get("data", {})
        sources = data.get("sources", [])
        
        # Extrair categorias e países únicos
        categories = list(set(s.get("category", "") for s in sources if s.get("category")))
        countries = list(set(s.get("country", "") for s in sources if s.get("country")))
        
        logger.info(
            "Fontes de notícias obtidas",
            total=len(sources),
            cached=response["cache_info"]["cached"]
        )
        
        return {
            "sources": sources,
            "total_sources": len(sources),
            "categories": categories,
            "countries": countries,
            "cache_info": response["cache_info"]
        }
    
    def _build_headlines_params(self, request: NewsRequest) -> Dict[str, Any]:
        params = {
            "pageSize": request.page_size,
            "page": request.page
        }
        
        if request.country:
            params["country"] = request.country
        if request.category:
            params["category"] = request.category
        if request.query:
            params["q"] = request.query
        
        return params
    
    def _build_search_params(self, request: NewsRequest) -> Dict[str, Any]:
        params = {
            "q": request.query,
            "pageSize": request.page_size,
            "page": request.page,
            "language": request.language,
            "sortBy": request.sort_by
        }
        
        return params

news_service = NewsService()
