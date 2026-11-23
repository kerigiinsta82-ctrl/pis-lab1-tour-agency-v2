# ПИС, ЛР1 — «Туристическая фирма» (тема 14)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kerigiinsta82-ctrl/pis-lab1-tour-agency-v2/blob/main/lab1.ipynb)

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

Ответы на теоретические вопросы: [docs/answers.md](docs/answers.md).

## Показ в Google Colab

[lab1.ipynb](lab1.ipynb) — ноутбук со всеми пунктами по порядку: код классов и демонстрация.
Код в нём самодостаточный, картинки подгружаются из этого репозитория на GitHub.

1. Нажмите кнопку **Open in Colab** вверху или откройте ссылку:
   <https://colab.research.google.com/github/kerigiinsta82-ctrl/pis-lab1-tour-agency-v2/blob/main/lab1.ipynb>.
   Можно и вручную: **Файл → Загрузить блокнот** → `lab1.ipynb`.
2. **Среда выполнения → Выполнить все.**

Ноутбук собирается из исходников командой `python tools/build_notebook.py`. После изменения
классов пересоберите его, чтобы код в ноутбуке совпадал с `.py` файлами.

## Запуск локально

```
python -m unittest -v           # тесты
python tools/draw_diagrams.py   # перерисовать диаграммы (нужен Pillow)
```
