from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import random
import logging

logger = logging.getLogger(__name__)

class DynamicParser:
    def __init__(self, proxy: str = None, headless: bool = False, user_agent: str = None):
        self.options = Options()
        if headless:
            self.options.add_argument("--headless")
        if proxy:
            self.options.add_argument(f"--proxy-server={proxy}")
        if user_agent:
            self.options.add_argument(f"user-agent={user_agent}")
        
        # Отключаем GPU и другие ненужные функции
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--disable-popup-blocking")
        self.options.add_argument("--disable-default-apps")
        self.options.add_argument("--disable-infobars")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--no-sandbox")
        
        # Автоматическая установка ChromeDriver
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        
    def parse_page(self, url: str, selectors: dict) -> dict:
        """Парсинг динамических страниц с использованием Selenium"""
        try:
            self.driver.get(url)
            time.sleep(random.uniform(2, 5))  # Рандомная задержка
            
            # Пролистывание страницы для загрузки контента
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
            soup = BeautifulSoup(self.driver.page_source, "lxml")
            results = {}
            
            for field, selector in selectors.items():
                elements = soup.select(selector)
                values = [el.get_text(strip=True) for el in elements]
                results[field] = values if len(values) > 1 else values[0] if values else None
                
            return results
            
        except Exception as e:
            logger.error(f"Dynamic parsing failed: {str(e)}")
            return {}
            
        finally:
            self.driver.quit()