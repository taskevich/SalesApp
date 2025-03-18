from datetime import datetime


def datetime_parse(date: str):
    """
    Вспомогательная функция парсинга времени из строки.
    """
    return datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
