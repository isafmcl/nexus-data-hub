from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from ..services.worldbank_service import worldbank_service

router = APIRouter(prefix="/worldbank", tags=["World Bank"])


@router.get("/countries")
async def get_countries(
    per_page: int = Query(100, ge=10, le=500, description="Países por página")
):
    try:
        result = await worldbank_service.get_countries(per_page=per_page)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result.get("error", "Erro ao buscar países"))
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.get("/indicator/{country_code}/{indicator}")
async def get_economic_indicator(
    country_code: str,
    indicator: str,
    start_year: Optional[int] = Query(None, ge=1960, le=2025, description="Ano inicial"),
    end_year: Optional[int] = Query(None, ge=1960, le=2025, description="Ano final")
):
    try:
        if start_year and end_year and start_year > end_year:
            raise HTTPException(status_code=400, detail="Ano inicial não pode ser maior que ano final")
        
        result = await worldbank_service.get_economic_indicator(
            country_code=country_code.lower(),
            indicator=indicator,
            start_year=start_year,
            end_year=end_year
        )
        
        if not result["success"]:
            raise HTTPException(status_code=404, detail=result.get("error", "Indicador não encontrado"))
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.get("/indicators/common")
async def get_common_indicators():
    return {
        "success": True,
        "indicators": [
            {
                "code": "NY.GDP.MKTP.CD",
                "name": "PIB (US$ correntes)",
                "description": "Produto Interno Bruto em dólares americanos correntes"
            },
            {
                "code": "NY.GDP.PCAP.CD", 
                "name": "PIB per capita (US$ correntes)",
                "description": "PIB per capita em dólares americanos correntes"
            },
            {
                "code": "SP.POP.TOTL",
                "name": "População total",
                "description": "População total do país"
            },
            {
                "code": "SL.UEM.TOTL.ZS",
                "name": "Taxa de desemprego (%)",
                "description": "Taxa de desemprego como percentual da força de trabalho"
            },
            {
                "code": "FP.CPI.TOTL.ZG",
                "name": "Inflação (CPI %)",
                "description": "Inflação medida pelo índice de preços ao consumidor"
            },
            {
                "code": "NE.EXP.GNFS.ZS",
                "name": "Exportações (% do PIB)",
                "description": "Exportações de bens e serviços como % do PIB"
            },
            {
                "code": "NE.IMP.GNFS.ZS", 
                "name": "Importações (% do PIB)",
                "description": "Importações de bens e serviços como % do PIB"
            },
            {
                "code": "SE.ADT.LITR.ZS",
                "name": "Taxa de alfabetização (%)",
                "description": "Taxa de alfabetização de adultos"
            }
        ]
    }
