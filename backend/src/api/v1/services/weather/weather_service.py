from typing import Dict, Any
from src.utils.cache import cached
from src.utils.logger import get_logger
from src.api.v1.schemas.weather import WeatherRequest, CurrentWeatherData
from .api_client import WeatherAPIClient
from .processors import WeatherDataProcessor

logger = get_logger(__name__)


class WeatherService:
    
    
    def __init__(self):
        self.api_client = WeatherAPIClient()
        self.processor = WeatherDataProcessor()
    
    @cached(ttl=1800, key_prefix="weather_current")
    async def get_current_weather(self, request_data: WeatherRequest) -> Dict[str, Any]:
        response = await self.api_client.fetch_current_weather(request_data, cache_ttl=1800)
        
        if response["status_code"] != 200:
            error_message = f"Erro na API: {response.get('data', {}).get('message', 'Erro desconhecido')}"
            logger.error(
                "Erro ao buscar dados meteorológicos",
                status_code=response["status_code"],
                error=error_message
            )
            raise ValueError(error_message)
        
        weather_data = CurrentWeatherData(**response["data"])
        processed_data = self.processor.process_current_weather(weather_data)
        processed_data["cache_info"] = response["cache_info"]
        
        logger.info(
            "Dados meteorológicos obtidos com sucesso",
            city=weather_data.name,
            temperature=weather_data.main.temp,
            cached=response["cache_info"]["cached"]
        )
        
        return processed_data
    
    @cached(ttl=3600, key_prefix="weather_forecast")
    async def get_weather_forecast(
        self, 
        request_data: WeatherRequest,
        days: int = 5
    ) -> Dict[str, Any]:
        if days > 5:
            days = 5
        

        response = await self.api_client.fetch_forecast(request_data, cache_ttl=3600)
        
        if response["status_code"] != 200:
            error_message = f"Erro na API: {response.get('data', {}).get('message', 'Erro desconhecido')}"
            logger.error(
                "Erro ao buscar previsão meteorológica",
                status_code=response["status_code"],
                error=error_message
            )
            raise ValueError(error_message)
        
        forecast_data = response["data"]
        processed_forecast = self.processor.process_forecast(forecast_data, days)
        
        result = {
            "processed": processed_forecast,
            "raw_data": forecast_data,
            "cache_info": response["cache_info"]
        }
        
        logger.info(
            "Previsão meteorológica obtida com sucesso",
            city=forecast_data["city"]["name"],
            days=len(processed_forecast["forecast"]),
            cached=response["cache_info"]["cached"]
        )
        
        return result


weather_service = WeatherService()
