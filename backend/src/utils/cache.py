import json
import logging
from typing import Any, Optional, Union
from functools import wraps

from src.core.config import get_redis_client
from src.core.settings import settings


logger = logging.getLogger(__name__)


class CacheManager:
    
    @staticmethod
    async def get(key: str) -> Optional[Any]:
        if not settings.cache_enabled:
            return None
            
        redis_client = get_redis_client()
        if not redis_client:
            return None
            
        try:
            value = await redis_client.get(key)
            if value:
                return json.loads(value)
        except Exception as e:
            logger.warning(f"Erro ao recuperar do cache {key}: {e}")
        
        return None
    
    @staticmethod
    async def set(
        key: str, 
        value: Any, 
        ttl: Optional[int] = None
    ) -> bool:
        if not settings.cache_enabled:
            return False
            
        redis_client = get_redis_client()
        if not redis_client:
            return False
            
        try:
            ttl = ttl or settings.cache_ttl
            serialized_value = json.dumps(value, default=str)
            
            if ttl > 0:
                await redis_client.setex(key, ttl, serialized_value)
            else:
                await redis_client.set(key, serialized_value)
                
            logger.debug(f"Valor salvo no cache: {key} (TTL: {ttl}s)")
            return True
            
        except Exception as e:
            logger.warning(f"Erro ao salvar no cache {key}: {e}")
            return False
    
    @staticmethod
    async def delete(key: str) -> bool:
        if not settings.cache_enabled:
            return False
            
        redis_client = get_redis_client()
        if not redis_client:
            return False
            
        try:
            result = await redis_client.delete(key)
            logger.debug(f"Chave removida do cache: {key}")
            return bool(result)
        except Exception as e:
            logger.warning(f"Erro ao remover do cache {key}: {e}")
            return False
    
    @staticmethod
    async def exists(key: str) -> bool:
        if not settings.cache_enabled:
            return False
            
        redis_client = get_redis_client()
        if not redis_client:
            return False
            
        try:
            result = await redis_client.exists(key)
            return bool(result)
        except Exception as e:
            logger.warning(f"Erro ao verificar existência no cache {key}: {e}")
            return False
    
    @staticmethod
    async def clear_pattern(pattern: str) -> int:
        if not settings.cache_enabled:
            return 0
            
        redis_client = get_redis_client()
        if not redis_client:
            return 0
            
        try:
            keys = await redis_client.keys(pattern)
            if keys:
                result = await redis_client.delete(*keys)
                logger.info(f"Removidas {result} chaves do padrão: {pattern}")
                return result
            return 0
        except Exception as e:
            logger.warning(f"Erro ao limpar padrão do cache {pattern}: {e}")
            return 0


def cached(
    ttl: Optional[int] = None,
    key_prefix: str = "",
    use_args: bool = True,
    use_kwargs: bool = True
):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not settings.cache_enabled:
                return await func(*args, **kwargs)
            
            key_parts = [key_prefix or func.__name__]
            
            if use_args and args:
                key_parts.extend([str(arg) for arg in args])
                
            if use_kwargs and kwargs:
                key_parts.extend([f"{k}:{v}" for k, v in sorted(kwargs.items())])
                
            cache_key = ":".join(key_parts)

            cached_result = await CacheManager.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit para função {func.__name__}: {cache_key}")
                return cached_result
            result = await func(*args, **kwargs)
            
            if result is not None:
                await CacheManager.set(cache_key, result, ttl)
                logger.debug(f"Resultado cacheado para função {func.__name__}: {cache_key}")
            
            return result
            
        return wrapper
    return decorator

class RateLimiter:
    
    @staticmethod
    async def is_allowed(
        identifier: str,
        max_requests: int = None,
        window_seconds: int = None
    ) -> tuple[bool, dict]:

        if not settings.rate_limit_enabled:
            return True, {"remaining": float("inf")}
            
        max_requests = max_requests or settings.rate_limit_requests
        window_seconds = window_seconds or settings.rate_limit_window
        
        redis_client = get_redis_client()
        if not redis_client:
            return True, {"remaining": max_requests}
            
        try:
            key = f"rate_limit:{identifier}"
            
            current_time = int(time.time())
            window_start = current_time - window_seconds

            await redis_client.zremrangebyscore(key, 0, window_start)
            

            current_requests = await redis_client.zcard(key)
            
            if current_requests >= max_requests:
                return False, {
                    "remaining": 0,
                    "reset_time": current_time + window_seconds
                }
            
            await redis_client.zadd(key, {str(current_time): current_time})
            await redis_client.expire(key, window_seconds)
            
            remaining = max_requests - current_requests - 1
            
            return True, {
                "remaining": remaining,
                "reset_time": current_time + window_seconds
            }
            
        except Exception as e:
            logger.warning(f"Erro no rate limiting: {e}")
            return True, {"remaining": max_requests}

import time
