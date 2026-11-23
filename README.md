# ПИС, ЛР1 — «Туристическая фирма» (тема 14)

Лабораторная работа №1: ER-модель предметной области и класс основной сущности на Python.

| Пункт | Где смотреть |
|---|---|
| 1. ER-модель (4 таблицы, 3НФ) | [docs/er_model.md](docs/er_model.md), [docs/schema.sql](docs/schema.sql) |
| 2. Выбор основной сущности — Клиент | [docs/er_model.md](docs/er_model.md#основная-сущность-для-лр1лр4-client-клиент) |
| 3. Класс `Client`, инкапсуляция полей | [client.py](client.py) |
| 4. Статические методы валидации | [client.py](client.py) — `validate_*` |
| 5. Устранение повтора кода в валидации | [client.py](client.py) — `_validate_string` |
| 6. Перегрузка конструктора (поля, словарь, JSON, строка) | [client.py](client.py) — `__init__`, `_parse_string` |
| 7. Полный и краткий вывод, сравнение на равенство | [client.py](client.py) — `__str__`, `short_str`, `__eq__` |
| 8. Краткий класс `ClientShort` | [client_short.py](client_short.py) |
| 9. Иерархия наследования `ClientShort` → `Client` без повтора кода | [client_short.py](client_short.py), [client.py](client.py) |
| 10. Диаграмма классов | [docs/class_diagram.md](docs/class_diagram.md), [docs/class_diagram.png](docs/class_diagram.png) |
