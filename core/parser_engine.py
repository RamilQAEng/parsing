from bs4 import BeautifulSoup
import requests
from typing import Dict, List, Optional
from fake_useragent import UserAgent

class SEOParser:
    def __init__(self, base_url: str, selectors: Dict[str, str], proxy: str = None):
        self.base_url = base_url
        self.selectors = selectors
        self.proxy = proxy
        self.ua = UserAgent()
        
    def _make_request(self, url: str) -> Optional[str]:
        proxies = {"http": self.proxy, "https": self.proxy} if self.proxy else None
        try:
            response = requests.get(
                url,
                proxies=proxies,
                timeout=15,
                headers={"User-Agent": self.ua.random}
            )
            return response.text if response.status_code == 200 else None
        except Exception as e:
            return None
            
    def parse_seo(self) -> Dict[str, Dict[str, List[str]]]:
        html = self._make_request(self.base_url)
        if not html:
            return {}
            
        soup = BeautifulSoup(html, "lxml")
        results = {
            "headers": {},
            "links": {},
            "images": {},
            "meta": []
        }
        
        # Парсинг заголовков
        for header_type, selector in self.selectors.get("headers", {}).items():
            elements = soup.select(selector)
            results["headers"][header_type] = [el.get_text(strip=True) for el in elements]
        
        # Парсинг ссылок
        for link_type, selector in self.selectors.get("links", {}).items():
            if "@" in selector:
                tag, attr = selector.split("@")
                elements = soup.select(tag)
                results["links"][link_type] = [el.get(attr, "") for el in elements]
            else:
                elements = soup.select(selector)
                results["links"][link_type] = [el.get_text(strip=True) for el in elements]
        
        # Парсинг изображений
        for img_type, selector in self.selectors.get("images", {}).items():
            if "@" in selector:
                tag, attr = selector.split("@")
                elements = soup.select(tag)
                results["images"][img_type] = [el.get(attr, "") for el in elements]
            else:
                elements = soup.select(selector)
                results["images"][img_type] = [el.get_text(strip=True) for el in elements]
        
        # Парсинг мета-тегов
        meta_tags = soup.find_all("meta")
        results["meta"] = [tag.attrs for tag in meta_tags if "name" in tag.attrs or "property" in tag.attrs]
        
        return results