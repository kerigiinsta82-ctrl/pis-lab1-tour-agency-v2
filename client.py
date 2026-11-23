"""Клиент туристической фирмы."""
import re


class Client:
    """Клиент туристической фирмы.

    Все поля приватные (двойное подчёркивание — name mangling),
    доступ снаружи только через свойства (property).
    Каждый сеттер проверяет значение, а конструктор заполняет поля
    через сеттеры, поэтому объект с недопустимыми полями создать нельзя.
    """

    def __init__(self, client_id, last_name, first_name, patronymic, address, phone, email):
        self.client_id = client_id
        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic
        self.address = address
        self.phone = phone
        self.email = email

    # ---------- валидация (статические методы) ----------

    NAME_PATTERN = r"[A-Za-zА-Яа-яЁё]+(-[A-Za-zА-Яа-яЁё]+)*"
    PHONE_PATTERN = r"(\+7|8)\d{10}"
    EMAIL_PATTERN = r"[\w.+-]+@[\w-]+(\.[\w-]+)+"

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
        return Client._validate_string(value, "last_name", 50, pattern=Client.NAME_PATTERN,
                                       pattern_msg="только буквы и дефис")

    @staticmethod
    def validate_first_name(value):
        return Client._validate_string(value, "first_name", 50, pattern=Client.NAME_PATTERN,
                                       pattern_msg="только буквы и дефис")

    @staticmethod
    def validate_patronymic(value):
        return Client._validate_string(value, "patronymic", 50, required=False,
                                       pattern=Client.NAME_PATTERN,
                                       pattern_msg="только буквы и дефис")

    @staticmethod
    def validate_address(value):
        return Client._validate_string(value, "address", 200, min_len=5)

    @staticmethod
    def validate_phone(value):
        if isinstance(value, str):
            value = re.sub(r"[\s()\-]", "", value)
        value = Client._validate_string(value, "phone", 12, pattern=Client.PHONE_PATTERN,
                                        pattern_msg="формат +7XXXXXXXXXX или 8XXXXXXXXXX")
        return "+7" + value[-10:]

    @staticmethod
    def validate_email(value):
        return Client._validate_string(value, "email", 100, required=False,
                                       pattern=Client.EMAIL_PATTERN,
                                       pattern_msg="некорректный адрес")

    # ---------- свойства ----------

    @property
    def client_id(self):
        return self.__client_id

    @client_id.setter
    def client_id(self, value):
        self.__client_id = Client.validate_client_id(value)

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        self.__last_name = Client.validate_last_name(value)

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        self.__first_name = Client.validate_first_name(value)

    @property
    def patronymic(self):
        return self.__patronymic

    @patronymic.setter
    def patronymic(self, value):
        self.__patronymic = Client.validate_patronymic(value)

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        self.__address = Client.validate_address(value)

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, value):
        self.__phone = Client.validate_phone(value)

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = Client.validate_email(value)
