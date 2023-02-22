import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, load_data, Publisher, Book, Shop, Stock, Sale
import os
from dotenv import load_dotenv


def find_stock_by_publisher(s, id_publisher=None, name=None):
    """Решение задания 2
    Функция find_stock_by_publisher() выводит на экран магазины продающие книги заданного в
    параметрах функции издания. Издание задается по id или по имени.
    """

    query = s.query(Book.title, Shop.name, Sale.price, Sale.date_sale)
    query = query.join(Stock, Stock.id == Sale.id_stock)
    query = query.join(Shop, Shop.id == Stock.id_shop)
    query = query.join(Book, Book.id == Stock.id_book)
    query = query.join(Publisher, Publisher.id == Book.id_publisher)
    if id_publisher:
        query = query.filter(Publisher.id == id_publisher)
    if name:
        query = query.filter(Publisher.name == name)
    for rec in query.all():
        print(f"{rec.title} | {rec.name} | {rec.price} | {rec.date_sale}")


if __name__ == '__main__':
    # DSN = 'dialect+driver://username:password@host:port/database'
    load_dotenv()

    dialect = os.getenv('dialect')
    driver = os.getenv('driver')
    username = os.getenv('login')
    password = os.getenv('password')
    host = os.getenv('host')
    port = os.getenv('port')
    database = os.getenv('database')

    DSN = f'{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}'
    engine = sqlalchemy.create_engine(DSN)
    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    load_data(session, 'data.json')

    find_stock_by_publisher(session, id_publisher=int(input('Введите id издателя: ')))
    find_stock_by_publisher(session, name=input('Введите имя издателя: '))

    session.close()
