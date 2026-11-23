# Диаграмма классов

![Диаграмма классов](class_diagram.png)

PNG рисует скрипт `python tools/draw_diagrams.py`. Ниже та же диаграмма в формате
Mermaid (её показывает GitHub).

Обозначения: `+` public, `#` protected (`_имя`), `-` private (`__имя`),
`$` — статический член класса.

```mermaid
classDiagram
    direction LR
    ClientShort <|-- Client : наследует
    Client ..> ClientShort : «create» to_short()

    class ClientShort {
        +FIELDS$ tuple
        +OPTIONAL_FIELDS$ tuple
        +SEPARATOR$ str
        +NAME_PATTERN$ str
        +PHONE_PATTERN$ str
        -__client_id int
        -__last_name str
        -__first_name str
        -__patronymic str | None
        -__phone str
        +__init__(*args, **kwargs)
        #_collect_values(args, kwargs)$ dict
        #_parse_string(text)$ dict
        #_fill(values)
        #_validate_string(value, field, max_len, ...)$ str
        +validate_client_id(value)$ int
        +validate_last_name(value)$ str
        +validate_first_name(value)$ str
        +validate_patronymic(value)$ str | None
        +validate_phone(value)$ str
        +client_id «property» int
        +last_name «property» str
        +first_name «property» str
        +patronymic «property» str | None
        +phone «property» str
        +to_dict() dict
        +full_name() str
        +short_name() str
        +short_str() str
        +__str__() str
        +__repr__() str
        +__eq__(other) bool
    }

    class Client {
        +FIELDS$ tuple
        +OPTIONAL_FIELDS$ tuple
        +EMAIL_PATTERN$ str
        -__address str
        -__email str | None
        #_fill(values)
        +to_short() ClientShort
        +validate_address(value)$ str
        +validate_email(value)$ str | None
        +address «property» str
        +email «property» str | None
        +__str__() str
    }
```
