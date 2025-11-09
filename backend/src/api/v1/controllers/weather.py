from typing import Dict, Any
from fastapi import HTTPException

from src.api.v1.services.weather import WeatherService
from src.api.v1.schemas.weather import WeatherRequest
from src.utils.logger import get_logger

logger = get_logger(__name__)


class WeatherController:
    
    def __init__(self):
        self.service = WeatherService()
    
    async def get_current(self, request: WeatherRequest) -> Dict[str, Any]:
        try:
            logger.info("Processing weather request", city=request.city)
            
            if not request.city and not (request.lat and request.lon):
                raise HTTPException(
                    status_code=400,
                    detail="City name or coordinates required"
                )
            

            data = await self.service.get_current_weather(request)
            
  
            return {
                "success": True,
                "data": {
                    "location": data["processed"]["location"],
                    "current": data["processed"]["current"],
                    "wind": data["processed"]["wind"],
                    "clouds": data["processed"]["clouds"],
                    "visibility": data["processed"]["visibility"],
                    "timestamp": data["processed"]["timestamp"]
                },
                "cache_info": data["cache_info"],
                "message": "Weather data retrieved successfully"
            }
            
        except ValueError as e:
            logger.error("Weather service error", error=str(e))
            raise HTTPException(status_code=400, detail=str(e))
        
        except Exception as e:
            logger.error("Unexpected weather error", error=str(e))
            raise HTTPException(status_code=500, detail="Internal server error")
    
    async def get_forecast(self, request: WeatherRequest, days: int = 5) -> Dict[str, Any]:
        try:

            if days < 1 or days > 5:
                raise HTTPException(
                    status_code=400,
                    detail="Days must be between 1 and 5"
                )
            
            logger.info("Processing forecast request", city=request.city, days=days)
            
            data = await self.service.get_weather_forecast(request, days)
            
            return {
                "success": True,
                "data": {
                    "location": data["processed"]["location"],
                    "forecast": data["processed"]["forecast"],
                    "days_count": len(data["processed"]["forecast"])
                },
                "cache_info": data["cache_info"],
                "message": f"{days}-day forecast retrieved successfully"
            }
            
        except ValueError as e:
            logger.error("Forecast service error", error=str(e))
            raise HTTPException(status_code=400, detail=str(e))
        
        except Exception as e:
            logger.error("Unexpected forecast error", error=str(e))
            raise HTTPException(status_code=500, detail="Internal server error")

weather_controller = WeatherController()
