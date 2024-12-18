import sqlalchemy
import json
from sqlalchemy.orm import sessionmaker
from orm import create_tables, Publisher, Shop, Book, Stock, Sale

def create_connection(db_name, db_user, db_password, db_host, db_port, name_db):
    DSN = f'{db_name}://{db_user}:{db_password}@{db_host}:{db_port}/{name_db}'
    engine = sqlalchemy.create_engine (DSN)
    return engine
engine = create_connection('postgresql', 'postgres', 'postgres', 'localhost', '5432', 'orm_db')

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', 'r') as file:
    data = json.load(file)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()

def price_list(serch=input('Введите идентификатор или название книги:')):
    serch = serch
    if serch.isdigit():
        results = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)\
        .join(Publisher, Publisher.id == Book.id_publisher) \
        .join(Stock, Stock.id_book == Book.id) \
        .join(Shop, Shop.id == Stock.id_shop) \
        .join(Sale, Sale.id_stock == Stock.id) \
        .filter(Publisher.id == serch).all()
    else:
        results = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale) \
            .join(Publisher, Publisher.id == Book.id_publisher) \
            .join(Stock, Stock.id_book == Book.id) \
            .join(Shop, Shop.id == Stock.id_shop) \
            .join(Sale, Sale.id_stock == Stock.id) \
            .filter(Publisher.name == serch).all()
    for book, shop, price, date_sale in results:
        print(f'{book: <40} | {shop: <10} | {price: <10} | {date_sale.strftime('%d-%m-%Y')}')
    


session.commit()
session.close()

if __name__ == '__main__':
    create_connection('postgresql', 'postgres', 'postgres', 'localhost', '5432', 'orm_db')
    price_list()