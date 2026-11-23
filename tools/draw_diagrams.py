"""Рисует диаграммы проекта в PNG (нужен только Pillow).

Запуск:  python tools/draw_diagrams.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

DOCS = Path(__file__).resolve().parent.parent / "docs"
FONT_DIR = Path("C:/Windows/Fonts")

INK = (40, 40, 40)
HEAD_BG = (31, 78, 121)
BODY_BG = (245, 248, 252)
KEY = (176, 96, 0)


def font(name, size):
    for candidate in (FONT_DIR / name, Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")):
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


TITLE = font("arialbd.ttf", 22)
TEXT = font("consola.ttf", 17)
SMALL = font("arial.ttf", 16)


class Box:
    """Прямоугольник-сущность: заголовок и одна или несколько секций строк."""

    LINE_H = 24
    PAD = 12

    def __init__(self, x, y, title, sections, width=None, subtitle=None):
        self.x, self.y, self.title, self.sections, self.subtitle = x, y, title, sections, subtitle
        widths = [TITLE.getlength(title)] + [TEXT.getlength(s) for sec in sections for s in sec]
        self.w = width or int(max(widths)) + 2 * self.PAD
        head = 40 + (22 if subtitle else 0)
        self.head_h = head
        self.h = head + sum(len(sec) * self.LINE_H + self.PAD for sec in sections)

    def draw(self, d):
        x, y, w = self.x, self.y, self.w
        d.rectangle([x, y, x + w, y + self.h], fill=BODY_BG, outline=INK, width=2)
        d.rectangle([x, y, x + w, y + self.head_h], fill=HEAD_BG, outline=INK, width=2)
        if self.subtitle:
            d.text((x + w / 2, y + 16), self.subtitle, font=SMALL, fill="white", anchor="mm")
        d.text((x + w / 2, y + self.head_h - 20), self.title, font=TITLE, fill="white",
               anchor="mm")
        cy = y + self.head_h
        for i, sec in enumerate(self.sections):
            if i:
                d.line([x, cy, x + w, cy], fill=INK, width=2)
            cy += self.PAD // 2
            for s in sec:
                color = KEY if (" PK" in s or " FK" in s) else INK
                d.text((x + self.PAD, cy), s, font=TEXT, fill=color)
                cy += self.LINE_H
            cy += self.PAD // 2

    # точки на серединах сторон
    def top(self):
        return self.x + self.w / 2, self.y

    def bottom(self):
        return self.x + self.w / 2, self.y + self.h

    def left(self):
        return self.x, self.y + self.h / 2

    def right(self):
        return self.x + self.w, self.y + self.h / 2


def crow_link(d, a, b, label, a_side, b_side):
    """Связь 1:N: черта «один» у a, «воронья лапка» у b."""
    (x1, y1), (x2, y2) = a, b
    d.line([x1, y1, x2, y2], fill=INK, width=2)
    # «один» — поперечная черта у a
    if a_side in ("right", "left"):
        sx = x1 + (14 if a_side == "right" else -14)
        d.line([sx, y1 - 9, sx, y1 + 9], fill=INK, width=2)
    else:
        sy = y1 + (14 if a_side == "bottom" else -14)
        d.line([x1 - 9, sy, x1 + 9, sy], fill=INK, width=2)
    # «много» — лапка у b
    if b_side in ("left", "right"):
        bx = x2 + (-16 if b_side == "left" else 16)
        for dy in (-10, 0, 10):
            d.line([bx, y2, x2, y2 + dy], fill=INK, width=2)
    else:
        by = y2 + (-16 if b_side == "top" else 16)
        for dx in (-10, 0, 10):
            d.line([x2, by, x2 + dx, y2], fill=INK, width=2)
    d.text(((x1 + x2) / 2, (y1 + y2) / 2 - 14), label, font=SMALL, fill=INK, anchor="mm")


def draw_er():
    img = Image.new("RGB", (1160, 580), "white")
    d = ImageDraw.Draw(img)
    country = Box(40, 40, "country (Страна)",
                  [["country_id  INT PK", "name        VARCHAR", "climate     VARCHAR"]])
    hotel = Box(40, 300, "hotel (Отель)",
                [["hotel_id    INT PK", "country_id  INT FK", "name        VARCHAR",
                  "stars       SMALLINT"]])
    voucher = Box(440, 260, "voucher (Путёвка)",
                  [["voucher_id        INT PK", "client_id         INT FK",
                    "hotel_id          INT FK", "sale_date         DATE",
                    "departure_date    DATE", "duration_days     SMALLINT",
                    "price             NUMERIC", "discount_percent  NUMERIC"]])
    client = Box(840, 40, "client (Клиент)",
                 [["client_id   INT PK", "last_name   VARCHAR", "first_name  VARCHAR",
                   "patronymic  VARCHAR?", "address     VARCHAR", "phone       VARCHAR",
                   "email       VARCHAR?"]])
    for b in (country, hotel, voucher, client):
        b.draw(d)
    crow_link(d, country.bottom(), hotel.top(), "", "bottom", "top")
    d.text((country.bottom()[0] + 12, 220), "находится в", font=SMALL, fill=INK)
    crow_link(d, hotel.right(), (voucher.x, hotel.right()[1]), "размещение", "right", "left")
    cx = client.bottom()[0]
    d.line([cx, client.y + client.h, cx, voucher.y + 60], fill=INK, width=2)
    d.line([cx - 9, client.y + client.h + 14, cx + 9, client.y + client.h + 14], fill=INK,
           width=2)
    end = (voucher.x + voucher.w, voucher.y + 60)
    d.line([cx, voucher.y + 60, end[0], end[1]], fill=INK, width=2)
    for dy in (-10, 0, 10):
        d.line([end[0] + 16, end[1], end[0], end[1] + dy], fill=INK, width=2)
    d.text((cx + 12, client.y + client.h + 30), "покупает", font=SMALL, fill=INK)
    d.text((40, 535), "PK — первичный ключ, FK — внешний ключ, ? — может быть пустым. "
                      "Связи: черта — «один», лапка — «много».", font=SMALL, fill=INK)
    img.save(DOCS / "er_diagram.png")


if __name__ == "__main__":
    draw_er()
    print("saved to", DOCS)
