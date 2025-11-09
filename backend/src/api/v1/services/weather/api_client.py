from typing import Dict, Any
from src.utils.http_client import http_client
from src.utils.logger import get_logger, APIMetricsLogger
from src.core.settings import settings
from src.api.v1.schemas.weather import WeatherRequest

logger = get_logger(__name__)
api_metrics_logger = APIMetricsLogger()


class WeatherAPIClient:
  
    def __init__(self):
        self.base_url = settings.api_endpoints["weather"]
        self.api_key = settings.openweather_api_key
    
    def _build_params(self, request_data: WeatherRequest) -> Dict[str, Any]:

        params = {
            "appid": self.api_key,
            "units": request_data.units,
            "lang": request_data.lang
        }
        
        if request_data.city:
            params["q"] = request_data.city
        elif request_data.lat and request_data.lon:
            params["lat"] = request_data.lat
            params["lon"] = request_data.lon
        else:
            raise ValueError("É necessário fornecer cidade ou coordenadas")
        
        return params
    
    async def fetch_current_weather(
        self, 
        request_data: WeatherRequest,
        cache_ttl: int = 1800
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/weather"
        params = self._build_params(request_data)
        
        logger.info(
            "Buscando dados meteorológicos",
            city=request_data.city,
            coordinates=f"{request_data.lat},{request_data.lon}" if request_data.lat else None
        )
        
        async with http_client() as client:
            response = await client.request("GET", url, params=params, cache_ttl=cache_ttl)
        
        await api_metrics_logger.log_api_metrics(
            api_name="OpenWeatherMap",
            endpoint="weather",
            method="GET",
            status_code=response["status_code"],
            response_time=response["cache_info"]["response_time"],
            cached=response["cache_info"]["cached"]
        )
        
        return response
    
    async def fetch_forecast(
        self, 
        request_data: WeatherRequest,
        cache_ttl: int = 3600
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/forecast"
        params = self._build_params(request_data)
        
        logger.info(
            "Buscando previsão meteorológica",
            city=request_data.city
        )
        
        async with http_client() as client:
            response = await client.request("GET", url, params=params, cache_ttl=cache_ttl)
        
        await api_metrics_logger.log_api_metrics(
            api_name="OpenWeatherMap",
            endpoint="forecast",
            method="GET",
            status_code=response["status_code"],
            response_time=response["cache_info"]["response_time"],
            cached=response["cache_info"]["cached"]
        )
        
        return response
