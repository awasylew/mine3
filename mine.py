from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for
from flask import jsonify
import os

#from flask_sqlalchemy import SQLAlchemy

#from game import Game
from gameset import GameSet
#from persistentgameset import PersistentGameSet

from persistentgame import PersistentGame, Base
from persistentgameset import PersistentGameSet 

from sqlalchemy import *
from sqlalchemy.orm.session import sessionmaker

#gameset = GameSet()
gameset = PersistentGameSet()

app = Flask(__name__) 

engine = create_engine('sqlite:///data.sqlite', echo=True)
#engine = create_engine('sqlite://', echo=True)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)  
print('created')      

Session = sessionmaker( bind=engine )
print( Session )
session = Session()
print( session )
gameset.session = session

# app.config['SQLALCHEMY_DATABASE_URI']='sqlite://'
# db = SQLAlchemy(app)

"""
class PersistentGame(db.Model, Game):
    __tablename__ = 'games'
    
    id = db.Column( db.Integer, primary_key=True )
    
    gameID = db.Column( db.String(20))
    width = db.Column( db.Integer )
    height = db.Column( db.Integer )
    totalMines = db.Column( db.Integer )
    status = db.Column( db.String(20))
    field = db.Column( db.PickleType )              # ew. mozna zmienic picklera na prostszy
    
    def __init__(self):
        Game(self).__init__()
    
    def __repr__(self):
        return "PersistentGame(id:%d, gameID:%s, status:%s)" % (self.id, self.gameID, self.status)


db.create_all()
print( 'created' )

from random import random 


class PersistentGameSet(GameSet):
    
#    def __init__(self):
#        super(self).__init__()
#        self.engine = create_engine('sqlite://', echo=True)
#        Base.metadata.create_all(self.engine)        
#        Session = sessionmaker(bind=self.engine)
#        db.session = Session()
#        print( 'engine:', self.engine )
#        print( 'session:', db.session )
#        print( 'before' )
#        traceback.print_stack()
#        print( 'after' )
#        g = PersistentGame()
#        db.session.add(g)
#        db.session.commit()
#        print( 'commit' )
        
        
    def startNewGame(self):
        print('startNewGame')
                
        newID = int( random() * 9000 + 1000)
        while( newID in self.games ):
            newID = int( random() * 9000 + 1000)
        newID = str(newID)
        
        newGame = PersistentGame()
        newGame.gameID = newID
        db.session.add(newGame)
        db.session.commit()
        print( 'added, commited')

        q1 = db.session.query(PersistentGame.gameID).all()
        print(q1)
        q2 = db.session.query(PersistentGame).all()
        print(q2)
        
        self.games[newID] = newGame
        return newID
 
    def getGameList(self): # zwraca list� id gier
        
        q = db.session.query(PersistentGame.gameID).all()
        print(q)
        return q
#        return list( self.games.keys())
    
    def getGameByID(self,id):  # zwraca obiekt gry
        q = db.session.query(PersistentGame).filter(PersistentGame.gameID==id).first()
        print('getGameByID q:', q)
        print('getGameByID type:', type(q))
        return q
#        return self.games[id]

"""


apiPrefix = '/api/v1'
apiPrefixBare = '/api'
webPrefix = ''

@app.route( '/' )
# @app.route( webPrefix )  chwilowo wylaczone, bo puste nie dziala - da sie poprawic?
def webRoot():
    return redirect( url_for('webGamesDefault'))

@app.route( apiPrefix )
@app.route( apiPrefixBare )
def apiRoot():
    return render_template( 'api.html' )

@app.route( webPrefix + '/games')                      # tylko lista gier
@app.route( webPrefix + '/games/<gameID>')             # biezaca gra + lista gier
def webGamesDefault( gameID=None ):
    if gameID != None:
        currentGame = gameset.getGameByID( gameID )
    else:
        currentGame = None
    game_ids = gameset.getGameList()
    return render_template('game.html', game=currentGame, game_url=url_for('webGamesDefault', gameID=gameID), 
                           game_ids=game_ids, games_url=webPrefix+'/games' )                                   # snake_case -> cameCase

@app.route( apiPrefix + '/games')
def apiGames():
    rsp = {'game_ids': gameset.getGameList()}
    print( rsp )
    return jsonify( rsp )

@app.route( apiPrefix + '/games2')
def apiGames2():
#    rsp = {'games': list(map(lambda gameID: apiPrefix+'/games/'+gameID, gameset.getGameList())) }
    rsp = {'games': list(map(lambda gameID: url_for('apiShowField', gameID=gameID, _external=True), gameset.getGameList())) }
    print( rsp )
    return jsonify( rsp )

@app.route( apiPrefix + '/games/<gameID>')
def apiShowField( gameID ):                                         # nazwa?
    game = gameset.getGameByID( gameID )                            # obsluga bledu id
    rsp = { 'width': game.width, 
           'height': game.height,
           'totalMines': game.totalMines,
           'minesLeft': game.getMinesLeft(),
           'status': game.status,
           'field': game.getFieldAsString(True) }
    return jsonify(rsp)                                             # dodac naglowki

@app.route( webPrefix + '/games/new' )                                         # w wersji API POST zamiast /new 
def webNewGame():
    gameID = gameset.startNewGame()
    print('started:', gameID )
#    return 'id = ' + str(id)
    return redirect( url_for('webGamesDefault', gameID=gameID ))

@app.route( apiPrefix+'/games', methods=['POST'])
def apiNewGame():
    gameID = gameset.startNewGame()
    return 'id = ' + str(gameID)

@app.route( webPrefix + '/games/<gameID>/flag/<x>/<y>/<state>' )            # tutaj sciezka na x/y/state, a w api parametry?
def webFlag( gameID, x, y, state ):
    game = gameset.getGameByID( gameID )
    print('pre add')
    session.add(game)
    print( type(game))
    print( session.dirty, session.is_modified(game))
    game.setFlag( int(x), int(y), state.upper()=='TRUE' )               # brak obslugi bledow
#    game.counter += 1
    game.fieldStr = game.getFieldAsString(True)
    print( session.dirty, session.is_modified(game))
    session.commit()
    print('post commit')
    return redirect( url_for('webGamesDefault', gameID=gameID ))

@app.route( apiPrefix + '/games/<gameID>/flag', methods=['GET', 'POST'])                    # powinno byc tylko POST
def apiFlag( gameID ):
    try:                                                            # nie mozna tego kodu ladnie uwspolnic z flag?
        game = gameset.getGameByID( gameID )            # obsluga bledu id
        x = int( request.args.get( 'x' ))
        y = int( request.args.get( 'y' ))
        s = request.args.get( 'state' ).upper()
        if not 0 <= x < game.width or not 0 <= y < game.height or not s in ['TRUE', 'FALSE']:
            raise 
    except:
        return 'Expecting params 0,0 <= x,y < width,height, state==false|true', 400        # dodac naglowki
    game.setFlag( x, y, s=='TRUE' )
    return apiShowField( gameID )
    
@app.route( webPrefix + '/games/<gameID>/step/<x>/<y>' )
def webStep( gameID, x, y ):
    game = gameset.getGameByID( gameID )
    session.add(game)
    game.stepOnField(int(x),int(y))                                     # brak obslugi bledow
#    game.counter += 1
    game.fieldStr = game.getFieldAsString(True)
    session.commit()
    return redirect( url_for('webGamesDefault', gameID=gameID ))

@app.route( apiPrefix + '/games/<gameID>/step', methods=['GET', 'POST'] )                   # powinno byc tylko POST
def apiStep( gameID ):
    try:                                                            # nie mozna tego kodu ladnie uwspolnic z flag?
        game = gameset.getGameByID( gameID )            # obsluga bledu id
        x = int( request.args.get( 'x' ))
        y = int( request.args.get( 'y' ))
        if not 0 <= x < game.width or not 0 <= y < game.height:
            raise 
    except:
        return 'Expecting params 0,0 <= x,y < width,height', 400        # dodac naglowki
    game.stepOnField( x, y )
    return apiShowField( gameID )

@app.route('/quit_server')
def quit_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return "Quitting server..."
   
if __name__ == '__main__':
    print('if')
    port = int(os.getenv("PORT"))
    app.run(host='0.0.0.0', port=port) 
