from fastapi import APIRouter

from .routers.weather import router as weather_router
from .routers.news import router as news_router
from .routers.countries import router as countries_router
from .routers.cep import router as cep_router
from .routers.books import router as books_router
from .routers.worldbank import router as worldbank_router


api_router = APIRouter()

api_router.include_router(weather_router)
api_router.include_router(news_router)
api_router.include_router(countries_router)
api_router.include_router(cep_router)
api_router.include_router(books_router)
api_router.include_router(worldbank_router)


@api_router.get("/")
async def api_root():
    return {
        "message": "Nexus Data Hub API",
        "version": "1.0.0", 
        "description": "Plataforma Inteligente de Integração de APIs Públicas",
        "active_endpoints": [
            "/weather - Previsão do tempo (OpenWeather)",
            "/news - Notícias globais (NewsAPI)",
            "/countries - Informações de países (REST Countries)",
            "/cep - CEPs brasileiros (ViaCEP)",
            "/books - Busca de livros (OpenLibrary)",
            "/worldbank - Dados econômicos (World Bank)"
        ],
        "total_apis": 6,
        "auth_required": 2,
        "public_apis": 4
    }


@api_router.get("/health")
async def api_health():
    return {
        "status": "healthy",
        "timestamp": "2025-11-08T20:40:00Z",
        "total_services": 6,
        "services": [
            {"name": "weather", "provider": "OpenWeather", "auth_required": True, "status": "active"},
            {"name": "news", "provider": "NewsAPI", "auth_required": True, "status": "active"},
            {"name": "countries", "provider": "REST Countries", "auth_required": False, "status": "active"},
            {"name": "cep", "provider": "ViaCEP", "auth_required": False, "status": "active"},
            {"name": "books", "provider": "OpenLibrary", "auth_required": False, "status": "active"},
            {"name": "worldbank", "provider": "World Bank", "auth_required": False, "status": "active"}
        ]
    }
