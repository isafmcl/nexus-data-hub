from typing import Dict, Any, Optional
from src.utils.http_client import http_client
from src.utils.logger import get_logger, APIMetricsLogger
from src.core.settings import settings

logger = get_logger(__name__)
api_metrics_logger = APIMetricsLogger()


class NewsAPIClient:

    
    def __init__(self):
        self.base_url = settings.api_endpoints["news"]
        self.api_key = settings.newsapi_key
    
    def _get_url(self, endpoint: str) -> str:
        return f"{self.base_url}/{endpoint}"
    
    def _get_headers(self) -> Dict[str, str]:
        return {
            "X-API-Key": self.api_key,
            "User-Agent": "Nexus-Data-Hub/1.0"
        }
    
    async def make_request(
        self,
        endpoint: str,
        params: Dict[str, Any],
        cache_ttl: int = 1800
    ) -> Dict[str, Any]:
        url = self._get_url(endpoint)
        headers = self._get_headers()
        
        logger.info(
            f"Fazendo requisição para NewsAPI: {endpoint}",
            endpoint=endpoint,
            params=params
        )
        
        async with http_client() as client:
            response = await client.request(
                "GET",
                url,
                params=params,
                headers=headers,
                cache_ttl=cache_ttl
            )
        
        await api_metrics_logger.log_api_metrics(
            api_name="NewsAPI",
            endpoint=endpoint,
            method="GET",
            status_code=response["status_code"],
            response_time=response["cache_info"]["response_time"],
            cached=response["cache_info"]["cached"]
        )
        
        return response
    
    def validate_response(self, response: Dict[str, Any]) -> None:
        if response["status_code"] != 200:
            error_msg = response.get("data", {}).get("message", "Erro desconhecido")
            logger.error(
                "Erro na resposta da NewsAPI",
                status_code=response["status_code"],
                error=error_msg
            )
            raise ValueError(f"Erro na API: {error_msg}")
        
        data = response.get("data", {})
        if data.get("status") == "error":
            error_msg = data.get("message", "Erro desconhecido")
            logger.error("NewsAPI retornou erro", error=error_msg)
            raise ValueError(f"Erro na API: {error_msg}")
