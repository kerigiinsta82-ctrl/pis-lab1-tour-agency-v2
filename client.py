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

    @staticmethod
    def validate_client_id(value):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("client_id: ожидается целое число")
        if value <= 0:
            raise ValueError("client_id: должен быть положительным")
        return value

    @staticmethod
    def validate_last_name(value):
        if not isinstance(value, str):
            raise TypeError("last_name: ожидается строка")
        value = value.strip()
        if not value:
            raise ValueError("last_name: не может быть пустым")
        if len(value) > 50:
            raise ValueError("last_name: не длиннее 50 символов")
        if not re.fullmatch(r"[A-Za-zА-Яа-яЁё]+(-[A-Za-zА-Яа-яЁё]+)*", value):
            raise ValueError("last_name: только буквы и дефис")
        return value

    @staticmethod
    def validate_first_name(value):
        if not isinstance(value, str):
            raise TypeError("first_name: ожидается строка")
        value = value.strip()
        if not value:
            raise ValueError("first_name: не может быть пустым")
        if len(value) > 50:
            raise ValueError("first_name: не длиннее 50 символов")
        if not re.fullmatch(r"[A-Za-zА-Яа-яЁё]+(-[A-Za-zА-Яа-яЁё]+)*", value):
            raise ValueError("first_name: только буквы и дефис")
        return value

    @staticmethod
    def validate_patronymic(value):
        if value is None:
            return None
        if not isinstance(value, str):
            raise TypeError("patronymic: ожидается строка или None")
        value = value.strip()
        if not value:
            return None
        if len(value) > 50:
            raise ValueError("patronymic: не длиннее 50 символов")
        if not re.fullmatch(r"[A-Za-zА-Яа-яЁё]+(-[A-Za-zА-Яа-яЁё]+)*", value):
            raise ValueError("patronymic: только буквы и дефис")
        return value

    @staticmethod
    def validate_address(value):
        if not isinstance(value, str):
            raise TypeError("address: ожидается строка")
        value = value.strip()
        if not value:
            raise ValueError("address: не может быть пустым")
        if len(value) > 200:
            raise ValueError("address: не длиннее 200 символов")
        if len(value) < 5:
            raise ValueError("address: слишком короткий")
        return value

    @staticmethod
    def validate_phone(value):
        if not isinstance(value, str):
            raise TypeError("phone: ожидается строка")
        value = re.sub(r"[\s()\-]", "", value)
        if not value:
            raise ValueError("phone: не может быть пустым")
        if not re.fullmatch(r"(\+7|8)\d{10}", value):
            raise ValueError("phone: формат +7XXXXXXXXXX или 8XXXXXXXXXX")
        return "+7" + value[-10:]

    @staticmethod
    def validate_email(value):
        if value is None:
            return None
        if not isinstance(value, str):
            raise TypeError("email: ожидается строка или None")
        value = value.strip()
        if not value:
            return None
        if len(value) > 100:
            raise ValueError("email: не длиннее 100 символов")
        if not re.fullmatch(r"[\w.+-]+@[\w-]+(\.[\w-]+)+", value):
            raise ValueError("email: некорректный адрес")
        return value

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
