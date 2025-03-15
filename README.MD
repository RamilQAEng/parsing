# Парсер сайтов

Проект для парсинга сайтов с использованием Python. Парсер поддерживает извлечение заголовков (`h1`, `h2`, `h3`), ссылок (`<a href>`), изображений (`<img src>`) и мета-тегов.

## Установка

1. Убедитесь, что у вас установлен Python 3.8 или выше.
2. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/RamilQAEng/parsing.git
   cd ваш-репозиторий
Установите зависимости:

bash
Copy
pip install -r requirements.txt
Использование
Заполните файл inputs/proxies.txt прокси (по одному на строку в формате ip:port).

Настройте конфигурацию парсера в configs/q_parser_config.json.

Запустите программу:

bash
Copy
python main.py
Введите URL сайта и выберите конфигурацию через графический интерфейс.

Структура проекта
Copy
ParserApp/
├── core/
│   ├── proxy_manager.py
│   ├── parser_engine.py
│   └── validator.py
├── configs/
│   ├── default_selectors.json
│   └── q_parser_config.json
├── inputs/
│   ├── proxies.txt
│   └── custom_selectors.csv
├── outputs/
│   └── results_{timestamp}.csv
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
Пример конфигурации
Пример конфигурации для парсинга заголовков, ссылок и изображений:

json
Copy
{
  "selectors": {
    "headers": {
      "h1": "h1",
      "h2": "h2",
      "h3": "h3"
    },
    "links": {
      "a": "a",
      "href": "a@href"
    },
    "images": {
      "img": "img",
      "src": "img@src"
    }
  }
}
Лицензия
Этот проект распространяется под лицензией MIT. Подробности см. в файле LICENSE.