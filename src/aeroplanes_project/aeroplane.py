from __future__ import annotations

from typing import Any


class Aeroplane:
    """Класс для описания самолета."""

    icao24: str
    callsign: str
    origin_country: str
    velocity: float
    altitude: float
    on_ground: bool

    def __init__(
        self,
        icao24: str,
        callsign: str,
        origin_country: str,
        velocity: float,
        altitude: float,
        on_ground: bool = False,
    ) -> None:
        """Инициализирует объект самолета."""
        if not icao24:
            raise ValueError("ICAO24 не может быть пустым")

        if velocity < 0:
            raise ValueError("Скорость не может быть отрицательной")

        if altitude < 0:
            raise ValueError("Высота не может быть отрицательной")

        self.icao24 = icao24
        self.callsign = callsign.strip() if callsign else "Unknown"
        self.origin_country = origin_country
        self.velocity = velocity
        self.altitude = altitude
        self.on_ground = on_ground

    def __repr__(self) -> str:
        """Возвращает техническое представление самолета."""
        return (
            f"Aeroplane("
            f"{self.icao24!r}, "
            f"{self.callsign!r}, "
            f"{self.origin_country!r}, "
            f"{self.velocity}, "
            f"{self.altitude}, "
            f"{self.on_ground}"
            f")"
        )

    def __str__(self) -> str:
        """Возвращает человекочитаемое представление самолета."""
        return (
            f"{self.callsign} | {self.origin_country} | "
            f"скорость: {self.velocity} м/с | "
            f"высота: {self.altitude} м"
        )

    def __lt__(self, other: Aeroplane) -> bool:
        """Сравнивает самолеты по скорости."""
        return self.velocity < other.velocity

    def is_higher_than(self, other: Aeroplane) -> bool:
        """Проверяет, летит ли самолет выше другого самолета."""
        return self.altitude > other.altitude

    def to_dict(self) -> dict[str, Any]:
        """Преобразует объект самолета в словарь."""
        return {
            "icao24": self.icao24,
            "callsign": self.callsign,
            "origin_country": self.origin_country,
            "velocity": self.velocity,
            "altitude": self.altitude,
            "on_ground": self.on_ground,
        }

    @classmethod
    def from_opensky_state(cls, state: list[Any]) -> Aeroplane:
        """Создает объект Aeroplane из одного state OpenSky."""
        icao24 = state[0]
        callsign = state[1]
        origin_country = state[2]
        altitude = state[7] or 0
        on_ground = state[8]
        velocity = state[9] or 0

        return cls(
            icao24=icao24,
            callsign=callsign,
            origin_country=origin_country,
            velocity=float(velocity),
            altitude=float(altitude),
            on_ground=bool(on_ground),
        )

    @classmethod
    def cast_to_object_list(cls, data: dict[str, Any]) -> list[Aeroplane]:
        """Преобразует ответ OpenSky в список объектов Aeroplane."""
        states = data.get("states")

        if not states:
            return []

        aeroplanes = []

        for state in states:
            try:
                aeroplanes.append(cls.from_opensky_state(state))
            except ValueError, TypeError, IndexError:
                continue

        return aeroplanes
