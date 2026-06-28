from abc import ABC, abstractmethod
from typing import Any

import requests


class AbstractAPI(ABC):
    """Абстрактный класс для работы с API."""

    @abstractmethod
    def get_country_coordinates(self, country: str) -> list[str]:
        """Получает географические координаты страны."""

    @abstractmethod
    def get_aeroplanes(self, country: str) -> dict[str, Any]:
        """Получает данные о самолетах в воздушном пространстве страны."""


class AeroplanesAPI(AbstractAPI):
    """Класс для работы с Nominatim и OpenSky API."""

    def __init__(self) -> None:
        """Инициализирует API-адреса."""
        self.openstreetmap_url = "https://nominatim.openstreetmap.org/search"
        self.opensky_url = "https://opensky-network.org/api/states/all"

    def get_country_coordinates(self, country: str) -> list[str]:
        """Получает boundingbox страны через Nominatim."""
        headers = {
            "User-Agent": "aeroplanes-project/1.0",
        }
        params = {
            "country": country,
            "format": "json",
            "limit": 1,
        }

        response = requests.get(
            self.openstreetmap_url,
            params=params,
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()

        data = response.json()

        if not data:
            raise ValueError("Страна не найдена")

        boundingbox = data[0].get("boundingbox")

        if not boundingbox:
            raise ValueError("Координаты страны не найдены")

        return list(boundingbox)

    def get_aeroplanes(self, country: str) -> dict[str, Any]:
        """Получает самолеты по координатам страны через OpenSky."""
        coordinates = self.get_country_coordinates(country)

        params = {
            "lamin": coordinates[0],
            "lamax": coordinates[1],
            "lomin": coordinates[2],
            "lomax": coordinates[3],
        }

        response = requests.get(
            self.opensky_url,
            params=params,
            timeout=10,
        )
        response.raise_for_status()

        data = response.json()

        if not isinstance(data, dict):
            raise ValueError("Некорректный ответ OpenSky")

        return data