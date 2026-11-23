"""Краткая версия клиента туристической фирмы."""
from client import Client


class ClientShort:
    """Краткие данные клиента: номер, ФИО (выводится с инициалами) и один контакт — телефон.

    Адреса и e-mail нет. Поля проверяются теми же статическими методами, что и в Client.
    """

    def __init__(self, client_id, last_name, first_name, patronymic, phone):
        self.client_id = client_id
        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic
        self.phone = phone

    @classmethod
    def from_client(cls, client):
        """Краткая версия существующего полного клиента."""
        return cls(client.client_id, client.last_name, client.first_name,
                   client.patronymic, client.phone)

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
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, value):
        self.__phone = Client.validate_phone(value)

    def short_name(self):
        """Фамилия и инициалы: «Иванов И. И.»."""
        initials = " ".join(f"{p[0]}." for p in (self.first_name, self.patronymic) if p)
        return f"{self.last_name} {initials}"

    def __str__(self):
        return f"{self.short_name()}, тел. {self.phone}"

    def __repr__(self):
        return (f"ClientShort(client_id={self.client_id!r}, last_name={self.last_name!r}, "
                f"first_name={self.first_name!r}, patronymic={self.patronymic!r}, "
                f"phone={self.phone!r})")

    def __eq__(self, other):
        if type(other) is not type(self):
            return NotImplemented
        return (self.client_id, self.last_name, self.first_name, self.patronymic, self.phone) == \
               (other.client_id, other.last_name, other.first_name, other.patronymic, other.phone)
