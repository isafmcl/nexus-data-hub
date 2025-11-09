from typing import Dict, Any, List, Optional
from src.utils.http_client import http_client
from src.utils.cache import cached
from src.core.settings import settings
from src.utils.logger import get_logger
import urllib.parse


class OpenLibraryService:
    
    def __init__(self):
        self.base_url = settings.api_endpoints["openlibrary"]
        self.logger = get_logger(__name__)
    
    @cached(ttl=3600, key_prefix="books_search") 
    async def search_books(
        self, 
        query: str, 
        limit: int = 20,
        offset: int = 0,
        fields: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        try:

            encoded_query = urllib.parse.quote_plus(query)
            
            url = f"{self.base_url}/search.json"
            
            params = {
                "q": encoded_query,
                "limit": limit,
                "offset": offset
            }
            
            if fields:
                params["fields"] = ",".join(fields)
            
            self.logger.info(f"Buscando livros: query='{query}', limit={limit}")

            async with http_client() as client:
                response = await client.request("GET", url, params=params)
            response_data = response.get("data", {})
            if response_data.get("docs"):
                books = []
                for book in response_data["docs"]:
                    processed_book = {
                        "title": book.get("title", "N/A"),
                        "author_name": book.get("author_name", []),
                        "first_publish_year": book.get("first_publish_year"),
                        "isbn": book.get("isbn", []),
                        "language": book.get("language", []),
                        "subject": book.get("subject", [])[:5],  
                        "publisher": book.get("publisher", [])[:3],  
                        "cover_i": book.get("cover_i"), 
                        "key": book.get("key"),
                        "rating": book.get("ratings_average"),
                        "rating_count": book.get("ratings_count")
                    }
                    
                    if book.get("cover_i"):
                        processed_book["cover_url"] = f"https://covers.openlibrary.org/b/id/{book['cover_i']}-M.jpg"
                    
                    books.append(processed_book)
                
                return {
                    "success": True,
                    "total": response_data.get("numFound", 0),
                    "offset": response_data.get("start", 0),
                    "books": books,
                    "query": query
                }
            
            return {
                "success": True,
                "total": 0,
                "books": [],
                "query": query,
                "message": "Nenhum livro encontrado"
            }
            
        except Exception as e:
            self.logger.error(f"Erro ao buscar livros: {e}")
            return {
                "success": False,
                "error": str(e),
                "query": query
            }
    
    @cached(ttl=7200, key_prefix="book_details")  
    async def get_book_details(self, book_key: str) -> Dict[str, Any]:
        try:
            clean_key = book_key.lstrip('/')
            
            url = f"{self.base_url}/{clean_key}.json"
            
            self.logger.info(f"Buscando detalhes do livro: {book_key}")
            
            async with http_client() as client:
                response = await client.request("GET", url)
            
            book_data = response.get("data", {})
            return {
                "success": True,
                "book": {
                    "title": book_data.get("title", "N/A"),
                    "description": self._extract_description(book_data.get("description")),
                    "subjects": book_data.get("subjects", []),
                    "subject_places": book_data.get("subject_places", []),
                    "subject_times": book_data.get("subject_times", []),
                    "key": book_data.get("key"),
                    "covers": book_data.get("covers", []),
                    "created": book_data.get("created", {}).get("value"),
                    "last_modified": book_data.get("last_modified", {}).get("value")
                }
            }
            
        except Exception as e:
            self.logger.error(f"Erro ao obter detalhes do livro {book_key}: {e}")
            return {
                "success": False,
                "error": str(e),
                "book_key": book_key
            }
    
    def _extract_description(self, description) -> str:
        if isinstance(description, dict):
            return description.get("value", "")
        elif isinstance(description, str):
            return description
        return ""

openlibrary_service = OpenLibraryService()
