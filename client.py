"""Клиент туристической фирмы — полная версия."""
from client_short import ClientShort


class Client(ClientShort):
    """Полные данные клиента туристической фирмы.

    Наследует от ClientShort конструктор (все варианты вызова), валидацию,
    общие поля (номер, ФИО, телефон), краткий вывод и сравнение.
    Добавляет только свои поля — адрес и e-mail — и полный вывод.
    """

    FIELDS = ("client_id", "last_name", "first_name", "patronymic", "address", "phone", "email")
    OPTIONAL_FIELDS = ClientShort.OPTIONAL_FIELDS + ("email",)

    EMAIL_PATTERN = r"[\w.+-]+@[\w-]+(\.[\w-]+)+"

    def _fill(self, values):
        super()._fill(values)
        self.address = values["address"]
        self.email = values.get("email")

    def to_short(self):
        """Краткая версия этого клиента (объект базового класса)."""
        return ClientShort(**{field: getattr(self, field) for field in ClientShort.FIELDS})

    # ---------- валидация собственных полей ----------

    @staticmethod
    def validate_address(value):
        return ClientShort._validate_string(value, "address", 200, min_len=5)

    @staticmethod
    def validate_email(value):
        return ClientShort._validate_string(value, "email", 100, required=False,
                                            pattern=Client.EMAIL_PATTERN,
                                            pattern_msg="некорректный адрес")

    # ---------- свойства собственных полей ----------

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        self.__address = Client.validate_address(value)

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = Client.validate_email(value)

    # ---------- вывод ----------

    def __str__(self):
        """Полная версия объекта (переопределяет краткий вывод базового класса)."""
        return (f"Клиент №{self.client_id}: {self.full_name()}\n"
                f"  Адрес:   {self.address}\n"
                f"  Телефон: {self.phone}\n"
                f"  E-mail:  {self.email or '—'}")
