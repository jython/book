from sqlalchemy import create_engine, MetaData
from sqlalchemy import String, Integer
from sqlalchemy.schema import Sequence, Table, Column, UniqueConstraint
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker

#engine = create_engine('postgresql+zxjdbc://localhost:5432/mydb')
engine = create_engine('postgresql://repustate:repustate@localhost:5432/mydb')
Session = sessionmaker(bind=engine)
connection = engine.connect()
metadata = MetaData()
player_table = Table('player', metadata,
        Column('id', Integer, primary_key=True),
        Column('first', String(50)),
        Column('last', String(50)),
        Column('position', String(30)),
        UniqueConstraint('first', 'last'), # setup a unique key with first and lastname
        )

class Player(object):
    def __init__(self, first, last, position):
        self.first = first
        self.last = last
        self.position = position

    def __repr__(self):
        return "<Player('%s', '%s', '%s')>" %(self.first, self.last, self.position)

player_mapper = mapper(Player, player_table)

def create_table():
    metadata.create_all(engine)


if __name__ == '__main__':
    create_table()
