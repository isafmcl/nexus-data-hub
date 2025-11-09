from typing import Dict, Any
from src.utils.cache import cached
from src.utils.logger import get_logger
from .api_client import CountriesAPIClient
from .processors import CountriesDataProcessor

logger = get_logger(__name__)


class CountriesService:
    
    def __init__(self):
        self.api_client = CountriesAPIClient()
        self.processor = CountriesDataProcessor()
    
    @cached(ttl=86400, key_prefix="countries_all")
    async def get_all_countries(self) -> Dict[str, Any]:
        try:
            fields = "name,capital,region,population,area,flags,currencies,cca2,cca3"
            response = await self.api_client.fetch_all(fields=fields)
            
            data = response.get("data", [])
            countries = self.processor.process_countries_list(data)
            countries.sort(key=lambda x: x["name"])
            
            logger.info(f"Países obtidos com sucesso: {len(countries)} países")
            
            return {
                "success": True,
                "message": f"{len(countries)} países encontrados",
                "data": {
                    "countries": countries,
                    "total": len(countries)
                },
                "cache_info": response.get("cache_info", {})
            }
        except Exception as e:
            logger.error(f"Erro ao buscar países: {e}")
            raise
    
    @cached(ttl=43200, key_prefix="country_detail")
    async def get_country_by_name(self, name: str) -> Dict[str, Any]:
        try:
            response = await self.api_client.fetch_by_name(name)
            data = response.get("data", [])
            
            if not data:
                return {
                    "success": False,
                    "error": f"País '{name}' não encontrado"
                }
            
            country = self.processor.process_country_detailed(data[0])
            
            logger.info(f"País {name} obtido com sucesso")
            
            return {
                "success": True,
                "message": f"Dados do país {country['name']} obtidos com sucesso",
                "data": country,
                "cache_info": response.get("cache_info", {})
            }
        except Exception as e:
            logger.error(f"Erro ao buscar país {name}: {e}")
            return {
                "success": False,
                "message": f"Erro ao buscar país {name}",
                "error": str(e)
            }
    
    @cached(ttl=21600, key_prefix="countries_region")
    async def get_countries_by_region(self, region: str) -> Dict[str, Any]:
        try:
            response = await self.api_client.fetch_by_region(region)
            data = response.get("data", [])
            
            if not data:
                return {
                    "success": False,
                    "error": f"Região '{region}' não encontrada"
                }
            
            countries = []
            for country_data in data:
                country = {
                    "name": country_data.get("name", {}).get("common", "Unknown"),
                    "capital": country_data.get("capital", ["N/A"])[0] if country_data.get("capital") else "N/A",
                    "population": country_data.get("population", 0),
                    "area": country_data.get("area", 0),
                    "flag": country_data.get("flags", {}).get("png", ""),
                    "code": country_data.get("cca2", "")
                }
                countries.append(country)
            
            countries.sort(key=lambda x: x["population"], reverse=True)
            stats = self.processor.calculate_region_statistics(data)
            
            logger.info(f"Países da região {region} obtidos: {len(countries)} países")
            
            return {
                "success": True,
                "message": f"{len(countries)} países encontrados na região {region}",
                "data": {
                    "region": region,
                    "countries": countries,
                    "total_countries": len(countries),
                    "statistics": stats
                },
                "cache_info": response.get("cache_info", {})
            }
        except Exception as e:
            logger.error(f"Erro ao buscar países da região {region}: {e}")
            return {
                "success": False,
                "message": f"Erro ao buscar países da região {region}",
                "error": str(e)
            }
    
    async def search_countries(self, query: str) -> Dict[str, Any]:
        try:
            fields = "name,capital,region,population,flags,cca2"
            response = await self.api_client.search(query, fields=fields)
            data = response.get("data", [])
            
            if not data:
                return {
                    "success": True,
                    "message": f"Nenhum país encontrado com o termo '{query}'",
                    "data": {
                        "countries": [],
                        "total": 0,
                        "query": query
                    }
                }
            
            countries = []
            for country in data:
                countries.append({
                    "name": country.get("name", {}).get("common", "Unknown"),
                    "official_name": country.get("name", {}).get("official", ""),
                    "capital": country.get("capital", ["N/A"])[0] if country.get("capital") else "N/A",
                    "region": country.get("region", "Unknown"),
                    "population": country.get("population", 0),
                    "flag": country.get("flags", {}).get("png", ""),
                    "code": country.get("cca2", "")
                })
            
            logger.info(f"Busca concluída: {len(countries)} países encontrados")
            
            return {
                "success": True,
                "message": f"{len(countries)} países encontrados com o termo '{query}'",
                "data": {
                    "countries": countries,
                    "total": len(countries),
                    "query": query
                },
                "cache_info": response.get("cache_info", {})
            }
        except Exception as e:
            logger.error(f"Erro ao buscar países com termo {query}: {e}")
            return {
                "success": False,
                "message": f"Erro ao buscar países com o termo '{query}'",
                "error": str(e),
                "data": {"query": query}
            }

countries_service = CountriesService()
