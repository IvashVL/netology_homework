import json

import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

"""Решение задания 1 
Ниже представлена реализация классов Publisher, Book, Shop, Stock, Sale 
"""

class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=100), unique=True)

class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=100), unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)

    publisher = relationship(Publisher, backref='book')

class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=100), unique=True)


class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    book = relationship(Book, backref='stock')
    shop = relationship(Shop, backref='stock')


class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.TIMESTAMP, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stock = relationship(Stock, backref='sale')


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def load_data(session, file):

    """Решение задания 3
    Функция load_data() загружает данные из json-файла в БД
    Закоментирован мой вариант решения т.к. ответ предложенный в самом задании более лаконичен
    """

    with open(file, encoding='utf-8') as f:
        data = json.load(f)
    for record in data:
        # if item['model'] == 'publisher':
        #     publisher = Publisher(name=item['fields']['name'])
        #     session.add(publisher)
        # elif item['model'] == 'book':
        #     book = Book(title=item['fields']['title'], id_publisher=int(item['fields']['id_publisher']))
        #     session.add(book)
        # elif item['model'] == 'shop':
        #     shop = Shop(name=item['fields']['name'])
        #     session.add(shop)
        # elif item['model'] == 'stock':
        #     stock = Stock(id_book=int(item['fields']['id_book']),
        #                   id_shop=int(item['fields']['id_shop']),
        #                   count=int(item['fields']['count']))
        #     session.add(stock)
        # elif item['model'] == 'sale':
        #     sale = Sale(price=float(item['fields']['price']),
        #                 date_sale=item['fields']['date_sale'],
        #                 id_stock=int(item['fields']['id_stock']),
        #                 count=int(item['fields']['count']))
        #     session.add(sale)

        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()


