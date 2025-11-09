
from typing import Dict, Any, List, Optional
from src.utils.http_client import http_client
from src.utils.logger import get_logger

logger = get_logger(__name__)


class WorldBankService:

    
    def __init__(self):
        self.base_url = "https://api.worldbank.org/v2"
    
    async def get_countries(self, per_page: int = 100) -> Dict[str, Any]:
    
        try:
            url = f"{self.base_url}/country"
            params = {"format": "json", "per_page": per_page}
            
            logger.info("Buscando lista de países do World Bank")
            
            async with http_client() as client:
                response_data = await client.request("GET", url, params=params)
                response = response_data.get("data")
            
            if isinstance(response, list) and len(response) > 1:
                countries_data = response[1] 
                
                countries = []
                for country in countries_data:
                    countries.append({
                        "id": country.get("id"),
                        "name": country.get("name"),
                        "capital_city": country.get("capitalCity"),
                        "region": country.get("region", {}).get("value"),
                        "income_level": country.get("incomeLevel", {}).get("value"),
                        "longitude": country.get("longitude"),
                        "latitude": country.get("latitude")
                    })
                
                return {
                    "success": True,
                    "message": f"{len(countries)} países encontrados",
                    "data": {
                        "total": len(countries),
                        "countries": countries
                    }
                }
            
            return {
                "success": True,
                "message": "Nenhum país encontrado",
                "data": {
                    "countries": [],
                    "total": 0
                }
            }
            
        except Exception as e:
            logger.error(f"Erro ao buscar países: {e}")
            return {
                "success": False,
                "message": "Erro ao buscar países do World Bank",
                "error": str(e)
            }
    
    async def get_economic_indicator(
        self, 
        country_code: str, 
        indicator: str,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None
    ) -> Dict[str, Any]:
       
        try:
            url = f"{self.base_url}/country/{country_code}/indicator/{indicator}"
            
            params = {"format": "json", "per_page": 100}
            
            if start_year:
                params["date"] = f"{start_year}:{end_year or start_year}"
            
            logger.info(f"Buscando indicador {indicator} para país {country_code}")
            
            async with http_client() as client:
                response_data = await client.request("GET", url, params=params)
                response = response_data.get("data")
            
            if isinstance(response, list) and len(response) > 1:
                metadata = response[0]
                data = response[1]
                
                processed_data = []
                for item in data:
                    if item.get("value") is not None:
                        processed_data.append({
                            "year": item.get("date"),
                            "value": item.get("value"),
                            "country": item.get("country", {}).get("value"),
                            "country_code": item.get("countryiso3code"),
                            "indicator": item.get("indicator", {}).get("value")
                        })
                
                return {
                    "success": True,
                    "country_code": country_code,
                    "indicator": indicator,
                    "total_records": metadata.get("total", 0) if metadata else 0,
                    "data": processed_data
                }
            
            return {
                "success": True,
                "data": [],
                "message": "Nenhum dado encontrado"
            }
            
        except Exception as e:
            logger.error(f"Erro ao buscar indicador {indicator}: {e}")
            return {
                "success": False,
                "error": str(e),
                "country_code": country_code,
                "indicator": indicator
            }


worldbank_service = WorldBankService()
