from bs4 import BeautifulSoup
import requests
from typing import Dict, List, Union
from fake_useragent import UserAgent
import logging

logger = logging.getLogger(__name__)

class StaticParser:
    def __init__(self, proxy: str = None):
        self.proxy = proxy
        self.ua = UserAgent()
        
    def parse_page(self, url: str, selectors: dict) -> dict:
        """Парсинг статических страниц"""
        try:
            response = requests.get(
                url,
                proxies={"http": self.proxy, "https": self.proxy} if self.proxy else None,
                headers={"User-Agent": self.ua.random},
                timeout=15
            )
            if response.status_code != 200:
                return {}
                
            soup = BeautifulSoup(response.text, "lxml")
            results = {}
            
            for field, selector_config in selectors.items():
                if isinstance(selector_config, dict):
                    # Обработка атрибутов (например, img@src)
                    selector = selector_config.get("selector")
                    attr = selector_config.get("attr")
                    elements = soup.select(selector)
                    values = [el.get(attr, '') for el in elements if el and attr in el.attrs]
                else:
                    # Обработка текста (например, h1, h2)
                    elements = soup.select(selector_config)
                    values = [el.get_text(strip=True) for el in elements]
                
                results[field] = values if len(values) > 1 else values[0] if values else None
                
            return results
            
        except Exception as e:
            logger.error(f"Static parsing failed: {str(e)}")
            return {}