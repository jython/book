import zxoracle
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.schema import Sequence

db = create_engine('zxoracle://database_schema:password@hostname:port/database')
metadata = MetaData()
player = Table('player', metadata,
    Column('id', Integer, Sequence('id_seq'), primary_key=True),
    Column('first', String(50)),
    Column('last', String(50)),
    Column('position', String(30)))

metadata.create_all(db)

class Player(object):
    def __init__(self, first, last, position):
        self.first = first
        self.last = last
        self.position = position
        
    def __repr__(self):
        return "<Player('%s', '%s', '%s')>" %(self.first, self.last, self.position)


# Delarative creation of the table, class, and mapper
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class Player(object):
    __tablename__ = 'player'
    
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    first = Column(String(50))
    last = Column(String(50))
    position = Column(String(30))
    
    def __init__(self, first, last, position):
        self.first = first
        self.last = last
        self.position = position
        
    def __repr__(self):
        return "<Player('%s','%s','%s')>" % (self.first, self.last, self.position)
        
from sqlalchemy.orm import mapper
mapper(Player, player)
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=db)
session = Session()
player1 = Player('Josh', 'Juneau', 'forward')
player2 = Player('Jim', 'Baker', 'forward')
player3 = Player('Frank', 'Wierzbicki', 'defense')
player4 = Player('Leo', 'Soto', 'defense')
player5 = Player('Vic', 'Ng', 'center')
session.add(player1)
session.add(player2)
session.add(player3)
session.add(player4)
session.add(player5)

forwards = session.query(Player).filter_by(position='forward').all()
defensemen = session.query(Player).filter_by(position='defense').all()
center = session.query(Player).filter_by(position='center').all()
