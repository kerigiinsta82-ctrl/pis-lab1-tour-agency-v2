"""Клиент туристической фирмы."""


class Client:
    """Клиент туристической фирмы.

    Все поля приватные (двойное подчёркивание — name mangling),
    доступ снаружи только через свойства (property).
    """

    def __init__(self, client_id, last_name, first_name, patronymic, address, phone, email):
        self.__client_id = client_id
        self.__last_name = last_name
        self.__first_name = first_name
        self.__patronymic = patronymic
        self.__address = address
        self.__phone = phone
        self.__email = email

    @property
    def client_id(self):
        return self.__client_id

    @client_id.setter
    def client_id(self, value):
        self.__client_id = value

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        self.__last_name = value

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        self.__first_name = value

    @property
    def patronymic(self):
        return self.__patronymic

    @patronymic.setter
    def patronymic(self, value):
        self.__patronymic = value

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        self.__address = value

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, value):
        self.__phone = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = value
