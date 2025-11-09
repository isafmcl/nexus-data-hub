from fastapi import APIRouter, Query, HTTPException
from typing import Optional

from src.api.v1.services.countries import countries_service
from src.api.v1.schemas.base import SuccessResponse

router = APIRouter(prefix="/countries", tags=["Countries"])


@router.get("/", response_model=SuccessResponse)
async def list_countries():
    try:
        return await countries_service.get_all_countries()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search/{name}", response_model=SuccessResponse)
async def get_country(name: str):
    try:
        return await countries_service.get_country_by_name(name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/region/{region}", response_model=SuccessResponse)
async def get_countries_by_region(region: str):
    try:
        return await countries_service.get_countries_by_region(region)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def countries_health():
    return {
        "service": "countries",
        "status": "healthy",
        "provider": "REST Countries"
    }
