import logging
import sys
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import redis.asyncio as redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from .settings import settings



def setup_logging():
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
 
    if settings.log_format.lower() == "json":
        import json
        import datetime
        
        class JSONFormatter(logging.Formatter):
            def format(self, record):
                log_entry = {
                    "timestamp": datetime.datetime.utcnow().isoformat(),
                    "level": record.levelname,
                    "message": record.getMessage(),
                    "module": record.module,
                    "function": record.funcName,
                    "line": record.lineno,
                }
                
                if hasattr(record, "request_id"):
                    log_entry["request_id"] = record.request_id
                    
                if hasattr(record, "user_id"):
                    log_entry["user_id"] = record.user_id
                    
                return json.dumps(log_entry)
        
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
 
    logging.basicConfig(
        level=log_level,
        handlers=[handler],
        force=True
    )
    
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)

redis_client: redis.Redis = None


async def init_redis():
    global redis_client
    
    try:
        redis_client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            password=settings.redis_password,
            db=settings.redis_db,
            decode_responses=True,
            socket_timeout=5,
            socket_connect_timeout=5,
            health_check_interval=30,
        )
        await redis_client.ping()
        logging.info(f"Redis conectado em {settings.redis_host}:{settings.redis_port}")
        
    except Exception as e:
        logging.error(f"Erro ao conectar com Redis: {e}")
        redis_client = None


async def close_redis():
    global redis_client
    if redis_client:
        await redis_client.aclose()
        logging.info("Redis conexão fechada")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    setup_logging()
    logging.info("Iniciando Nexus Data Hub...")
    
    if settings.cache_enabled:
        await init_redis()
    
    logging.info("Aplicação iniciada com sucesso!")
    
    yield
    
    # Shutdown
    logging.info("Encerrando aplicação...")
    
    if settings.cache_enabled:
        await close_redis()
    
    logging.info(" Aplicação encerrada com sucesso!")


def create_app() -> FastAPI:
    
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=" Plataforma Inteligente de Integração de APIs Públicas",
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        openapi_url="/openapi.json" if settings.debug else None,
        lifespan=lifespan
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"] if settings.debug else ["localhost", "127.0.0.1"]
    )
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        logging.error(f"Erro não tratado: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": "Erro interno do servidor",
                "message": "Ocorreu um erro inesperado"
            }
        )
    
    @app.get("/health", tags=["Health"])
    async def health_check():
 
        health_status = {
            "status": "healthy",
            "version": settings.app_version,
            "environment": settings.environment,
            "redis": "disconnected"
        }
        
        if settings.cache_enabled and redis_client:
            try:
                await redis_client.ping()
                health_status["redis"] = "connected"
            except Exception:
                health_status["redis"] = "error"
        
        return health_status
    

    @app.get("/info", tags=["Info"])
    async def app_info():
        return {
            "name": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
            "features": {
                "cache": settings.cache_enabled,
                "rate_limiting": settings.rate_limit_enabled,
                "debug": settings.debug
            },
            "available_apis": list(settings.api_endpoints.keys())
        }
    
    return app

def get_redis_client() -> redis.Redis:
    return redis_client
