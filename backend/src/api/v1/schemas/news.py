from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl


class NewsSource(BaseModel):
    id: Optional[str] = Field(None, description="ID da fonte")
    name: str = Field(description="Nome da fonte")


class NewsArticle(BaseModel):
    source: NewsSource = Field(description="Fonte da notícia")
    author: Optional[str] = Field(None, description="Autor do artigo")
    title: str = Field(description="Título da notícia")
    description: Optional[str] = Field(None, description="Descrição/resumo")
    url: HttpUrl = Field(description="URL completa do artigo")
    url_to_image: Optional[HttpUrl] = Field(None, alias="urlToImage", description="URL da imagem de capa")
    published_at: datetime = Field(alias="publishedAt", description="Data/hora de publicação")
    content: Optional[str] = Field(None, description="Conteúdo parcial do artigo")
    
    class Config:
        populate_by_name = True


class NewsResponse(BaseModel):
    status: str = Field(description="Status da resposta")
    total_results: int = Field(alias="totalResults", description="Total de resultados encontrados")
    articles: List[NewsArticle] = Field(description="Lista de artigos")
    
    class Config:
        populate_by_name = True


class NewsRequest(BaseModel):
    query: Optional[str] = Field(None, description="Termo de busca")
    category: Optional[str] = Field(
        None, 
        description="Categoria",
        pattern="^(business|entertainment|general|health|science|sports|technology)$"
    )
    country: str = Field(default="br", description="Código do país")
    language: str = Field(default="pt", description="Idioma")
    page_size: int = Field(default=10, ge=1, le=100, description="Número de artigos por página")
    page: int = Field(default=1, ge=1, description="Número da página")
    sort_by: str = Field(
        default="publishedAt", 
        description="Ordenação",
        pattern="^(relevancy|popularity|publishedAt)$"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "tecnologia",
                "category": "technology",
                "country": "br",
                "language": "pt",
                "page_size": 10,
                "page": 1,
                "sort_by": "publishedAt"
            }
        }
