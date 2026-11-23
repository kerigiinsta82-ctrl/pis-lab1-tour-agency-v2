"""Собирает lab1.ipynb для Google Colab из исходников проекта.

Код классов берётся прямо из client_short.py и client.py, поэтому ноутбук
всегда совпадает с репозиторием. Картинки подгружаются по прямым ссылкам
из публичного репозитория на GitHub: Colab, открывающий ноутбук с GitHub,
не показывает вложения ячеек.

Запуск:  python tools/build_notebook.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = "https://raw.githubusercontent.com/kerigiinsta82-ctrl/pis-lab1-tour-agency-v2/main/docs/"


def src(name):
    return (ROOT / name).read_text(encoding="utf-8")


def image(name):
    """Картинка из папки docs репозитория на GitHub."""
    return f"![{name}]({RAW}{name})"


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.strip("\n")}


def code(text):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
            "source": text.strip("\n")}


client_code = src("client.py").replace("from client_short import ClientShort\n", "")

cells = [
    md("""
# ПИС, ЛР1 — «Туристическая фирма» (тема 14)

Основная сущность — **Клиент**. Чтобы всё показать, выполните ячейки по порядку
(в Colab: *Среда выполнения → Выполнить все*).
"""),
    md("## П.1. ER-модель (4 таблицы в 3НФ)\n\n" + image("er_diagram.png") + """

* **1НФ:** все атрибуты атомарны (ФИО разбито на 3 поля), повторяющихся групп нет.
* **2НФ:** ключи простые (суррогатные `*_id`), частичных зависимостей нет.
* **3НФ:** нет транзитивных зависимостей: климат хранится в `country`, класс отеля — в `hotel`,
  в `voucher` только ссылки на клиента и отель.
"""),
    md("""
## П.2. Основная сущность — `client`

Независимые сущности (без внешних ключей): `country` (3 поля) и `client` (7 полей).
У клиента полей больше, поэтому ЛР1–ЛР4 делаются с ним.
"""),
    md("""
## П.3–П.9. Классы

Базовый класс `ClientShort` — краткая версия клиента. В нём всё общее: инкапсуляция полей
(п.3), статические методы валидации (п.4) с общим `_validate_string` без повторов (п.5),
перегруженный конструктор (п.6), вывод и сравнение (п.7).
"""),
    code(src("client_short.py")),
    md("Наследник `Client` — полная версия (п.8–9): добавляет только адрес, e-mail и полный вывод."),
    code(client_code),
    md("## П.3. Инкапсуляция: поля приватные, доступ через свойства"),
    code("""
c = Client(1, "Иванов", "Иван", "Иванович", "г. Москва, ул. Ленина, д. 1",
           "+79161234567", "ivanov@mail.ru")
print(c.last_name, c.phone)           # через свойства — можно
try:
    print(c.__phone)                  # напрямую — нельзя
except AttributeError as e:
    print("AttributeError:", e)
print(vars(c))                        # имена полей «искажены» (name mangling)
"""),
    md("## П.4–5. Валидация: объект с недопустимыми полями создать нельзя"),
    code("""
print(Client.validate_phone("8 (916) 123-45-67"))   # статический метод — без объекта

bad_cases = {
    "client_id": 0,
    "last_name": "Ив4нов",
    "address": "abc",
    "phone": "12345",
    "email": "not-an-email",
}
for field, value in bad_cases.items():
    data = c.to_dict()
    data[field] = value
    try:
        Client(data)
        print("создан?!", field)
    except (ValueError, TypeError) as e:
        print(f"{type(e).__name__}: {e}")

try:
    c.email = "bad@"                  # сеттер тоже проверяет
except ValueError as e:
    print("сеттер:", e)
print("e-mail не изменился:", c.email)
"""),
    md("## П.6. Перегрузка конструктора"),
    code("""
by_fields = Client(1, "Иванов", "Иван", "Иванович", "г. Москва, ул. Ленина, д. 1",
                   "+79161234567", "ivanov@mail.ru")
by_kwargs = Client(client_id=2, last_name="Петрова", first_name="Анна",
                   address="г. Казань, ул. Баумана, 5", phone="89031112233")
by_dict = Client({"client_id": 3, "last_name": "Смирнов", "first_name": "Олег",
                  "address": "г. Сочи, ул. Морская, 3", "phone": "+79001234567"})
by_json = Client('{"client_id": 4, "last_name": "Кузнецова", "first_name": "Мария", '
                 '"patronymic": "Петровна", "address": "г. Тверь, пр. Мира, 10", '
                 '"phone": "8 912 000 11 22", "email": "mk@ya.ru"}')
by_string = Client("5;Орлов;Денис;;г. Пермь, ул. Ленина, 50;+79125556677;")

for client in (by_fields, by_kwargs, by_dict, by_json, by_string):
    print(repr(client))
"""),
    md("## П.7. Полный и краткий вывод, сравнение"),
    code("""
print(by_json)                 # полная версия
print(by_json.short_str())     # краткая версия

same = Client("1;Иванов;Иван;Иванович;г. Москва, ул. Ленина, д. 1;8 916 123 45 67;"
              "ivanov@mail.ru")
print("by_fields == same:     ", by_fields == same)
print("by_fields == by_kwargs:", by_fields == by_kwargs)
"""),
    md("## П.8–9. Краткий класс и иерархия наследования"),
    code("""
short = by_fields.to_short()
print(type(short).__name__, "->", short)
print(repr(short))
print("Client — наследник ClientShort:", issubclass(Client, ClientShort))
print("MRO:", [cls.__name__ for cls in Client.__mro__])

# краткий клиент создаётся теми же способами, что и полный — код не дублируется
print(ClientShort("7;Белов;Илья;Сергеевич;+79007654321"))

# методы, которые Client берёт у родителя, а не определяет заново
inherited = [m for m in ("__init__", "_parse_string", "validate_phone", "short_str", "__eq__")
             if m not in vars(Client)]
print("унаследованы:", inherited)
"""),
    md("## П.10. Диаграмма классов\n\n" + image("class_diagram.png")),
]

nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "colab": {"provenance": []},
        "kernelspec": {"name": "python3", "display_name": "Python 3"},
        "language_info": {"name": "python"},
    },
    "cells": cells,
}
for i, cell in enumerate(nb["cells"]):
    cell["id"] = f"cell-{i}"
    cell["source"] = cell["source"].splitlines(keepends=True)

(ROOT / "lab1.ipynb").write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n",
                                 encoding="utf-8")
print("lab1.ipynb:", len(cells), "ячеек")
