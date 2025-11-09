from typing import Dict, Any, List
from datetime import datetime, date
from src.api.v1.schemas.weather import CurrentWeatherData


class WeatherDataProcessor:

    
    @staticmethod
    def process_current_weather(weather_data: CurrentWeatherData) -> Dict[str, Any]:
        """Processa dados de clima atual"""
        return {
            "raw_data": weather_data.dict(),
            "processed": {
                "location": {
                    "city": weather_data.name,
                    "country": weather_data.sys.country,
                    "coordinates": {
                        "lat": weather_data.coord.lat,
                        "lon": weather_data.coord.lon
                    }
                },
                "current": {
                    "temperature": weather_data.main.temp,
                    "feels_like": weather_data.main.feels_like,
                    "humidity": weather_data.main.humidity,
                    "pressure": weather_data.main.pressure,
                    "description": weather_data.weather[0].description,
                    "icon": weather_data.weather[0].icon
                },
                "wind": {
                    "speed": weather_data.wind.speed if weather_data.wind else None,
                    "direction": weather_data.wind.deg if weather_data.wind else None
                } if weather_data.wind else None,
                "clouds": {
                    "coverage": weather_data.clouds.all
                },
                "visibility": weather_data.visibility,
                "timestamp": weather_data.dt
            }
        }
    
    @staticmethod
    def process_forecast(forecast_data: Dict[str, Any], days: int = 5) -> Dict[str, Any]:
        processed_forecast = {
            "location": {
                "city": forecast_data["city"]["name"],
                "country": forecast_data["city"]["country"],
                "coordinates": {
                    "lat": forecast_data["city"]["coord"]["lat"],
                    "lon": forecast_data["city"]["coord"]["lon"]
                }
            },
            "forecast": []
        }

        forecasts_by_date = {}
        
        for item in forecast_data["list"][:days * 8]:
            forecast_date = date.fromtimestamp(item["dt"])
            
            if forecast_date not in forecasts_by_date:
                forecasts_by_date[forecast_date] = []
            
            forecasts_by_date[forecast_date].append({
                "datetime": datetime.fromtimestamp(item["dt"]).isoformat(),
                "temperature": {
                    "temp": item["main"]["temp"],
                    "feels_like": item["main"]["feels_like"],
                    "temp_min": item["main"]["temp_min"],
                    "temp_max": item["main"]["temp_max"]
                },
                "weather": {
                    "main": item["weather"][0]["main"],
                    "description": item["weather"][0]["description"],
                    "icon": item["weather"][0]["icon"]
                },
                "humidity": item["main"]["humidity"],
                "pressure": item["main"]["pressure"],
                "wind": {
                    "speed": item["wind"]["speed"],
                    "deg": item["wind"].get("deg")
                } if "wind" in item else None,
                "clouds": item["clouds"]["all"],
                "precipitation": item.get("rain", {}).get("3h", 0) + item.get("snow", {}).get("3h", 0)
            })
        
        for forecast_date in sorted(forecasts_by_date.keys()):
            processed_forecast["forecast"].append({
                "date": forecast_date.isoformat(),
                "periods": forecasts_by_date[forecast_date]
            })
        
        return processed_forecast
