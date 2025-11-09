"""
Countries API Client
Cliente para comunicação com RestCountries API
"""
from typing import Dict, Any
from src.utils.http_client import http_client
from src.utils.logger import get_logger

logger = get_logger(__name__)


class CountriesAPIClient:
    """Cliente para RestCountries API"""
    
    def __init__(self):
        self.base_url = "https://restcountries.com/v3.1"
    
    async def fetch_all(self, fields: str = None) -> Dict[str, Any]:
        """Busca todos os países"""
        url = f"{self.base_url}/all"
        params = {}
        if fields:
            params["fields"] = fields
        
        logger.info("Buscando todos os países")
        
        async with http_client() as client:
            return await client.request("GET", url, params=params)
    
    async def fetch_by_name(self, name: str) -> Dict[str, Any]:
        """Busca país por nome"""
        url = f"{self.base_url}/name/{name}"
        
        logger.info(f"Buscando país: {name}")
        
        async with http_client() as client:
            return await client.request("GET", url)
    
    async def fetch_by_region(self, region: str) -> Dict[str, Any]:
        """Busca países por região"""
        url = f"{self.base_url}/region/{region}"
        
        logger.info(f"Buscando países da região: {region}")
        
        async with http_client() as client:
            return await client.request("GET", url)
    
    async def search(self, query: str, fields: str = None) -> Dict[str, Any]:
        """Busca países por termo"""
        url = f"{self.base_url}/name/{query}"
        params = {}
        if fields:
            params["fields"] = fields
        
        logger.info(f"Buscando países com termo: {query}")
        
        async with http_client() as client:
            return await client.request("GET", url, params=params)
