from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

from gameset import GameSet
from persistentgame import PersistentGame    #, Base

from random import random

# import traceback

# class PersistentGameSet(GameSet):
class PersistentGameSet():

    """    
    def __init__(self):
#        super(self).__init__()
        self.engine = create_engine('sqlite:///data.sqlite', echo=True)
#        Base.metadata.create_all(self.engine)        
#        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        print( 'engine:', self.engine )
        print( 'session:', self.session )
        print( 'before' )
#        traceback.print_stack()
        print( 'after' )
        g = PersistentGame()
        self.session.add(g)
        self.session.commit()
        print( 'commit' )
    """    
    def __init__(self):
        self.games = dict()
        
    def startNewGame(self):
        newID = int( random() * 9000 + 1000)
        """ while( newID in self.games ):
            newID = int( random() * 9000 + 1000)
        newID = str(newID)
        """
        
        newGame = PersistentGame()
        newGame.gameID = newID
        newGame.counter = 1
        newGame.fieldStr = newGame.getFieldAsString(True)
        self.session.add(newGame)
        self.session.commit()
        
#        self.games[newID] = newGame
        return newID
 
    def getGameList(self): # zwraca listê id gier
        
        q = self.session.query(PersistentGame.gameID).all()
        print( type(q))
        print(q)
        q = list(map( lambda x: x[0], q ))
        print(q)
        return q
#        return list( self.games.keys())
    
    def getGameByID(self,id):  # zwraca obiekt gry
        q = self.session.query(PersistentGame).filter(PersistentGame.gameID==id).first()
        print(type(q))
        print(q.id, q.gameID)
        print(q)
        q.setFieldFromString( q.fieldStr )
        return q
#        return self.games[id]

    
       