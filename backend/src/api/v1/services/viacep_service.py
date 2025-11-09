from typing import Dict, Any, Optional
import re


class ViaCEPService:

    
    def __init__(self):
        self.base_url = "https://viacep.com.br/ws"
    
    def _validate_cep(self, cep: str) -> str:

        clean_cep = re.sub(r'\D', '', cep)
        

        if len(clean_cep) == 8:
            return clean_cep
        
        raise ValueError(f"CEP inválido: {cep}. Deve conter 8 dígitos.")
    
    async def get_address_by_cep(self, cep: str) -> Dict[str, Any]:
        try:
            from src.utils.http_client import http_client
            from src.utils.logger import get_logger
            from src.utils.cache import cached
            
            logger = get_logger(__name__)
            

            clean_cep = self._validate_cep(cep)
            
            @cached(ttl=86400, key_prefix="cep") 
            async def _fetch_cep(validated_cep: str):
                url = f"{self.base_url}/{validated_cep}/json/"
                
                logger.info(f"Consultando CEP: {cep}")
                
                async with http_client() as client:
                    response = await client.request("GET", url)
                
                data = response.get("data", {})
                
                if data.get("erro"):
                    return {
                        "success": False,
                        "error": "CEP não encontrado",
                        "cep": cep
                    }
                
                return {
                    "success": True,
                    "message": f"CEP {cep} encontrado com sucesso",
                    "data": {
                        "cep": data.get("cep"),
                        "street": data.get("logradouro"),
                        "complement": data.get("complemento"),
                        "neighborhood": data.get("bairro"), 
                        "city": data.get("localidade"),
                        "state": data.get("uf"),
                        "ibge_code": data.get("ibge"),
                        "gia_code": data.get("gia"),
                        "ddd": data.get("ddd"),
                        "siafi_code": data.get("siafi")
                    },
                    "cache_info": response.get("cache_info", {})
                }
            
            return await _fetch_cep(clean_cep)
            
        except ValueError as ve:
            return {
                "success": False,
                "message": "CEP inválido",
                "error": str(ve),
                "data": {"cep": cep}
            }
        except Exception as e:
            from src.utils.logger import get_logger
            logger = get_logger(__name__)
            logger.error(f"Erro ao consultar CEP {cep}: {e}")
            return {
                "success": False,
                "message": f"Erro ao consultar CEP {cep}",
                "error": str(e),
                "data": {"cep": cep}
            }
    
    async def search_addresses_by_location(
        self, 
        state: str, 
        city: str, 
        street: str
    ) -> Dict[str, Any]:
        try:
            from src.utils.http_client import http_client
            from src.utils.logger import get_logger
            import urllib.parse
            
            logger = get_logger(__name__)
            
            if len(state) != 2:
                raise ValueError("Estado deve ter 2 caracteres (UF)")
            
            if len(street) < 3:
                raise ValueError("Nome da rua deve ter pelo menos 3 caracteres")
            
            encoded_state = urllib.parse.quote_plus(state.upper())
            encoded_city = urllib.parse.quote_plus(city)
            encoded_street = urllib.parse.quote_plus(street)
            
            url = f"{self.base_url}/{encoded_state}/{encoded_city}/{encoded_street}/json/"
            
            logger.info(f"Buscando endereços: {state}/{city}/{street}")
            
            async with http_client() as client:
                response = await client.request("GET", url)
            
            data = response.get("data", [])
            
            if isinstance(data, list):
                addresses = []
                for address in data:
                    addresses.append({
                        "cep": address.get("cep"),
                        "street": address.get("logradouro"),
                        "complement": address.get("complemento"),
                        "neighborhood": address.get("bairro"),
                        "city": address.get("localidade"),
                        "state": address.get("uf"),
                        "ibge_code": address.get("ibge"),
                        "gia_code": address.get("gia"),
                        "ddd": address.get("ddd"),
                        "siafi_code": address.get("siafi")
                    })
                
                return {
                    "success": True,
                    "total": len(addresses),
                    "addresses": addresses,
                    "search_params": {
                        "state": state,
                        "city": city,
                        "street": street
                    }
                }
            
            return {
                "success": True,
                "total": 0,
                "addresses": [],
                "message": "Nenhum endereço encontrado"
            }
            
        except ValueError as ve:
            return {
                "success": False,
                "error": str(ve),
                "search_params": {"state": state, "city": city, "street": street}
            }
        except Exception as e:
            from src.utils.logger import get_logger
            logger = get_logger(__name__)
            logger.error(f"Erro ao buscar endereços: {e}")
            return {
                "success": False,
                "error": str(e),
                "search_params": {"state": state, "city": city, "street": street}
            }


viacep_service = ViaCEPService()
