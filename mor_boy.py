# -*- coding: utf-8 -*-

import random

ship_symbol  = chr(0x25A0)
empty_symbol = chr(0x25CB)
kill_symbol  = 'X' #chr(0x02DF)
miss_symbol  = 'T'
contour_symbol = 'N'




# классы исключений

# такой ход уже был
class RepeatException(Exception):
    def __init__(self, text):
        self.txt = text

# ход за пределами поля
class BoardOutException(Exception):
    def __init__(self, text):
        self.txt = text

# создание корабля за пределами поля
class ShipOutException(Exception):
    def __init__(self, text):
        self.txt = text

class Dot():
    def __init__(self, x, y):
        self.x = x
        self.y = y
# находим хэш для точки
    def __hash__(self):
        return hash((self.x, self.y))
# 
    def __str__(self):
        return f'{self.x} {self.y}'

    def __eq__(self, another_dot):
        return (self.x==another_dot.x) and (self.y==another_dot.y)

    def isNear(self, dot):
        dx = abs(self.x - dot.x)
        dy = abs(self.y - dot.y)
        if (dx==1 and dy==0) or (dx==0 and dy==1):
            return True
        else:
            return False

    def getAllNearDots(self):
        near_dots = list()
        for ix in range(self.x-1, self.x+2):
            for iy in range(self.y-1, self.y+2):
                near_dots.append(Dot(ix, iy))
        return near_dots

class Ship():
    def __init__(self, ship_len ,init_dot, ship_dir):
        self.ship_len = ship_len
        self.init_dot = init_dot
        self.ship_dir = ship_dir
        self.ship_livs = ship_len

    def dots(self):
        ship_dots =[]
        if self.ship_dir:
            for i in range(self.ship_len):
                ship_dots.append(Dot(self.init_dot.x + i, self.init_dot.y))
        else:
            for i in range(self.ship_len):
                ship_dots.append(Dot(self.init_dot.x, self.init_dot.y + i))
        return ship_dots

class Board():
    def __init__(self, hid=True):
        self.board_size = 6
        self.board_dots = dict()
        self.killed_dots = 0
        for col in range(self.board_size):
            for row in range(self.board_size):
                self.board_dots[Dot(row, col)] = empty_symbol

        self.ship_lst  = list()
        self.hid = hid
        self.alive_n = 0
# функция возвращает случайный корабль заданной длины
    def random_ship(self, shp_len):
        random.seed()
        direct = random.randint(0, 1)
        x0 = random.randint(0, self.board_size-1)
        y0 = random.randint(0, self.board_size-1)
        return Ship(shp_len, Dot(x0, y0), direct)
# делаем случайную доску
    def make_random_ships(self, n_iter=2000):
        ships =[3, 2, 2, 1, 1, 1, 1]
        
        for trying in range(n_iter):
            
            self.board_dots = dict()
            for col in range(self.board_size):
                for row in range(self.board_size):
                    self.board_dots[Dot(row, col)] = empty_symbol
            self.ship_lst  = list()
            
            n_ship =0
            for ship_len in ships:
                for i in range(n_iter):
                    if self.add_ship(self.random_ship(ship_len)):
                        n_ship+=1
                        break
            if n_ship >= 7:
                break
                



    def add_ship(self, shp):
        try:
            for dot in shp.dots():
                if dot not in self.board_dots:
                    raise ShipOutException(str(dot))
                if self.board_dots[dot] != empty_symbol:
                    raise ShipOutException(str(dot))
        except ShipOutException:
            return 0
        else:
            for dot in shp.dots():
                self.board_dots[dot] = ship_symbol
                # print(dot, self.board_dots[dot])
                # контурные точки
            for dot in shp.dots():
                for dot2 in dot.getAllNearDots():
                    if (dot2 in self.board_dots) and (self.board_dots[dot2]!=ship_symbol):
                        self.board_dots[dot2] = contour_symbol
                        # print(dot, self.board_dots[dot])
            self.ship_lst.append(shp)
            self.alive_n += 1
            return 1

    def contour():
        pass

    def print_board(self):
        print_list = list( list('0' for j in range(self.board_size)) for i in range(self.board_size))
        
        for dot in self.board_dots:
            if self.hid:
                if self.board_dots[dot] in [contour_symbol, ship_symbol]:
                    print_list[dot.x][dot.y] = empty_symbol
                else:
                    print_list[dot.x][dot.y] = self.board_dots[dot]
            else:
                if self.board_dots[dot] in [contour_symbol]:
                    print_list[dot.x][dot.y] = empty_symbol
                else:
                    print_list[dot.x][dot.y] = self.board_dots[dot]
            # print_list[dot.x][dot.y] = self.board_dots[dot]
                
        if self.hid:
            print('Поле компьютера:')
        else:
            print('Поле игрока:')
        print(' |1|2|3|4|5|6')
        for i in range(self.board_size):
            str1 = str(i+1) + '|'
            for j in range(self.board_size):
                str1 = str1 + print_list[i][j] + '|'
            print(str1)

    def out(self, dot):
        pass
    def shot(self, x, y):
        pass

class Player():
    def __init__(self, self_board, enemy_board):
        pass
        self.self_board  = self_board
        self.enemy_board = enemy_board
    def ask(self):
        pass
    def move(self):
        atack_point = self.ask()
        if atack_point not in self.enemy_board.board_dots:
            return True
        elif self.enemy_board.board_dots[atack_point] in [empty_symbol, contour_symbol]:
            self.enemy_board.board_dots[atack_point] = miss_symbol
            return False
        elif self.enemy_board.board_dots[atack_point]==ship_symbol:
            self.enemy_board.board_dots[atack_point] = kill_symbol
            self.enemy_board.killed_dots += 1
            return True
            
            

class User(Player):
    def ask(self):
        board_size = self.enemy_board.board_size
        try:
            x, y = tuple(map(int, list(input('Ваш ход: ').split())))
            x = x - 1 
            y = y - 1 
            
            if (0<=x<board_size) and (0<=y<board_size):
                if self.enemy_board.board_dots[Dot(x,y)] in [miss_symbol, kill_symbol]:
                    raise RepeatException()
            else:
                raise BoardOutException()
                
        except RepeatException:
            print('Такой ход уже был, сходите по другому')
            return Dot(-1, -1)
        except BoardOutException:
            print('Ваш ход за пределами поля, сходите по другому')
            return Dot(-1, -1)
        except:
            print('Некорректный ход, сходите по другому')
            return Dot(-1, -1)
        else:
            return Dot(x, y)


class AI(Player):
    def ask(self):
        board_size = self.enemy_board.board_size
        try:
            random.seed()
            x = random.randint(0, board_size-1)
            y = random.randint(0, board_size-1)
            if (1<=x<=board_size) and (1<=y<=board_size):
                if self.enemy_board.board_dots[Dot(x,y)] in [miss_symbol, kill_symbol]:
                    raise RepeatException()
            else:
                raise BoardOutException()
                
        except RepeatException:
            # print('Такой ход уже был, сходите по другому')
            return Dot(-1, -1)
        except BoardOutException:
            # print('Ваш ход за пределами поля, сходите по другому')
            return Dot(-1, -1)
        except:
            # print('Некорректный ход, сходите по другому')
            return Dot(-1, -1)
        else:
            return Dot(x, y)



class Game():
    def __init__(self):
        self.user_board = Board(hid=False)
        self.ai_board   = Board(hid=True)
        self.user       = User(self.user_board, self.ai_board)
        self.ai         = AI(self.ai_board, self.user_board)


    def random_board(self):
        self.user_board.make_random_ships()
        self.ai_board.make_random_ships()
        # self.user_board.print_board()
        # self.ai_board.print_board()

    def greet(self):
        print('Привет. Давайте начнём игру.')
        print('Делайте ходы в виде координат точек(x, y) через пробел(пример:1 3)')



    def loop(self):
        while True:
            res = True
            while res:
                self.user_board.print_board()
                self.ai_board.print_board()
                res = self.user.move()
                # проверка на победу юзера
                if self.ai_board.killed_dots>=11:
                    break
            if self.ai_board.killed_dots>=11:
                print('Игра окончена. Вы выиграли!')
                break

            
            
            res = True
            while res:
                res = self.ai.move()
            # проверка на победу ии
                if self.user_board.killed_dots>=11:
                    break
            if self.user_board.killed_dots>=11:
                print('Игра окончена. Вы проиграли!')
                break




    def start(self):
        self.greet()
        self.random_board()
        self.loop()

if __name__ == "__main__":
    gm1 = Game()
    gm1.start()
