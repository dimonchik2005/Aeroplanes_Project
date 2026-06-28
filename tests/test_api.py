from typing import Any

import pytest

from aeroplanes_project.api import AbstractAPI, AeroplanesAPI


class FakeResponse:
    """Фейковый ответ вместо настоящего requests.Response."""

    def __init__(self, data: Any) -> None:
        """Инициализирует фейковый ответ."""
        self.data = data

    def json(self) -> Any:
        """Возвращает JSON-данные."""
        return self.data

    def raise_for_status(self) -> None:
        """Имитирует успешный HTTP-ответ."""


def test_abstract_api_cannot_be_created() -> None:
    """Проверяет, что AbstractAPI нельзя создать напрямую."""
    with pytest.raises(TypeError):
        AbstractAPI()  # type: ignore[abstract]


def test_get_country_coordinates(monkeypatch: pytest.MonkeyPatch) -> None:
    """Проверяет получение координат страны."""
    api = AeroplanesAPI()

    def fake_get(*args: Any, **kwargs: Any) -> FakeResponse:
        return FakeResponse(
            [
                {
                    "boundingbox": [
                        "41.6765597",
                        "83.3362128",
                        "-141.0027500",
                        "-52.3237664",
                    ]
                }
            ]
        )

    monkeypatch.setattr("requests.get", fake_get)

    result = api.get_country_coordinates("Canada")

    assert result == [
        "41.6765597",
        "83.3362128",
        "-141.0027500",
        "-52.3237664",
    ]


def test_get_country_coordinates_empty_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Проверяет ошибку, если страна не найдена."""
    api = AeroplanesAPI()

    def fake_get(*args: Any, **kwargs: Any) -> FakeResponse:
        return FakeResponse([])

    monkeypatch.setattr("requests.get", fake_get)

    with pytest.raises(ValueError, match="Страна не найдена"):
        api.get_country_coordinates("UnknownCountry")


def test_get_country_coordinates_without_boundingbox(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Проверяет ошибку, если нет boundingbox."""
    api = AeroplanesAPI()

    def fake_get(*args: Any, **kwargs: Any) -> FakeResponse:
        return FakeResponse([{}])

    monkeypatch.setattr("requests.get", fake_get)

    with pytest.raises(ValueError, match="Координаты страны не найдены"):
        api.get_country_coordinates("Canada")


def test_get_aeroplanes(monkeypatch: pytest.MonkeyPatch) -> None:
    """Проверяет получение самолетов через OpenSky."""
    api = AeroplanesAPI()

    responses = [
        FakeResponse(
            [
                {
                    "boundingbox": [
                        "41.6765597",
                        "83.3362128",
                        "-141.0027500",
                        "-52.3237664",
                    ]
                }
            ]
        ),
        FakeResponse(
            {
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
        ),
    ]

    def fake_get(*args: Any, **kwargs: Any) -> FakeResponse:
        return responses.pop(0)

    monkeypatch.setattr("requests.get", fake_get)

    result = api.get_aeroplanes("Canada")

    assert result["time"] == 1766142246
    assert len(result["states"]) == 1
    assert result["states"][0][1] == "SWR438A "


def test_get_aeroplanes_invalid_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Проверяет ошибку при некорректном ответе OpenSky."""
    api = AeroplanesAPI()

    responses = [
        FakeResponse(
            [
                {
                    "boundingbox": [
                        "41.6765597",
                        "83.3362128",
                        "-141.0027500",
                        "-52.3237664",
                    ]
                }
            ]
        ),
        FakeResponse([]),
    ]

    def fake_get(*args: Any, **kwargs: Any) -> FakeResponse:
        return responses.pop(0)

    monkeypatch.setattr("requests.get", fake_get)

    with pytest.raises(ValueError, match="Некорректный ответ OpenSky"):
        api.get_aeroplanes("Canada")