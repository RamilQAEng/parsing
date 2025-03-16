from gooey import Gooey, GooeyParser
from core.static_parser import StaticParser
from core.dynamic_parser import DynamicParser
from core.proxy_manager import ProxyManager
from config_loader import load_config
from datetime import datetime
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

@Gooey(program_name="Marketplace Parser", default_size=(800, 600))
def main():
    parser = GooeyParser(description="Парсер для маркетплейсов")
    
    # Настройки GUI
    parser.add_argument(
        "--platform",
        widget="Dropdown",
        choices=["Ozon", "Wildberries", "seo"],
        default="Ozon",
        help="Выберите платформу для парсинга"
    )
    
    parser.add_argument(
        "--parser_type",
        widget="Dropdown",
        choices=["Статический", "Динамический"],
        default="Динамический",
        help="Тип парсера (для динамических сайтов требуется Chrome)"
    )
    
    parser.add_argument(
        "--proxy_file",
        widget="FileChooser",
        help="Файл с прокси (ip:port)",
        default="configs/proxies.txt"
    )
    
    parser.add_argument(
        "--target_url",
        required=True,
        help="URL для парсинга (например, https://www.ozon.ru/product/123)"
    )
    
    args = parser.parse_args()
    
    # Загрузка конфигурации
    config = load_config(f"configs/{args.platform.lower()}_config.yaml")
    selectors = config.get('fields', {})
    
    # Инициализация прокси
    proxy_manager = ProxyManager(args.proxy_file)
    proxy_manager.validate_proxies()
    proxy = proxy_manager.get_random_proxy()
    
    # Выбор парсера
    try:
        if args.parser_type == "Статический":
            parser = StaticParser(proxy=proxy)
        else:
            parser = DynamicParser(
                proxy=proxy,
                headless=False,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
            
        results = parser.parse_page(args.target_url, selectors)
        
    except Exception as e:
        logging.error(f"Ошибка парсинга: {str(e)}")
        return

    # Очистка данных
    cleaned_results = {}
    for field, values in results.items():
        if field == "price" or field == "old_price":
            cleaned = [v.replace(" ", "").replace("₽", "").strip() for v in values]
        else:
            cleaned = values
        cleaned_results[field] = cleaned

        # Проверка наличия данных
    if not cleaned_results:
        logging.error("Нет данных для записи в CSV.")
        return


    # Нормализация данных для CSV
    normalized = []
    max_rows = max(len(v) if isinstance(v, list) else 1 for v in cleaned_results.values())

    for i in range(max_rows):
        row = {}
        for key, values in cleaned_results.items():
            if isinstance(values, list):
                row[key] = values[i] if i < len(values) else ""
            else:
                row[key] = values if i == 0 else ""
        normalized.append(row)

    # Запись файла
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join("outputs", f"{args.platform}_{timestamp}.csv")
    
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=cleaned_results.keys(), delimiter=';')
        writer.writeheader()
        writer.writerows(normalized)
    
    logging.info(f"Данные сохранены в: {output_file}")

if __name__ == "__main__":
    main()