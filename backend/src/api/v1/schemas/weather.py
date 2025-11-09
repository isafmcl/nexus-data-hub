from typing import List, Optional
from pydantic import BaseModel, Field


class WeatherCondition(BaseModel):
    id: int = Field(description="ID da condição")
    main: str = Field(description="Grupo principal (Rain, Snow, Clear, etc.)")
    description: str = Field(description="Descrição detalhada")
    icon: str = Field(description="ID do ícone")


class WeatherMain(BaseModel):
    temp: float = Field(description="Temperatura atual em Celsius")
    feels_like: float = Field(description="Sensação térmica em Celsius")
    temp_min: float = Field(description="Temperatura mínima em Celsius")
    temp_max: float = Field(description="Temperatura máxima em Celsius")
    pressure: int = Field(description="Pressão atmosférica em hPa")
    humidity: int = Field(description="Umidade em %")
    sea_level: Optional[int] = Field(None, description="Pressão ao nível do mar em hPa")
    grnd_level: Optional[int] = Field(None, description="Pressão ao nível do solo em hPa")


class WeatherWind(BaseModel):
    speed: float = Field(description="Velocidade do vento em m/s")
    deg: Optional[int] = Field(None, description="Direção do vento em graus")
    gust: Optional[float] = Field(None, description="Rajadas em m/s")


class WeatherClouds(BaseModel):
    all: int = Field(description="Nebulosidade em %")


class WeatherRain(BaseModel):
    one_hour: Optional[float] = Field(None, alias="1h", description="Volume de chuva na última 1h em mm")
    three_hours: Optional[float] = Field(None, alias="3h", description="Volume de chuva nas últimas 3h em mm")


class WeatherSnow(BaseModel):
    one_hour: Optional[float] = Field(None, alias="1h", description="Volume de neve na última 1h em mm")
    three_hours: Optional[float] = Field(None, alias="3h", description="Volume de neve nas últimas 3h em mm")


class WeatherSys(BaseModel):
    type: Optional[int] = Field(None, description="Tipo interno")
    id: Optional[int] = Field(None, description="ID interno")
    country: str = Field(description="Código do país")
    sunrise: int = Field(description="Timestamp do nascer do sol")
    sunset: int = Field(description="Timestamp do pôr do sol")


class WeatherCoord(BaseModel):
    lon: float = Field(description="Longitude")
    lat: float = Field(description="Latitude")


class CurrentWeatherData(BaseModel):
    coord: WeatherCoord = Field(description="Coordenadas")
    weather: List[WeatherCondition] = Field(description="Condições climáticas")
    base: str = Field(description="Tipo de estação")
    main: WeatherMain = Field(description="Dados principais")
    visibility: Optional[int] = Field(None, description="Visibilidade em metros")
    wind: Optional[WeatherWind] = Field(None, description="Informações do vento")
    clouds: WeatherClouds = Field(description="Informações das nuvens")
    rain: Optional[WeatherRain] = Field(None, description="Informações de chuva")
    snow: Optional[WeatherSnow] = Field(None, description="Informações de neve")
    dt: int = Field(description="Timestamp dos dados")
    sys: WeatherSys = Field(description="Informações do sistema")
    timezone: int = Field(description="Fuso horário em segundos UTC")
    id: int = Field(description="ID da cidade")
    name: str = Field(description="Nome da cidade")
    cod: int = Field(description="Código de resposta")


class WeatherRequest(BaseModel):
    """Parâmetros para requisição de clima"""
    city: Optional[str] = Field(None, description="Nome da cidade")
    lat: Optional[float] = Field(None, description="Latitude")
    lon: Optional[float] = Field(None, description="Longitude")
    units: str = Field(default="metric", description="Unidades (metric, imperial, kelvin)")
    lang: str = Field(default="pt_br", description="Idioma da resposta")
    
    class Config:
        json_schema_extra = {
            "example": {
                "city": "São Paulo",
                "units": "metric",
                "lang": "pt_br"
            }
        }
