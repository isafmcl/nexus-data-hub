import json
import logging
import time
from datetime import datetime
from typing import Any, Dict, Optional
from functools import wraps

from src.core.settings import settings


class StructuredLogger:
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
    
    def _log_with_context(
        self,
        level: int,
        message: str,
        extra_context: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        filtered_kwargs = {k: v for k, v in kwargs.items() if v is not None}
        
        context = {
            "timestamp": datetime.utcnow().isoformat(),
            "logger_name": self.logger.name,
            **(extra_context or {}),
            **filtered_kwargs
        }
        

        self.logger.log(level, message, extra=context)
    
    def info(self, message: str, **context):
        self._log_with_context(logging.INFO, message, context)
    
    def warning(self, message: str, **context):
        self._log_with_context(logging.WARNING, message, context)
    
    def error(self, message: str, **context):
        self._log_with_context(logging.ERROR, message, context)
    
    def debug(self, message: str, **context):
        self._log_with_context(logging.DEBUG, message, context)
    
    def api_call(
        self,
        api_name: str,
        endpoint: str,
        method: str,
        status_code: int,
        response_time: float,
        cached: bool = False,
        **extra_context
    ):
        """Log específico para chamadas de API"""
        context = {
            "api_name": api_name,
            "endpoint": endpoint,
            "http_method": method,
            "status_code": status_code,
            "response_time_ms": round(response_time * 1000, 2),
            "cached": cached,
            "log_type": "api_call",
            **extra_context
        }
        
        if status_code >= 400:
            self.error(f"API call failed: {api_name}", **context)
        else:
            self.info(f"API call success: {api_name}", **context)
    
    def user_action(
        self,
        action: str,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        **extra_context
    ):
        """Log específico para ações do usuário"""
        context = {
            "action": action,
            "user_id": user_id,
            "ip_address": ip_address,
            "log_type": "user_action",
            **extra_context
        }
        
        self.info(f"User action: {action}", **context)


def log_execution_time(logger: Optional[StructuredLogger] = None):
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            func_logger = logger or StructuredLogger(func.__module__)
            
            try:
                result = await func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                func_logger.debug(
                    f"Function executed successfully: {func.__name__}",
                    execution_time_ms=round(execution_time * 1000, 2),
                    function_name=func.__name__,
                    log_type="function_execution"
                )
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                
                func_logger.error(
                    f"Function failed: {func.__name__}",
                    execution_time_ms=round(execution_time * 1000, 2),
                    function_name=func.__name__,
                    error_type=type(e).__name__,
                    error_message=str(e),
                    log_type="function_execution"
                )
                
                raise
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            func_logger = logger or StructuredLogger(func.__module__)
            
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                func_logger.debug(
                    f"Function executed successfully: {func.__name__}",
                    execution_time_ms=round(execution_time * 1000, 2),
                    function_name=func.__name__,
                    log_type="function_execution"
                )
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                
                func_logger.error(
                    f"Function failed: {func.__name__}",
                    execution_time_ms=round(execution_time * 1000, 2),
                    function_name=func.__name__,
                    error_type=type(e).__name__,
                    error_message=str(e),
                    log_type="function_execution"
                )
                
                raise
        
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


class APIMetricsLogger:
    
    def __init__(self):
        self.logger = StructuredLogger("api_metrics")
    
    async def log_api_metrics(
        self,
        api_name: str,
        endpoint: str,
        method: str,
        status_code: int,
        response_time: float,
        data_size: Optional[int] = None,
        cached: bool = False,
        error_message: Optional[str] = None
    ):
        
        metrics = {
            "api_name": api_name,
            "endpoint": endpoint,
            "method": method,
            "status_code": status_code,
            "response_time_ms": round(response_time * 1000, 2),
            "data_size_bytes": data_size,
            "cached": cached,
            "success": status_code < 400,
            "log_type": "api_metrics"
        }
        
        if error_message:
            metrics["error_message"] = error_message
        
        if status_code >= 400:
            self.logger.error(f"API Error: {api_name} {endpoint}", **metrics)
        else:
            self.logger.info(f"API Success: {api_name} {endpoint}", **metrics)

api_metrics_logger = APIMetricsLogger()


def get_logger(name: str) -> StructuredLogger:
    return StructuredLogger(name)
