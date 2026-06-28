from aeroplanes_project.aeroplane import Aeroplane
from aeroplanes_project.utils import (filter_aeroplanes_by_country,
                                      get_aeroplanes_by_altitude,
                                      get_top_aeroplanes, print_aeroplanes,
                                      sort_aeroplanes_by_altitude)


def test_filter_aeroplanes_by_country() -> None:
    """Проверяет фильтрацию самолетов по стране регистрации."""
    aeroplanes = [
        Aeroplane("1", "ONE", "Canada", 100.0, 1000.0),
        Aeroplane("2", "TWO", "Switzerland", 200.0, 2000.0),
        Aeroplane("3", "THREE", "Canada", 300.0, 3000.0),
    ]

    result = filter_aeroplanes_by_country(aeroplanes, "Canada")

    assert len(result) == 2
    assert result[0].icao24 == "1"
    assert result[1].icao24 == "3"


def test_filter_aeroplanes_by_country_empty_country() -> None:
    """Проверяет возврат всех самолетов, если страна не указана."""
    aeroplanes = [
        Aeroplane("1", "ONE", "Canada", 100.0, 1000.0),
    ]

    result = filter_aeroplanes_by_country(aeroplanes, "")

    assert result == aeroplanes


def test_filter_aeroplanes_by_country_case_insensitive() -> None:
    """Проверяет фильтрацию без учета регистра."""
    aeroplanes = [
        Aeroplane("1", "ONE", "Canada", 100.0, 1000.0),
    ]

    result = filter_aeroplanes_by_country(aeroplanes, "canada")

    assert len(result) == 1
    assert result[0].origin_country == "Canada"


def test_get_aeroplanes_by_altitude() -> None:
    """Проверяет фильтрацию самолетов по диапазону высоты."""
    aeroplanes = [
        Aeroplane("1", "ONE", "Canada", 100.0, 1000.0),
        Aeroplane("2", "TWO", "Switzerland", 200.0, 2000.0),
        Aeroplane("3", "THREE", "Canada", 300.0, 3000.0),
    ]

    result = get_aeroplanes_by_altitude(aeroplanes, 1500.0, 3000.0)

    assert len(result) == 2
    assert result[0].icao24 == "2"
    assert result[1].icao24 == "3"


def test_sort_aeroplanes_by_altitude() -> None:
    """Проверяет сортировку самолетов по высоте по убыванию."""
    aeroplanes = [
        Aeroplane("1", "ONE", "Canada", 100.0, 1000.0),
        Aeroplane("2", "TWO", "Switzerland", 200.0, 3000.0),
        Aeroplane("3", "THREE", "Canada", 300.0, 2000.0),
    ]

    result = sort_aeroplanes_by_altitude(aeroplanes)

    assert result[0].icao24 == "2"
    assert result[1].icao24 == "3"
    assert result[2].icao24 == "1"


def test_get_top_aeroplanes() -> None:
    """Проверяет получение топ N самолетов."""
    aeroplanes = [
        Aeroplane("1", "ONE", "Canada", 100.0, 1000.0),
        Aeroplane("2", "TWO", "Switzerland", 200.0, 3000.0),
        Aeroplane("3", "THREE", "Canada", 300.0, 2000.0),
    ]

    result = get_top_aeroplanes(aeroplanes, 2)

    assert len(result) == 2
    assert result[0].icao24 == "1"
    assert result[1].icao24 == "2"


def test_get_top_aeroplanes_zero() -> None:
    """Проверяет возврат пустого списка при top_n <= 0."""
    aeroplanes = [
        Aeroplane("1", "ONE", "Canada", 100.0, 1000.0),
    ]

    result = get_top_aeroplanes(aeroplanes, 0)

    assert result == []


def test_print_aeroplanes(capsys) -> None:
    """Проверяет печать списка самолетов."""
    aeroplanes = [
        Aeroplane("1", "ONE", "Canada", 100.0, 1000.0),
    ]

    print_aeroplanes(aeroplanes)
    captured = capsys.readouterr()

    assert "ONE | Canada | скорость: 100.0 м/с | высота: 1000.0 м" in captured.out


def test_print_aeroplanes_empty(capsys) -> None:
    """Проверяет печать сообщения, если самолетов нет."""
    print_aeroplanes([])
    captured = capsys.readouterr()

    assert "Самолеты не найдены" in captured.out
