﻿from random import random 

class Game(object):  
    """
    Obiekt utrzymujacy stan pojedynczej rozgrywki i prowadzacy rozgrywke.
    Gra rozpoczyna sie od wszystkich zakrytych pol. Na niektorych polach znajduja sie miny. Pola mozna odkrywac lub flagowac.
    Gra toczy sie do momentu oznaczenia wszystkich min i odkrycia pozostalych pol lub do wejscia na mine.
    
    Wartosci pol:
    'e' puste
    'M' mina
    'Fe' flaga + puste
    'FM' flaga + mina
    '.' odsloniete, 0 sasiadow
    '0' tymczasowy stan wystepujace w trakcie odslaniania pola po wejsciu; nie jest widoczny w stanie ustalonym
    '1'-'8' odsloniete, n sasiadow
    'B' mina wybuchala
    
    Statusy:
    'ready' poczatek gry, brak odslonietych pol
    'started' trwa rozgrywka
    'success' koniec gry - wygrana
    'fail' koniec gry - przegrana
    """
    
    # ENUMy zamiast tekstow?
    
    def __init__(self, setWidth=5, setHeight=5, setTotalMines=4):
        """
        Rozpoczyna nowa rozgrywke od wszystkich zakrytych pol, bez rozlozenia min.
        Miny zostana dodane po okreciu pierwszego pola.
        """
        self.width = setWidth
        self.height = setHeight
        self.totalMines = setTotalMines 
        self.status = 'ready'  
        self.clearField()
        
    def fieldAsString(self, external=False):
        """
        Zwraca cale pole jako jeden napis wierszami z gory na dol. Wiersze oddzielone '/'.
        Pola wierszy od lewej do prawej. Pola oddzielone '&'.
        Przyklad 3x3: 'e&e&e/e&e&e/e&e&e'
        W trybie wewnetrzym (external=False) pola sa reprezentowane bez zmian. 
        W zewnetrznym:
            Pola odsloniete '.', 'B', '1'-'9' sa pokazywane bez zmian.
            Pozostale pola przeksztalcane, zeby ukryc zawartosc (warunkowo zaleznie of statusu gry).
        """
        result = ''
        for y in range(self.width):
            row = ''
            for x in range(self.height):
                f = self.field[ x,y ]
                if not external or f in [ '.', '1', '2', '3', '4', '5', '6', '7', '8', 'B']:
                    fld = f
                elif f in [ 'Fe', 'FM' ]:
                    if self.status == 'fail':
                        fld = f
                    else:
                        fld = 'F' 
                elif f == 'M':
                    if self.status == 'fail':
                        fld = f
                    else:
                        fld = 'X' 
                else:  # 'e'
                    fld = 'X'
                if row != '':
                    row += '&'
                row += fld 
            if result != '':
                result += '/'
            result += row
        return result
        
    
    def allCells(self):
        """
        Funkcja pomocnicza - generuje oniesienia do wszystkich elementow planszy
        """
        for x in range(self.height):
            for y in range(self.width):
                yield x,y
                
    def getMinesLeft(self):
        """
        Zwraca liczbe nieoznaczonych min - wynikajaca z wypelnienia planszy i oznaczen flagami. 
        Nie bada dopasowania flag do min - jesli gracz zle stawia flagi, to licznik i tak się zmniejsza.
        Jesli flag jest wiecej niz min, zwraca zero. 
        """
        fieldValues = list(self.field.values())
        flags = fieldValues.count( 'Fe' ) + fieldValues.count( 'FM' )
        # return max( self.totalMines - flags, 0 )
        return self.totalMines - flags

    def neighbourCells(self,xy):
        """
        Funkcja pomocnicza - generuje wspolrzedne wszystkich pol otaczajacych dane pole - sprawdzajac czy nie wychodza poza plansze.
        """
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if dx==0 and dy==0:
                    continue
                x1,y1 = xy[0]+dx, xy[1]+dy
                if 0 <= x1 < self.width and 0 <= y1 < self.height:
                    yield x1,y1
        
    def clearField(self):
        """
        Poczatkowe wypelnienie wszystkich pol na pusto (bez min).
        """
        self.field = dict()
        for xy in self.allCells():
                self.field[xy] = 'e'
        
    def layMines(self, spareX=None, spareY=None):
        """
        Rozklada miny na planszy unikajac wskazanego pola.
        Zaklada, ze pole jest cale puste ('e').
        """
        for m in range(self.totalMines):
            while True:
                xy = int(random()*self.width), int(random()*self.height)
                if xy == (spareX, spareY):
                    continue
                if self.field[xy] == 'M':
                    continue
                break
            self.field[xy] = 'M'

    def numNeighbourMines(self,xy):
        """
        Funkcja wyznacza liczbe min na planszy dookola danego pola.
        """
        count = 0
        for xy1 in self.neighbourCells(xy):
            if self.field[xy1] in ['M', 'FM']:
                count += 1 
        return count
        
    def exploreSafeFields(self):
        """
        Funkcja automatycznie odslania wszystkie pola sasiadujace z nowoodslonietymi polami wokol ktorych nie ma min.
        Odslanianie jest kontynuowane rekurencyjnie.
        Jesli mozna odslonic pole z flaga, flaga jest usuwana.
        '0' to tymczasowe oznaczenie pola, z ktorym nie sasiaduja zadne miny. Po zakonczeniu procesu takie pole bedzie oznaczone '.'.
        """
        again=True
        while again:
            again=False
            for xy in self.allCells():
                if self.field[xy] == '0':
                    again=True
                    self.field[xy] = '.'
                    for xy1 in self.neighbourCells(xy):
                        if self.field[xy1] in ['e', 'Fe']:
                            self.field[xy1] = str(self.numNeighbourMines(xy1))
        
    def checkSuccess(self):
        """
        Funkcja sprawdza czy spelniony jest warunek zwyciestwa i ew. ustawia status.
        """ 
        if self.status != 'started':
            return
        fieldValues = list(self.field.values())
        if fieldValues.count( 'Fe' ) == 0 and \
           fieldValues.count( 'e' ) == 0 and \
           fieldValues.count( 'M' ) == 0:
            self.status = 'success'
    
    def stepOnField(self,x,y):
        """
        Odslania pole przy wstapieniu na nie.
        Jesli na polu znajduje sie mina, gra sie konczy przegrana.
        Jesli odslonieto wszystkie pola poza minami, gra sie konczy wygrana.  
        Jesli mozna odslonic sasiednie pola, sa one rowniez odslaniane - rekurencyjnie.
        Jesli gra dopiero sie zaczyna, pierwsze wejscie powodule rozlozenie min.
        Jesli gra jest zakonczona, metoda nie ma skutkow.
        """
        if self.status in ['fail', 'success']:
            return
        if self.status == 'ready':
            self.status = 'started'
            self.layMines( x, y )
        xy = x,y
        if self.field[xy] == 'M':
            self.field[xy] = 'B'
            self.status = 'fail'   
        else:
            numMines = str(self.numNeighbourMines(xy))
            self.field[xy] = numMines
            if numMines == '0':
                self.exploreSafeFields()
        self.checkSuccess()

    def setFlag(self,x,y,state):
        """
        Ustawia (state==True) na polu lub usuwa (state==False) flage z pola, jesli mozna to zrobic i wtedy sprawdza warunek konca gry.
        W przeciwnym razie - brak skutkow.
        """
        if self.status != 'started':
            return
        xy = x,y
        if state:
            if self.field[xy] in ['e','M']:
                self.field[xy] = 'F' + self.field[xy]
                self.checkSuccess()
        else:
            if self.field[xy] in ['Fe','FM']:
                self.field[xy] = self.field[xy][1:]
                self.checkSuccess()
    
    """
    def show(self, transform):
        print('   ', end='')
        for x in range(self.width):
            print( "%s  " % chr( x + ord('a')), end='')
        print()
        for y in range(self.height):
            print( "%2d " % (y+1), end='' )
            for x in range(self.width):
                print(transform(self.field[(x,y)]), ' ', end='')
            print()
        print()
    
    def reveal(self):
        self.show( lambda x: x )

    def display(self):
        self.show( lambda x: '*' if x in ['e', 'M'] else 'F' if x[0]=='F' else x )
        
    def display(self):
        print( 'status: ', self.status )
        print( 'mines left: ', self.minesLeft )
        self.field.reveal()
        self.field.display()
    """

