from gooey import Gooey, GooeyParser
import json
import pandas as pd
from datetime import datetime
from core.proxy_manager import ProxyManager
from core.parser_engine import SEOParser
import os
import csv

@Gooey(program_name="SEO Parser Pro", default_size=(800, 600))
def main():
    parser = GooeyParser()
    
    # Вкладка "Основные настройки"
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
    
    # Вкладка "SEO-селекторы"
    parser.add_argument(
        "--selectors_config",
        widget="FileChooser",
        help="JSON-файл с кастомными селекторами",
        default="configs/q_parser_config.json"  # Используем новый конфиг
    )
    
    args = parser.parse_args()
    
    # Загрузка селекторов
    with open(args.selectors_config, "r", encoding="utf-8") as f:
        selectors = json.load(f)
    
    # Инициализация прокси
    proxy_manager = ProxyManager(args.proxy_file)
    proxy_manager.validate_proxies()
    proxy = proxy_manager.get_random_proxy()
    
    # Парсинг
    seo_parser = SEOParser(args.target_url, selectors["selectors"], proxy)
    results = seo_parser.parse_seo()
    
    # Сохранение результатов в CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join("outputs", f"results_{timestamp}.csv")
    
    # Преобразуем результаты в DataFrame
    rows = []
    for section, items in results.items():
        if isinstance(items, list):  # Обработка списков (например, headers, links, images)
            for item in items:
                rows.append([section, "", item])  # Section, Key, Value
        elif isinstance(items, dict):  # Обработка словарей (например, meta)
            for key, values in items.items():
                if isinstance(values, list):
                    for value in values:
                        rows.append([section, key, value])
                else:
                    rows.append([section, key, values])
    
    df = pd.DataFrame(rows, columns=["Section", "Key", "Value"])
    df.to_csv(output_file, index=False, encoding="utf-8", quoting=csv.QUOTE_ALL)
    
    print(f"Результаты сохранены в {output_file}")

if __name__ == "__main__":
    main()