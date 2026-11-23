-- Предметная область «Туристическая фирма» (тема 14)
-- Все таблицы приведены к третьей нормальной форме (3НФ).

CREATE TABLE country (
    country_id   SERIAL       PRIMARY KEY,
    name         VARCHAR(100) NOT NULL UNIQUE,
    climate      VARCHAR(255) NOT NULL              -- особенности местного климата
);

CREATE TABLE hotel (
    hotel_id     SERIAL       PRIMARY KEY,
    country_id   INTEGER      NOT NULL REFERENCES country (country_id),
    name         VARCHAR(150) NOT NULL,
    stars        SMALLINT     NOT NULL CHECK (stars BETWEEN 1 AND 5),  -- класс отеля
    UNIQUE (country_id, name)
);

CREATE TABLE client (
    client_id    SERIAL       PRIMARY KEY,
    last_name    VARCHAR(50)  NOT NULL,
    first_name   VARCHAR(50)  NOT NULL,
    patronymic   VARCHAR(50),                       -- отчества может не быть
    address      VARCHAR(200) NOT NULL,
    phone        VARCHAR(12)  NOT NULL UNIQUE,      -- формат +7XXXXXXXXXX
    email        VARCHAR(100) UNIQUE                -- необязательное поле
);

CREATE TABLE voucher (
    voucher_id       SERIAL        PRIMARY KEY,
    client_id        INTEGER       NOT NULL REFERENCES client (client_id),
    hotel_id         INTEGER       NOT NULL REFERENCES hotel (hotel_id),
    sale_date        DATE          NOT NULL,
    departure_date   DATE          NOT NULL,
    duration_days    SMALLINT      NOT NULL CHECK (duration_days > 0),
    price            NUMERIC(10,2) NOT NULL CHECK (price > 0),
    discount_percent NUMERIC(5,2)  NOT NULL DEFAULT 0 CHECK (discount_percent BETWEEN 0 AND 100),
    CHECK (departure_date >= sale_date)
);
