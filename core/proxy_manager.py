import requests
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional

class ProxyManager:
    def __init__(self, proxy_file: str = "inputs/proxies.txt"):
        self.proxy_file = proxy_file
        self.valid_proxies: List[str] = []
        
    def load_proxies(self) -> List[str]:
        with open(self.proxy_file, "r") as f:
            return [line.strip() for line in f if line.strip()]
    
    def check_proxy(self, proxy: str, test_url: str = "https://httpbin.org/ip") -> bool:
        try:
            response = requests.get(
                test_url,
                proxies={"http": proxy, "https": proxy},
                timeout=10,
                headers={"User-Agent": "Mozilla/5.0"}
            )
            return response.status_code == 200
        except Exception as e:
            return False
    
    def validate_proxies(self, max_workers: int = 20) -> None:
        proxies = self.load_proxies()
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = executor.map(self.check_proxy, proxies)
            self.valid_proxies = [p for p, valid in zip(proxies, results) if valid]
        
    def get_random_proxy(self) -> Optional[str]:
        import random
        return random.choice(self.valid_proxies) if self.valid_proxies else None