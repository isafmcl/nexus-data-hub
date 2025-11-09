from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from ..services.openlibrary_service import openlibrary_service

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/search")
async def search_books(
    q: str = Query(..., description="Termo de busca (título, autor, etc.)"),
    limit: int = Query(20, ge=1, le=100, description="Número de resultados por página"),
    offset: int = Query(0, ge=0, description="Deslocamento para paginação"),
    fields: Optional[str] = Query(None, description="Campos específicos separados por vírgula")
):
    try:

        fields_list = None
        if fields:
            fields_list = [field.strip() for field in fields.split(",")]
        
        result = await openlibrary_service.search_books(
            query=q,
            limit=limit,
            offset=offset,
            fields=fields_list
        )
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result.get("error", "Erro na busca"))
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.get("/details/{book_key:path}")
async def get_book_details(book_key: str):
    try:
        result = await openlibrary_service.get_book_details(book_key)
        
        if not result["success"]:
            raise HTTPException(status_code=404, detail=result.get("error", "Livro não encontrado"))
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.get("/search/autocomplete")
async def autocomplete_books(
    q: str = Query(..., min_length=2, description="Termo para autocompletar"),
    limit: int = Query(10, ge=1, le=20, description="Número de sugestões")
):
    try:
        result = await openlibrary_service.search_books(
            query=q,
            limit=limit,
            fields=["title", "author_name", "key", "cover_i"]
        )
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result.get("error", "Erro na busca"))
        
        suggestions = []
        for book in result.get("books", []):
            suggestions.append({
                "title": book["title"],
                "author": book.get("author_name", [])[:2], 
                "key": book["key"],
                "cover_url": book.get("cover_url")
            })
        
        return {
            "success": True,
            "suggestions": suggestions,
            "query": q
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
