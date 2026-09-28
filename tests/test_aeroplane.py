import pytest

from aeroplanes_project.aeroplane import Aeroplane


def test_aeroplane_initialization() -> None:
    """Проверяет создание объекта Aeroplane."""
    aeroplane = Aeroplane(
        "4b1812",
        "SWR438A",
        "Switzerland",
        189.7,
        4267.2,
        False,
    )

    assert aeroplane.icao24 == "4b1812"
    assert aeroplane.callsign == "SWR438A"
    assert aeroplane.origin_country == "Switzerland"
    assert aeroplane.velocity == 189.7
    assert aeroplane.altitude == 4267.2
    assert aeroplane.on_ground is False


def test_aeroplane_empty_callsign() -> None:
    """Проверяет замену пустого позывного."""
    aeroplane = Aeroplane("4b1812", "", "Switzerland", 189.7, 4267.2)

    assert aeroplane.callsign == "Unknown"


def test_aeroplane_invalid_icao24() -> None:
    """Проверяет ошибку при пустом ICAO24."""
    with pytest.raises(ValueError, match="ICAO24 не может быть пустым"):
        Aeroplane("", "SWR438A", "Switzerland", 189.7, 4267.2)


def test_aeroplane_negative_velocity() -> None:
    """Проверяет ошибку при отрицательной скорости."""
    with pytest.raises(ValueError, match="Скорость не может быть отрицательной"):
        Aeroplane("4b1812", "SWR438A", "Switzerland", -1, 4267.2)


def test_aeroplane_negative_altitude() -> None:
    """Проверяет ошибку при отрицательной высоте."""
    with pytest.raises(ValueError, match="Высота не может быть отрицательной"):
        Aeroplane("4b1812", "SWR438A", "Switzerland", 189.7, -1)


def test_aeroplane_str() -> None:
    """Проверяет строковое представление самолета."""
    aeroplane = Aeroplane("4b1812", "SWR438A", "Switzerland", 189.7, 4267.2)

    assert str(aeroplane) == (
        "SWR438A | Switzerland | скорость: 189.7 м/с | высота: 4267.2 м"
    )


def test_aeroplane_repr() -> None:
    """Проверяет техническое представление самолета."""
    aeroplane = Aeroplane("4b1812", "SWR438A", "Switzerland", 189.7, 4267.2)

    assert repr(aeroplane) == (
        "Aeroplane('4b1812', 'SWR438A', 'Switzerland', 189.7, 4267.2, False)"
    )


def test_aeroplane_compare_by_velocity() -> None:
    """Проверяет сравнение самолетов по скорости."""
    aeroplane1 = Aeroplane("4b1812", "SWR438A", "Switzerland", 189.7, 4267.2)
    aeroplane2 = Aeroplane("abc123", "TEST", "Canada", 250.0, 3000.0)

    assert aeroplane1 < aeroplane2


def test_aeroplane_compare_by_altitude() -> None:
    """Проверяет сравнение самолетов по высоте."""
    aeroplane1 = Aeroplane("4b1812", "SWR438A", "Switzerland", 189.7, 4267.2)
    aeroplane2 = Aeroplane("abc123", "TEST", "Canada", 250.0, 3000.0)

    assert aeroplane1.is_higher_than(aeroplane2) is True


def test_aeroplane_to_dict() -> None:
    """Проверяет преобразование самолета в словарь."""
    aeroplane = Aeroplane("4b1812", "SWR438A", "Switzerland", 189.7, 4267.2)

    assert aeroplane.to_dict() == {
        "icao24": "4b1812",
        "callsign": "SWR438A",
        "origin_country": "Switzerland",
        "velocity": 189.7,
        "altitude": 4267.2,
        "on_ground": False,
    }


def test_from_opensky_state() -> None:
    """Проверяет создание объекта из state OpenSky."""
    state = [
        "4b1812",
        "SWR438A ",
        "Switzerland",
        1766166618,
        1766166618,
        -0.0168,
        51.0888,
        4267.2,
        False,
        189.7,
        129.39,
        14.63,
        None,
        4282.44,
        "2061",
        False,
        0,
    ]

    aeroplane = Aeroplane.from_opensky_state(state)

    assert aeroplane.icao24 == "4b1812"
    assert aeroplane.callsign == "SWR438A"
    assert aeroplane.origin_country == "Switzerland"
    assert aeroplane.altitude == 4267.2
    assert aeroplane.velocity == 189.7
    assert aeroplane.on_ground is False


def test_cast_to_object_list() -> None:
    """Проверяет преобразование ответа OpenSky в список объектов."""
    data = {
        "time": 1766142246,
        "states": [
            [
                "4b1812",
                "SWR438A ",
                "Switzerland",
                1766166618,
                1766166618,
                -0.0168,
                51.0888,
                4267.2,
                False,
                189.7,
                129.39,
                14.63,
                None,
                4282.44,
                "2061",
                False,
                0,
            ]
        ],
    }

    aeroplanes = Aeroplane.cast_to_object_list(data)

    assert len(aeroplanes) == 1
    assert aeroplanes[0].callsign == "SWR438A"


def test_cast_to_object_list_empty() -> None:
    """Проверяет пустой ответ OpenSky."""
    data = {"time": 1766142246, "states": None}

    assert Aeroplane.cast_to_object_list(data) == []
