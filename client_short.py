"""Краткая версия клиента — базовый класс иерархии клиентов туристической фирмы."""
import json
import re


class ClientShort:
    """Краткие данные клиента: номер, ФИО (выводится с инициалами) и один контакт — телефон.

    Базовый класс иерархии: здесь всё общее для краткой и полной версии —
    перегруженный конструктор, разбор строк и JSON, валидация, общие поля,
    краткий вывод и сравнение. Наследник добавляет только свои поля.

    Все поля приватные, доступ только через свойства. Сеттеры проверяют значения,
    конструктор заполняет поля через сеттеры, поэтому объект с недопустимыми
    полями создать нельзя.
    """

    FIELDS = ("client_id", "last_name", "first_name", "patronymic", "phone")
    OPTIONAL_FIELDS = ("patronymic",)
    SEPARATOR = ";"

    NAME_PATTERN = r"[A-Za-zА-Яа-яЁё]+(-[A-Za-zА-Яа-яЁё]+)*"
    PHONE_PATTERN = r"(\+7|8)\d{10}"

    def __init__(self, *args, **kwargs):
        """Перегруженный конструктор. Варианты вызова (поля — в порядке FIELDS):

        ClientShort(1, "Иванов", "Иван", "Иванович", "+79161234567")
        ClientShort(client_id=1, last_name="Иванов", ...)          — именованные аргументы
        ClientShort({"client_id": 1, "last_name": "Иванов", ...})  — словарь
        ClientShort('{"client_id": 1, "last_name": "Иванов", ...}') — JSON-строка
        ClientShort("1;Иванов;Иван;Иванович;+79161234567")          — строка через «;»

        Необязательные поля (OPTIONAL_FIELDS) можно не передавать.
        Наследники получают все эти варианты вызова без изменений.
        """
        self._fill(self._collect_values(args, kwargs))

    @classmethod
    def _collect_values(cls, args, kwargs):
        """Приводит любой вариант вызова конструктора к словарю {поле: значение}."""
        if len(args) == 1 and not kwargs and isinstance(args[0], (str, dict)):
            data = args[0]
            values = cls._parse_string(data) if isinstance(data, str) else dict(data)
        else:
            if len(args) > len(cls.FIELDS):
                raise TypeError(f"слишком много аргументов: {len(args)}")
            values = dict(zip(cls.FIELDS, args))
            for key, value in kwargs.items():
                if key in values:
                    raise TypeError(f"{key}: значение передано дважды")
                values[key] = value

        unknown = set(values) - set(cls.FIELDS)
        if unknown:
            raise TypeError(f"неизвестные поля: {', '.join(sorted(unknown))}")
        missing = [f for f in cls.FIELDS if f not in values and f not in cls.OPTIONAL_FIELDS]
        if missing:
            raise TypeError(f"не заданы обязательные поля: {', '.join(missing)}")
        return values

    @classmethod
    def _parse_string(cls, text):
        """Разбирает JSON-объект или строку с полями через SEPARATOR в словарь."""
        text = text.strip()
        if text.startswith("{"):
            try:
                data = json.loads(text)
            except json.JSONDecodeError as e:
                raise ValueError(f"некорректный JSON: {e}") from None
            if not isinstance(data, dict):
                raise ValueError("JSON должен описывать объект")
            return data

        parts = [p.strip() for p in text.split(cls.SEPARATOR)]
        if len(parts) != len(cls.FIELDS):
            raise ValueError(f"в строке должно быть {len(cls.FIELDS)} полей через "
                             f"«{cls.SEPARATOR}», а не {len(parts)}")
        values = dict(zip(cls.FIELDS, parts))
        if values["client_id"].isdigit():
            values["client_id"] = int(values["client_id"])
        return values

    def _fill(self, values):
        """Заполняет поля через сеттеры (а значит, с проверкой).

        Наследник переопределяет метод и вызывает super()._fill(values).
        """
        self.client_id = values["client_id"]
        self.last_name = values["last_name"]
        self.first_name = values["first_name"]
        self.patronymic = values.get("patronymic")
        self.phone = values["phone"]

    # ---------- валидация (статические методы) ----------

    @staticmethod
    def _validate_string(value, field, max_len, *, required=True, min_len=1,
                         pattern=None, pattern_msg="неверный формат"):
        """Общая проверка строкового поля.

        Обрезает пробелы по краям. Необязательное поле (required=False)
        может быть None или пустой строкой — тогда возвращается None.
        """
        if value is None and not required:
            return None
        if not isinstance(value, str):
            raise TypeError(f"{field}: ожидается строка" + ("" if required else " или None"))
        value = value.strip()
        if not value:
            if not required:
                return None
            raise ValueError(f"{field}: не может быть пустым")
        if len(value) < min_len:
            raise ValueError(f"{field}: не короче {min_len} символов")
        if len(value) > max_len:
            raise ValueError(f"{field}: не длиннее {max_len} символов")
        if pattern and not re.fullmatch(pattern, value):
            raise ValueError(f"{field}: {pattern_msg}")
        return value

    @staticmethod
    def validate_client_id(value):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("client_id: ожидается целое число")
        if value <= 0:
            raise ValueError("client_id: должен быть положительным")
        return value

    @staticmethod
    def validate_last_name(value):
        return ClientShort._validate_string(value, "last_name", 50,
                                            pattern=ClientShort.NAME_PATTERN,
                                            pattern_msg="только буквы и дефис")

    @staticmethod
    def validate_first_name(value):
        return ClientShort._validate_string(value, "first_name", 50,
                                            pattern=ClientShort.NAME_PATTERN,
                                            pattern_msg="только буквы и дефис")

    @staticmethod
    def validate_patronymic(value):
        return ClientShort._validate_string(value, "patronymic", 50, required=False,
                                            pattern=ClientShort.NAME_PATTERN,
                                            pattern_msg="только буквы и дефис")

    @staticmethod
    def validate_phone(value):
        if isinstance(value, str):
            value = re.sub(r"[\s()\-]", "", value)
        value = ClientShort._validate_string(value, "phone", 12,
                                             pattern=ClientShort.PHONE_PATTERN,
                                             pattern_msg="формат +7XXXXXXXXXX или 8XXXXXXXXXX")
        return "+7" + value[-10:]

    # ---------- свойства ----------

    @property
    def client_id(self):
        return self.__client_id

    @client_id.setter
    def client_id(self, value):
        self.__client_id = ClientShort.validate_client_id(value)

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        self.__last_name = ClientShort.validate_last_name(value)

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        self.__first_name = ClientShort.validate_first_name(value)

    @property
    def patronymic(self):
        return self.__patronymic

    @patronymic.setter
    def patronymic(self, value):
        self.__patronymic = ClientShort.validate_patronymic(value)

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, value):
        self.__phone = ClientShort.validate_phone(value)

    # ---------- вывод и сравнение ----------

    def to_dict(self):
        """Все поля объекта в виде словаря (в порядке FIELDS своего класса)."""
        return {field: getattr(self, field) for field in self.FIELDS}

    def full_name(self):
        """Фамилия Имя Отчество (без отчества, если его нет)."""
        return " ".join(p for p in (self.last_name, self.first_name, self.patronymic) if p)

    def short_name(self):
        """Фамилия и инициалы: «Иванов И. И.»."""
        initials = " ".join(f"{p[0]}." for p in (self.first_name, self.patronymic) if p)
        return f"{self.last_name} {initials}"

    def short_str(self):
        """Краткая версия объекта: ФИО с инициалами и один контакт."""
        return f"{self.short_name()}, тел. {self.phone}"

    def __str__(self):
        """У краткой версии полный вывод совпадает с кратким."""
        return self.short_str()

    def __repr__(self):
        args = ", ".join(f"{k}={v!r}" for k, v in self.to_dict().items())
        return f"{type(self).__name__}({args})"

    def __eq__(self, other):
        """Равны объекты одного и того же класса с одинаковыми полями."""
        if type(other) is not type(self):
            return NotImplemented
        return self.to_dict() == other.to_dict()
