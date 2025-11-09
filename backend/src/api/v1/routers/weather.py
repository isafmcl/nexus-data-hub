from fastapi import APIRouter, Query, HTTPException
from typing import Optional

from src.api.v1.controllers.weather import weather_controller
from src.api.v1.schemas.weather import WeatherRequest
from src.api.v1.schemas.base import SuccessResponse

router = APIRouter(prefix="/weather", tags=["Weather"])


@router.get("", response_model=SuccessResponse)
@router.get("/", response_model=SuccessResponse)
async def get_weather(
    city: str = Query(..., description="City name"),
    units: str = Query("metric", description="Units (metric/imperial/kelvin)"),
):

    request = WeatherRequest(
        city=city,
        units=units,
        lang="pt_br"
    )
    
    return await weather_controller.get_current(request)


@router.get("/current", response_model=SuccessResponse)
async def current_weather(
    city: Optional[str] = Query(None, description="City name"),
    lat: Optional[float] = Query(None, description="Latitude"),
    lon: Optional[float] = Query(None, description="Longitude"),
    units: str = Query("metric", description="Units (metric/imperial/kelvin)"),
    lang: str = Query("pt_br", description="Language")
):
   
    request = WeatherRequest(
        city=city,
        lat=lat,
        lon=lon,
        units=units,
        lang=lang
    )
    
    return await weather_controller.get_current(request)


@router.get("/forecast", response_model=SuccessResponse)
async def weather_forecast(
    city: Optional[str] = Query(None, description="City name"),
    lat: Optional[float] = Query(None, description="Latitude"),
    lon: Optional[float] = Query(None, description="Longitude"),
    days: int = Query(5, ge=1, le=5, description="Forecast days (1-5)"),
    units: str = Query("metric", description="Units"),
    lang: str = Query("pt_br", description="Language")
):
   
    request = WeatherRequest(
        city=city,
        lat=lat,
        lon=lon,
        units=units,
        lang=lang
    )
    
    return await weather_controller.get_forecast(request, days)


@router.get("/health")
async def weather_health():
    """Weather service health check"""
    return {
        "service": "weather",
        "status": "healthy",
        "provider": "OpenWeatherMap"
    }
