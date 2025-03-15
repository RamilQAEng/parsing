from bs4 import BeautifulSoup
import requests
from typing import Dict, List, Optional
from fake_useragent import UserAgent
import logging

logger = logging.getLogger(__name__)

class SEOParser:
    def __init__(self, base_url: str, selectors: Dict[str, str], proxy: str = None):
        self.base_url = base_url
        self.selectors = selectors  # Новая структура селекторов
        self.proxy = proxy
        self.ua = UserAgent()
        
    def _make_request(self, url: str) -> Optional[str]:
        proxies = {"http": self.proxy, "https": self.proxy} if self.proxy else None
        try:
            response = requests.get(
                url,
                proxies=proxies,
                timeout=20,
                headers={"User-Agent": self.ua.random}
            )
            return response.text if response.status_code == 200 else None
        except Exception as e:
            logger.error(f"Request error: {str(e)}")
            return None
            
    def parse_seo(self) -> Dict[str, List[str]]:
        html = self._make_request(self.base_url)
        if not html:
            return {}

        soup = BeautifulSoup(html, "lxml")
        results = {}

        for field_name, selector in self.selectors.items():
            try:
                # Обработка составных селекторов
                if isinstance(selector, list):
                    values = []
                    for s in selector:
                        if '@' in s:
                            css_selector, attr = s.split('@', 1)
                            elements = soup.select(css_selector)
                            values.extend([el.get(attr, '') for el in elements if el and attr in el.attrs])
                        else:
                            elements = soup.select(s)
                            values.extend([el.get_text(strip=True) for el in elements])
                    results[field_name] = values
                else:
                    if '@' in selector:
                        css_selector, attr = selector.split('@', 1)
                        elements = soup.select(css_selector)
                        results[field_name] = [el.get(attr, '') for el in elements if el and attr in el.attrs]
                    else:
                        elements = soup.select(selector)
                        results[field_name] = [el.get_text(strip=True) for el in elements]

                if not results[field_name]:
                    logger.warning(f"Elements not found: {field_name} ({selector})")

            except Exception as e:
                logger.error(f"Error parsing {field_name}: {str(e)}")
                results[field_name] = []

        return results