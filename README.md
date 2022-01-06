# TransFinance

Инструмент анализа инвестиций и инвестиционного портфеля в Тинькофф Инвестициях

## Установка

1. Поставить python 3.10
2. Установить пакетный менеджер poetry `pip install poetry`
3. Развернуть виртуальное окружение `poetry install`
4. Создать конфигурационный файл transfinance/config.yaml с пользовательскими 
данными аналогии с examples/config.yaml

## Запуск

## Разработка

1. Перед коммитами использовать линтеры:
   * mypy `poetry run mypy .`
   * black `poetry run black .`