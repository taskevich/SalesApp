from datetime import datetime


def datetime_parse(date: str):
    """
    Вспомогательная функция парсинга времени из строки.
    """
    try:
        return datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return datetime.strptime(date, "%Y-%m-%d")
