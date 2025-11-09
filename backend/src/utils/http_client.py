import asyncio
import time
import logging
from typing import Dict, Any, Optional, Union
from contextlib import asynccontextmanager

import httpx
from src.core.config import get_redis_client
from src.core.settings import settings
import json
import hashlib


logger = logging.getLogger(__name__)


class HTTPClient:
    def __init__(self):
        self.client: Optional[httpx.AsyncClient] = None
        self._timeout = httpx.Timeout(timeout=settings.http_timeout)
        
    async def __aenter__(self):
        """Entrada do context manager"""
        self.client = httpx.AsyncClient(
            timeout=self._timeout,
            follow_redirects=True,
            limits=httpx.Limits(
                max_keepalive_connections=20,
                max_connections=100,
                keepalive_expiry=30.0
            )
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()
    
    def _generate_cache_key(
        self, 
        method: str, 
        url: str, 
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> str:
        cache_data = {
            "method": method,
            "url": url,
            "params": params or {},
            # Incluir apenas headers relevantes para cache
            "auth_headers": {k: v for k, v in (headers or {}).items() 
                           if k.lower() in ['authorization', 'x-api-key', 'x-auth-token']}
        }
        cache_string = json.dumps(cache_data, sort_keys=True)
        return f"http_cache:{hashlib.md5(cache_string.encode()).hexdigest()}"
    
    async def _get_from_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        if not settings.cache_enabled:
            return None
            
        redis_client = get_redis_client()
        if not redis_client:
            return None
            
        try:
            cached_data = await redis_client.get(cache_key)
            if cached_data:
                logger.debug(f"Cache hit para chave: {cache_key}")
                return json.loads(cached_data)
        except Exception as e:
            logger.warning(f"Erro ao acessar cache: {e}")
            
        return None
    
    async def _save_to_cache(
        self, 
        cache_key: str, 
        data: Dict[str, Any], 
        ttl: Optional[int] = None
    ) -> None:
        if not settings.cache_enabled:
            return
            
        redis_client = get_redis_client()
        if not redis_client:
            return
            
        try:
            ttl = ttl or settings.cache_ttl
            await redis_client.setex(
                cache_key, 
                ttl, 
                json.dumps(data, default=str)
            )
            logger.debug(f"Dados salvos no cache com TTL {ttl}s: {cache_key}")
        except Exception as e:
            logger.warning(f"Erro ao salvar no cache: {e}")
    
    async def _make_request_with_retry(
        self,
        method: str,
        url: str,
        **kwargs
    ) -> httpx.Response:
        last_exception = None
        
        for attempt in range(settings.max_retries + 1):
            try:
                response = await self.client.request(method, url, **kwargs)
                
                logger.info(
                    f"{method.upper()} {url} - {response.status_code} "
                    f"({len(response.content)} bytes)"
                )
                
                if response.status_code >= 400:
                    response.raise_for_status()
                    
                return response
                
            except (httpx.RequestError, httpx.HTTPStatusError) as e:
                last_exception = e
                
                if attempt < settings.max_retries:
                    wait_time = 2 ** attempt  
                    logger.warning(
                        f"Tentativa {attempt + 1} falhou para {method} {url}. "
                        f"Tentando novamente em {wait_time}s. Erro: {e}"
                    )
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(
                        f"Todas as {settings.max_retries + 1} tentativas falharam "
                        f"para {method} {url}. Último erro: {e}"
                    )
                    
        raise last_exception
    
    async def request(
        self,
        method: str,
        url: str,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        cache_ttl: Optional[int] = None,
        use_cache: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        start_time = time.time()
        cache_key = self._generate_cache_key(method, url, params, headers)
        if method.upper() == "GET" and use_cache:
            cached_response = await self._get_from_cache(cache_key)
            if cached_response:
                response_time = time.time() - start_time
                return {
                    **cached_response,
                    "cache_info": {
                        "cached": True,
                        "cache_key": cache_key,
                        "response_time": response_time
                    }
                }

        try:
            kwargs_for_request = kwargs.copy()
            if json_data:
                kwargs_for_request["json"] = json_data
            if params:
                kwargs_for_request["params"] = params
            if headers:
                kwargs_for_request["headers"] = headers
                
            response = await self._make_request_with_retry(
                method, url, **kwargs_for_request
            )
            
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                response_data = {"content": response.text}
            
            result = {
                "status_code": response.status_code,
                "data": response_data,
                "headers": dict(response.headers),
                "url": str(response.url),
                "cache_info": {
                    "cached": False,
                    "cache_key": cache_key,
                    "response_time": time.time() - start_time
                }
            }
            
            if (method.upper() == "GET" and 
                use_cache and 
                200 <= response.status_code < 300):
                await self._save_to_cache(cache_key, result, cache_ttl)
                
            return result
            
        except Exception as e:
            response_time = time.time() - start_time
            logger.error(f"Erro na requisição {method} {url}: {e}")
            
            raise HTTPException(
                status_code=503,
                detail={
                    "message": f"Erro ao acessar API externa: {str(e)}",
                    "url": url,
                    "response_time": response_time
                }
            )

@asynccontextmanager
async def http_client():
    """Context manager para cliente HTTP"""
    async with HTTPClient() as client:
        yield client

 
async def quick_request(
    method: str,
    url: str, 
    **kwargs
) -> Dict[str, Any]:
    async with http_client() as client:
        return await client.request(method, url, **kwargs)

try:
    from fastapi import HTTPException
except ImportError:
    class HTTPException(Exception):
        def __init__(self, status_code: int, detail: Union[str, Dict]):
            self.status_code = status_code
            self.detail = detail
            super().__init__(detail)
