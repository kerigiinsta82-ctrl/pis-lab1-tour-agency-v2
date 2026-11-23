"""Тесты классов ClientShort и Client.

Запуск из корня проекта:  python -m unittest -v
"""
import json
import unittest

from client import Client
from client_short import ClientShort

FULL = dict(client_id=1, last_name="Иванов", first_name="Иван", patronymic="Иванович",
            address="г. Москва, ул. Ленина, д. 1", phone="+79161234567", email="ivanov@mail.ru")


class ConstructorTest(unittest.TestCase):
    def test_all_call_forms_give_equal_objects(self):
        expected = Client(**FULL)
        variants = [
            Client(*FULL.values()),
            Client(dict(FULL)),
            Client(json.dumps(FULL, ensure_ascii=False)),
            Client("1;Иванов;Иван;Иванович;г. Москва, ул. Ленина, д. 1;8 (916) 123-45-67;"
                   "ivanov@mail.ru"),
        ]
        for c in variants:
            self.assertEqual(c, expected)

    def test_optional_fields_may_be_omitted(self):
        c = Client(client_id=2, last_name="Петрова", first_name="Анна",
                   address="г. Казань, ул. Баумана, 5", phone="89031112233")
        self.assertIsNone(c.patronymic)
        self.assertIsNone(c.email)
        self.assertEqual(c.phone, "+79031112233")

    def test_wrong_arguments(self):
        with self.assertRaises(TypeError):
            Client(1, "Иванов")                       # не все обязательные поля
        with self.assertRaises(TypeError):
            Client(1, client_id=2)                    # поле передано дважды
        with self.assertRaises(TypeError):
            Client({**FULL, "age": 30})               # неизвестное поле
        with self.assertRaises(ValueError):
            Client("1;Иванов;Иван")                   # мало полей в строке
        with self.assertRaises(ValueError):
            Client("{не json")


class ValidationTest(unittest.TestCase):
    BAD = {
        "client_id": [0, -5, "1", True, 1.5],
        "last_name": ["", "   ", "Ив4нов", "-Иванов", "И" * 51, None],
        "first_name": ["", "John!", None],
        "patronymic": ["Иван0вич", 5],
        "address": ["", "abc", "x" * 201, None],
        "phone": ["", "123", "+7916123456", "+19161234567", None],
        "email": ["a@b", "no-at.ru", "a b@c.ru", 5],
    }

    def test_invalid_values_rejected_in_constructor(self):
        for field, values in self.BAD.items():
            for value in values:
                with self.subTest(field=field, value=value):
                    with self.assertRaises((ValueError, TypeError)):
                        Client(**{**FULL, field: value})

    def test_invalid_value_rejected_in_setter_and_object_unchanged(self):
        c = Client(**FULL)
        with self.assertRaises(ValueError):
            c.phone = "abc"
        self.assertEqual(c.phone, "+79161234567")

    def test_normalization(self):
        c = Client(**{**FULL, "last_name": "  Иванов ", "patronymic": "", "email": " ",
                      "phone": "8 916 123 45 67"})
        self.assertEqual(c.last_name, "Иванов")
        self.assertIsNone(c.patronymic)
        self.assertIsNone(c.email)
        self.assertEqual(c.phone, "+79161234567")

    def test_static_validators_callable_without_object(self):
        self.assertEqual(Client.validate_phone("8(916)1234567"), "+79161234567")
        self.assertEqual(ClientShort.validate_last_name("Салтыков-Щедрин"), "Салтыков-Щедрин")

    def test_fields_are_private(self):
        c = Client(**FULL)
        with self.assertRaises(AttributeError):
            c.__phone  # noqa: B018 — проверяем, что прямого доступа нет


class OutputAndEqualityTest(unittest.TestCase):
    def test_full_and_short_output(self):
        c = Client(**FULL)
        self.assertIn("Иванов Иван Иванович", str(c))
        self.assertIn("г. Москва", str(c))
        self.assertEqual(c.short_str(), "Иванов И. И., тел. +79161234567")

    def test_equality(self):
        self.assertEqual(Client(**FULL), Client(**FULL))
        self.assertNotEqual(Client(**FULL), Client(**{**FULL, "client_id": 2}))
        self.assertNotEqual(Client(**FULL), "Иванов")


class HierarchyTest(unittest.TestCase):
    def test_client_is_client_short(self):
        self.assertTrue(issubclass(Client, ClientShort))
        self.assertIsInstance(Client(**FULL), ClientShort)

    def test_short_version(self):
        s = Client(**FULL).to_short()
        self.assertIs(type(s), ClientShort)
        self.assertEqual(str(s), "Иванов И. И., тел. +79161234567")
        self.assertEqual(s, ClientShort("1;Иванов;Иван;Иванович;89161234567"))
        self.assertFalse(hasattr(s, "address"))
        self.assertNotEqual(s, Client(**FULL))  # разные классы — не равны

    def test_no_duplicated_methods_in_child(self):
        own = set(vars(Client))
        for name in ("__init__", "_parse_string", "validate_phone", "short_str", "__eq__",
                     "phone", "last_name"):
            self.assertNotIn(name, own, f"{name} должен наследоваться, а не дублироваться")


if __name__ == "__main__":
    unittest.main()
