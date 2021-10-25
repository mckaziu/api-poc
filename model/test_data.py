
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Float

Base = declarative_base()


class MyObject(Base):
    __tablename__ = 'test'

    id = Column(Integer, primary_key=True)
    x = Column(Float)
    y = Column(Float)

    def __repr__(self):
        return f'MyObject(x={self.x}, y={self.y})'

    def to_dict(self):
        return {"id": self.id, "values": [self.x, self.y]}


class TestOperations:
    def __init__(self, session):
        self.session = session

    def create(self, x, y):
        with self.session.begin():
            self.session.add(MyObject(x=x, y=y))

    def read(self, id=None):
        with self.session.begin():
            if id:
                return list(map(lambda o: o.to_dict(), self.session.query(MyObject).filter(MyObject.id == id).all()))
            else:
                return list(map(lambda o: o.to_dict(), self.session.query(MyObject).all()))

    def update(self, id, x, y):
        with self.session.begin():
            data = self.session.query(MyObject).get(id)
            data.x = x
            data.y = y

    def delete(self, id):
        with self.session.begin():
            data = self.session.query(MyObject).get(id)
            if data:
                self.session.delete(data)
