from game import Game
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relation, sessionmaker

Base = declarative_base()

class PersistentGame(Game, Base):
#class PersistentGame(Base):
    __tablename__ = 'games'
    
    id = Column( Integer, primary_key=True )
    
    counter = Column( Integer )
    fieldStr = Column( String )
    
    gameID = Column( String(20))
    status = Column( String(20))
    width = Column( Integer )
    height = Column( Integer )
    totalMines = Column( Integer )
    field = Column( PickleType )              # ew. mozna zmienic picklera na prostszy
    
    def __repr__(self):
        return 'PersistentGame( %r, %r, %r, %r, %r, %r, %r, %r, %r )' % \
            (self.id, self.counter, self.gameID, self.status, self.width, self.height, self.totalMines, self.fieldStr, self.field )
    
