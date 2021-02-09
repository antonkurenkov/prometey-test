from sqlalchemy import create_engine
from sqlalchemy import Column, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from parser import Parser

import locale
locale.setlocale(locale.LC_ALL, 'ru_RU')

base = declarative_base()


class NewsTable(base):
    __tablename__ = 'news'
    title = Column(String, primary_key=True)
    url = Column(String)
    date = Column(Date)


class Connector:

    def __init__(self):
        db_string = "postgres://localhost:5432/prometey"
        self.db = create_engine(db_string)

        session = sessionmaker(self.db)
        self.session = session()
        base.metadata.create_all(self.db)

    def insert(self, news):
        i = 0
        for item in news:
            duple = self.session.query(NewsTable).get(item['title'])
            if not duple:
                news_item = NewsTable(
                    title=item['title'],
                    url=item['url'],
                    date=item['date']
                )

                self.session.add(news_item)
                i += 1
            else:
                print(f'"{duple.title}" already exists, pass\n')

        self.session.commit()
        print(f'{i} items added')
        print(f'{self.session.query(NewsTable).count()} items total')
        print()

    def head(self, num):
        news = self.session.query(NewsTable).limit(num)
        for n in news:
            print(f'Title: {n.title}')
            print(f'Date: {n.date}')
            print(f'Url: {n.url}')
            print()

    # def clear(self):
    #     self.table.__table__.drop(self.db)


if __name__ == '__main__':
    c = Connector()
    p = Parser()
    urls = p.get_detailed()
    objs = [p.follow(u) for u in urls]
    c.insert(objs)
    c.head(2)