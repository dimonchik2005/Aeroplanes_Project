import json
from pathlib import Path
from typing import Any

import pytest

from aeroplanes_project.aeroplane import Aeroplane
from aeroplanes_project.saver import AbstractSaver, JSONSaver


def test_abstract_saver_cannot_be_created() -> None:
    """Проверяет, что AbstractSaver нельзя создать напрямую."""
    with pytest.raises(TypeError):
        AbstractSaver()  # type: ignore[abstract]


def test_json_saver_creates_file(tmp_path: Path) -> None:
    """Проверяет создание JSON-файла."""
    file_path = tmp_path / "aeroplanes.json"

    JSONSaver(file_path)

    assert file_path.exists()
    assert file_path.read_text(encoding="utf-8") == "[]"


def test_add_aeroplane(tmp_path: Path) -> None:
    """Проверяет добавление самолета в JSON-файл."""
    file_path = tmp_path / "aeroplanes.json"
    saver = JSONSaver(file_path)
    aeroplane = Aeroplane("4b1812", "SWR438A", "Switzerland", 189.7, 4267.2)

    saver.add_aeroplane(aeroplane)

    with open(file_path, encoding="utf-8") as file:
        data = json.load(file)

    assert len(data) == 1
    assert data[0]["icao24"] == "4b1812"
    assert data[0]["callsign"] == "SWR438A"


def test_get_all_aeroplanes(tmp_path: Path) -> None:
    """Проверяет получение всех самолетов из JSON-файла."""
    file_path = tmp_path / "aeroplanes.json"
    saver = JSONSaver(file_path)
    aeroplane = Aeroplane("4b1812", "SWR438A", "Switzerland", 189.7, 4267.2)

    saver.add_aeroplane(aeroplane)

    result = saver.get_aeroplanes()

    assert len(result) == 1
    assert result[0]["origin_country"] == "Switzerland"


def test_get_aeroplanes_by_country(tmp_path: Path) -> None:
    """Проверяет фильтрацию самолетов по стране регистрации."""
    file_path = tmp_path / "aeroplanes.json"
    saver = JSONSaver(file_path)

    aeroplane1 = Aeroplane("4b1812", "SWR438A", "Switzerland", 189.7, 4267.2)
    aeroplane2 = Aeroplane("abc123", "TEST", "Canada", 250.0, 3000.0)

    saver.add_aeroplane(aeroplane1)
    saver.add_aeroplane(aeroplane2)

    result = saver.get_aeroplanes("origin_country", "Canada")

    assert len(result) == 1
    assert result[0]["icao24"] == "abc123"


def test_delete_aeroplane(tmp_path: Path) -> None:
    """Проверяет удаление самолета из JSON-файла."""
    file_path = tmp_path / "aeroplanes.json"
    saver = JSONSaver(file_path)

    aeroplane1 = Aeroplane("4b1812", "SWR438A", "Switzerland", 189.7, 4267.2)
    aeroplane2 = Aeroplane("abc123", "TEST", "Canada", 250.0, 3000.0)

    saver.add_aeroplane(aeroplane1)
    saver.add_aeroplane(aeroplane2)
    saver.delete_aeroplane(aeroplane1)

    result = saver.get_aeroplanes()

    assert len(result) == 1
    assert result[0]["icao24"] == "abc123"


def test_read_invalid_json(tmp_path: Path) -> None:
    """Проверяет обработку некорректного JSON."""
    file_path = tmp_path / "aeroplanes.json"
    file_path.write_text("invalid json", encoding="utf-8")

    saver = JSONSaver(file_path)

    assert saver.get_aeroplanes() == []


def test_read_not_list_json(tmp_path: Path) -> None:
    """Проверяет обработку JSON, который не является списком."""
    file_path = tmp_path / "aeroplanes.json"
    data: dict[str, Any] = {"icao24": "4b1812"}

    file_path.write_text(json.dumps(data), encoding="utf-8")

    saver = JSONSaver(file_path)

    assert saver.get_aeroplanes() == []