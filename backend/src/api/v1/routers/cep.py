from fastapi import APIRouter, Query, HTTPException, Path
from ..services.viacep_service import viacep_service

router = APIRouter(prefix="/cep", tags=["CEP & Exchange"])


@router.get("/{cep}")
async def get_address_by_cep(
    cep: str = Path(..., description="CEP para consultar (formato: 12345678 ou 12345-678)")
):

    try:
        result = await viacep_service.get_address_by_cep(cep)
        
        if not result["success"]:
            if "não encontrado" in result.get("error", "").lower():
                raise HTTPException(status_code=404, detail=result["error"])
            else:
                raise HTTPException(status_code=400, detail=result["error"])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.get("/search/{state}/{city}/{street}")
async def search_addresses_by_location(
    state: str = Path(..., description="UF do estado (ex: SP, RJ, RS)"),
    city: str = Path(..., description="Nome da cidade"),
    street: str = Path(..., description="Nome da rua/logradouro")
):
    try:
        result = await viacep_service.search_addresses_by_location(
            state=state,
            city=city,
            street=street
        )
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.get("/validate/{cep}")
async def validate_cep(
    cep: str = Path(..., description="CEP para validar")
):
    try:
        import re
        
        clean_cep = re.sub(r'\D', '', cep)
        
        is_valid = len(clean_cep) == 8
        
        return {
            "success": True,
            "cep": cep,
            "clean_cep": clean_cep,
            "is_valid": is_valid,
            "formatted_cep": f"{clean_cep[:5]}-{clean_cep[5:]}" if is_valid else None,
            "message": "CEP válido" if is_valid else "CEP inválido - deve conter 8 dígitos"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.get("/health")
async def cep_health():
    """CEP service health check"""
    return {
        "service": "cep_service",
        "status": "healthy",
        "providers": ["ViaCEP"],
        "endpoints": [
            "/cep/{cep}",
            "/cep/search/{state}/{city}/{street}",
            "/cep/validate/{cep}"
        ]
    }
