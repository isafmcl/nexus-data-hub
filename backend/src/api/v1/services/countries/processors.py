from typing import Dict, Any, List


class CountriesDataProcessor:
    
    @staticmethod
    def process_country_basic(country: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "name": country.get("name", {}).get("common", "Unknown"),
            "official_name": country.get("name", {}).get("official", ""),
            "capital": country.get("capital", ["N/A"])[0] if country.get("capital") else "N/A",
            "region": country.get("region", "Unknown"),
            "population": country.get("population", 0),
            "area": country.get("area", 0),
            "flag": country.get("flags", {}).get("png", ""),
            "currencies": list(country.get("currencies", {}).keys()) if country.get("currencies") else [],
            "code": country.get("cca2", ""),
            "code3": country.get("cca3", "")
        }
    
    @staticmethod
    def process_country_detailed(country: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "name": country.get("name", {}).get("common", "Unknown"),
            "official_name": country.get("name", {}).get("official", ""),
            "capital": country.get("capital", ["N/A"])[0] if country.get("capital") else "N/A",
            "region": country.get("region", "Unknown"),
            "subregion": country.get("subregion", "Unknown"),
            "population": country.get("population", 0),
            "area": country.get("area", 0),
            "borders": country.get("borders", []),
            "languages": list(country.get("languages", {}).values()) if country.get("languages") else [],
            "currencies": [
                {
                    "code": code,
                    "name": info.get("name", ""),
                    "symbol": info.get("symbol", "")
                }
                for code, info in country.get("currencies", {}).items()
            ] if country.get("currencies") else [],
            "timezones": country.get("timezones", []),
            "flag": country.get("flags", {}).get("png", ""),
            "coat_of_arms": country.get("coatOfArms", {}).get("png", ""),
            "maps": country.get("maps", {}).get("googleMaps", ""),
            "code": country.get("cca2", ""),
            "code3": country.get("cca3", "")
        }
    
    @staticmethod
    def process_countries_list(countries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [
            CountriesDataProcessor.process_country_basic(country)
            for country in countries
        ]
    
    @staticmethod
    def calculate_region_statistics(countries: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_population = sum(c.get("population", 0) for c in countries)
        total_area = sum(c.get("area", 0) for c in countries)
        
        return {
            "total_population": total_population,
            "total_area": total_area,
            "average_population": total_population // len(countries) if countries else 0,
            "average_area": total_area // len(countries) if countries else 0
        }
