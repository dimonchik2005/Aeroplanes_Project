from aeroplanes_project.aeroplane import Aeroplane


def filter_aeroplanes_by_country(
    aeroplanes: list[Aeroplane],
    country: str,
) -> list[Aeroplane]:
    """Фильтрует самолеты по стране регистрации."""
    if not country:
        return aeroplanes

    return [
        aeroplane
        for aeroplane in aeroplanes
        if aeroplane.origin_country.lower() == country.lower()
    ]


def get_aeroplanes_by_altitude(
    aeroplanes: list[Aeroplane],
    min_altitude: float,
    max_altitude: float,
) -> list[Aeroplane]:
    """Возвращает самолеты в указанном диапазоне высоты."""
    return [
        aeroplane
        for aeroplane in aeroplanes
        if min_altitude <= aeroplane.altitude <= max_altitude
    ]


def sort_aeroplanes_by_altitude(
    aeroplanes: list[Aeroplane],
) -> list[Aeroplane]:
    """Сортирует самолеты по высоте полета по убыванию."""
    return sorted(aeroplanes, key=lambda aeroplane: aeroplane.altitude, reverse=True)


def get_top_aeroplanes(
    aeroplanes: list[Aeroplane],
    top_n: int,
) -> list[Aeroplane]:
    """Возвращает топ N самолетов."""
    if top_n <= 0:
        return []

    return aeroplanes[:top_n]


def print_aeroplanes(aeroplanes: list[Aeroplane]) -> None:
    """Печатает список самолетов."""
    if not aeroplanes:
        print("Самолеты не найдены")
        return

    for aeroplane in aeroplanes:
        print(aeroplane)
