from venv import logger
from gooey import Gooey, GooeyParser
import pandas as pd
from datetime import datetime
from core.proxy_manager import ProxyManager
from core.parser_engine import SEOParser
from config_loader import load_config
import os
import csv
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('seo_parser.log'),
        logging.StreamHandler()
    ]
)

@Gooey(program_name="SEO Parser Pro", default_size=(800, 600))
def main():
    parser = GooeyParser()
    
    parser.add_argument(
        "--proxy_file", 
        widget="FileChooser",
        help="Выберите файл с прокси (формат: ip:port)",
        default="inputs/proxies.txt"
    )
    
    parser.add_argument(
        "--target_url",
        required=True,
        help="URL сайта для парсинга (например, https://example.com)"
    )
    
    parser.add_argument(
        "--selectors_config",
        widget="FileChooser",
        help="Конфигурационный файл (JSON/YAML)",
        default="configs/seo_config.yaml"
    )
    
    args = parser.parse_args()
    
    # Загрузка конфигурации
    config = load_config(args.selectors_config)
    selectors = config.get('fields', {})
    
    # Инициализация прокси
    proxy_manager = ProxyManager(args.proxy_file)
    proxy_manager.validate_proxies()
    proxy = proxy_manager.get_random_proxy()
    
    # Парсинг
    seo_parser = SEOParser(args.target_url, selectors, proxy)
    results = seo_parser.parse_seo()

    # Проверка наличия данных
    if not results:
            logger.error("No data to save. Check the target URL and selectors.")
            return

    # Определяем максимальное количество строк
    max_rows = max(len(v) for v in results.values()) if results else 0

    # Создаем список словарей для записи
    csv_rows = []
    for i in range(max_rows):
        row = {}
        for key in results.keys():
            row[key] = results[key][i] if i < len(results[key]) else ""
        csv_rows.append(row)

    # Сохранение результатов
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join("outputs", f"results_{timestamp}.csv")
    
    # Запись в CSV
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=results.keys(), delimiter=';')
        writer.writeheader()
        writer.writerows(csv_rows)
    
    print(f"Результаты сохранены в {output_file}")

if __name__ == "__main__":
    main()