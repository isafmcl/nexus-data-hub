from datetime import datetime
from typing import Any, Dict, Optional, List
from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    success: bool = Field(description="Indica se a requisição foi bem-sucedida")
    message: str = Field(description="Mensagem descritiva")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp da resposta")


class ErrorResponse(BaseResponse):
    success: bool = Field(default=False)
    error_code: Optional[str] = Field(None, description="Código do erro")
    details: Optional[Dict[str, Any]] = Field(None, description="Detalhes adicionais do erro")


class SuccessResponse(BaseResponse):
    success: bool = Field(default=True)
    data: Optional[Dict[str, Any]] = Field(None, description="Dados da resposta")


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1, description="Número da página")
    limit: int = Field(default=10, ge=1, le=100, description="Limite de itens por página")


class PaginatedResponse(SuccessResponse):
    data: List[Dict[str, Any]] = Field(description="Lista de itens")
    pagination: Dict[str, Any] = Field(description="Informações de paginação")


class CacheInfo(BaseModel):
    cached: bool = Field(description="Se os dados vieram do cache")
    cache_key: Optional[str] = Field(None, description="Chave do cache")
    ttl: Optional[int] = Field(None, description="Time to live em segundos")


class APIMetrics(BaseModel):
    api_name: str = Field(description="Nome da API")
    response_time: float = Field(description="Tempo de resposta em segundos")
    status_code: int = Field(description="Status code da resposta")
    cached: bool = Field(description="Se a resposta veio do cache")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
