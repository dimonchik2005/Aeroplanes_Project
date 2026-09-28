from aeroplanes_project.aeroplane import Aeroplane
from aeroplanes_project.api import AeroplanesAPI
from aeroplanes_project.saver import JSONSaver
from aeroplanes_project.utils import (filter_aeroplanes_by_country,
                                      get_top_aeroplanes, print_aeroplanes,
                                      sort_aeroplanes_by_altitude)


def user_interaction() -> None:
    """Запускает консольное взаимодействие с пользователем."""
    api = AeroplanesAPI()
    saver = JSONSaver()

    country = input("Введите название страны для поиска самолетов: ")

    try:
        data = api.get_aeroplanes(country)
    except Exception as error:
        print(f"Ошибка при получении данных: {error}")
        return

    aeroplanes = Aeroplane.cast_to_object_list(data)

    if not aeroplanes:
        print("Самолеты не найдены")
        return

    for aeroplane in aeroplanes:
        saver.add_aeroplane(aeroplane)

    print(f"Найдено самолетов: {len(aeroplanes)}")

    filter_country = input(
        "Введите страну регистрации для фильтрации или нажмите Enter: "
    )

    filtered_aeroplanes = filter_aeroplanes_by_country(
        aeroplanes,
        filter_country,
    )

    sorted_aeroplanes = sort_aeroplanes_by_altitude(filtered_aeroplanes)

    try:
        top_n = int(input("Введите количество самолетов для топа по высоте: "))
    except ValueError:
        print("Некорректное число, будет показан топ 5")
        top_n = 5

    top_aeroplanes = get_top_aeroplanes(sorted_aeroplanes, top_n)

    print("Результат:")
    print_aeroplanes(top_aeroplanes)


if __name__ == "__main__":
    user_interaction()
