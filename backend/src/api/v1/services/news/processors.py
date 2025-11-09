"""
News Data Processors
Processadores de dados de notícias para normalização
"""
from typing import Dict, Any, List
from datetime import datetime


class NewsDataProcessor:
    """Processa e normaliza dados de notícias"""
    
    @staticmethod
    def process_article(article: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa um único artigo
        
        Args:
            article: Dados brutos do artigo
            
        Returns:
            Artigo processado e normalizado
        """
        return {
            "title": article.get("title", "Sem título"),
            "description": article.get("description", ""),
            "content": article.get("content", ""),
            "url": article.get("url", ""),
            "image": article.get("urlToImage", ""),
            "published_at": article.get("publishedAt", ""),
            "source": {
                "id": article.get("source", {}).get("id"),
                "name": article.get("source", {}).get("name", "Desconhecido")
            },
            "author": article.get("author", "Desconhecido")
        }
    
    @staticmethod
    def process_articles(articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Processa lista de artigos
        
        Args:
            articles: Lista de artigos brutos
            
        Returns:
            Lista de artigos processados
        """
        return [
            NewsDataProcessor.process_article(article) 
            for article in articles
        ]
    
    @staticmethod
    def calculate_statistics(articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calcula estatísticas dos artigos
        
        Args:
            articles: Lista de artigos processados
            
        Returns:
            Estatísticas calculadas
        """
        sources = {}
        for article in articles:
            source_name = article.get("source", {}).get("name", "Desconhecido")
            sources[source_name] = sources.get(source_name, 0) + 1
        
        return {
            "total_articles": len(articles),
            "sources_count": len(sources),
            "top_sources": sorted(
                sources.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:5]
        }
    
    @staticmethod
    def filter_articles(
        articles: List[Dict[str, Any]], 
        filters: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Filtra artigos baseado em critérios
        
        Args:
            articles: Lista de artigos
            filters: Filtros a aplicar
            
        Returns:
            Artigos filtrados
        """
        filtered = articles
        
        # Filtro por fonte
        if "source" in filters:
            filtered = [
                a for a in filtered 
                if a.get("source", {}).get("name") == filters["source"]
            ]
        
        # Filtro por palavra-chave no título
        if "keyword" in filters:
            keyword = filters["keyword"].lower()
            filtered = [
                a for a in filtered 
                if keyword in a.get("title", "").lower()
            ]
        
        return filtered
