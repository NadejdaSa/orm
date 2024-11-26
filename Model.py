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

publisher = input('Введите идентификатор или название книги:')
def price_list(publisher):
    result = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).filter(Publisher.name==publisher).filter(Publisher.id==Book.id_publisher).filter(Book.id==Stock.id_book).filter(Stock.id_shop==Shop.id).filter(Stock.id==Sale.id_stock).all()
    return result
result = price_list(publisher)
for r in result:
    print(f'{r[0]} | {r[1]} | {r[2]}| {r[3]}')

session.commit()
session.close()