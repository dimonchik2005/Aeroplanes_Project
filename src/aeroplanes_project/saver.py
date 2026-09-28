import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from aeroplanes_project.aeroplane import Aeroplane


class AbstractSaver(ABC):
    """Абстрактный класс для сохранения данных о самолетах."""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавляет самолет в файл."""

    @abstractmethod
    def get_aeroplanes(
        self,
        field_name: str | None = None,
        field_value: Any | None = None,
    ) -> list[dict[str, Any]]:
        """Получает самолеты из файла по указанному критерию."""

    @abstractmethod
    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Удаляет самолет из файла."""


class JSONSaver(AbstractSaver):
    """Класс для сохранения данных о самолетах в JSON-файл."""

    def __init__(self, file_path: str | Path = "data/aeroplanes.json") -> None:
        """Инициализирует путь к JSON-файлу."""
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf-8")

    def _read_data(self) -> list[dict[str, Any]]:
        """Считывает данные из JSON-файла."""
        try:
            with open(self.file_path, encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError, json.JSONDecodeError:
            return []

        if not isinstance(data, list):
            return []

        return data

    def _write_data(self, data: list[dict[str, Any]]) -> None:
        """Записывает данные в JSON-файл."""
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавляет самолет в JSON-файл."""
        data = self._read_data()
        data.append(aeroplane.to_dict())
        self._write_data(data)

    def get_aeroplanes(
        self,
        field_name: str | None = None,
        field_value: Any | None = None,
    ) -> list[dict[str, Any]]:
        """Получает самолеты из JSON-файла по указанному критерию."""
        data = self._read_data()

        if field_name is None:
            return data

        return [
            aeroplane for aeroplane in data if aeroplane.get(field_name) == field_value
        ]

    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Удаляет самолет из JSON-файла по ICAO24."""
        data = self._read_data()

        filtered_data = [
            item for item in data if item.get("icao24") != aeroplane.icao24
        ]

        self._write_data(filtered_data)
