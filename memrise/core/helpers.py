from random import randint


def generate_custom_id(max_len: int = 7) -> int:
    """Генерация номера ID для дублированных записей"""
    range_start = 10**(max_len-1)
    range_end = (10**max_len)-1
    return randint(range_start, range_end)
