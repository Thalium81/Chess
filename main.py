from enum import Enum, auto
import copy

# Перечисление цветов, используемых для фигур.
class Color(Enum):
    WHITE = auto()
    BLACK = auto()

# Изначально нам нужно создать класс, который будет описывать все фигуры в целом.
class Piece:
    def __init__(self, color):
        """
        Инициализирует фигуры и дает ей указанный цвет.

        :param color: Цвет, используемый для фигуры. (Color.WHITE, Color.BLACK)
        """
        self.color = color

    def __str__(self):
        """
        Возвращает буквенное обозначение фигуры.

        :return: Буквенное обозначение фигуры.
        """
        return self.letter[self.color]
    def is_move_correct(self, start, final, board):
        """
        Проверяет, возможно ли совершить указанный ход при заданной фигуре.
        
        :param start: Кортеж (x,y) координат стартовой позиции.
        :param final: Кортеж (x,y) координат финальной позиции.
        :param board: Доска.
        :return: True, если ход возможно совершить, иначе False.
        """

# Пешка - Pawn ------------------------------------------------------------------------------------------------------
class Pawn(Piece):
    letter = {
        Color.WHITE: 'P',
        Color.BLACK: 'p'
    }

    def is_move_correct(self, start, final, board):
        """
        Проверяет, возможно ли совершить указанный ход пешкой.

        :param start: Кортеж (x,y) - координаты стартовой позиции.
        :param final: Кортеж (x,y) - координаты финальной позиции.
        :param board: Доска.
        :return: True, если ход возможно совершить, иначе False.
        """
        x1, y1 = start
        
        x2, y2 = final

        if board.get_piece(x2, y2) and board.get_piece(x2, y2).color == self.color: #Финальная клетка не содержит фигуры того же цвета.
            return False
        
        if self.color == Color.WHITE:
            direct = -1
        else:
            direct = 1
        # Ход вперед
        if y1 == y2 and x2 == x1 + direct and not(board.get_piece(x2, y2)):
            return True
        # Двойной ход вперед (С начальной позиции x = 6 для белых)
        if y1 == y2 and x2 == x1 + 2 * direct and x1 == 6 and self.color == Color.WHITE and not(board.get_piece(x2, y2)):
            return True
        # Двойной ход вперед (С начальной позиции x = 1 для черных)
        if y1 == y2 and x2 == x1 + 2 * direct and x1 == 1 and self.color == Color.BLACK and not(board.get_piece(x2, y2)):
            return True
        # Бьет
        if abs(y2 - y1) == 1 and x2 == x1 + direct and board.get_piece(x2, y2):
            return True
        return False

# Ладья - Rook ------------------------------------------------------------------------------------------------------
class Rook(Piece):
    letter = {
        Color.WHITE: 'R',
        Color.BLACK: 'r'
    }

    def is_move_correct(self, start, final, board):
        """
        Проверяет, возможно ли совершить указанный ход ладьей.

        :param start: Кортеж (x,y) - координаты стартовой позиции.
        :param final: Кортеж (x,y) - координаты финальной позиции.
        :param board: Доска.
        :return: True, если ход возможно совершить, иначе False.
        """
        x1, y1 = start
        
        x2, y2 = final

        if  board.get_piece(x2, y2) and board.get_piece(x2, y2).color == self.color: #Финальная клетка не содержит фигуры того же цвета.
            return False
        
        if x1 == x2:

            if y2 > y1:
                direct = 1
            else:
                direct = -1
            for y in range(y1 + direct, y2, direct):
                if board.get_piece(x1, y):
                    return False
        if y1 == y2:
            
            if x2 > x1:
                direct = 1
            else:
                direct = -1
            for x in range(x1 + direct, x2, direct):
                if board.get_piece(x, y1):
                    return False
            return True
        return False

# Конь - Knight ------------------------------------------------------------------------------------------------------
class Knight(Piece):
    letter = {
        Color.WHITE: 'N', #K занята королем
        Color.BLACK: 'n'
    }

    def is_move_correct(self, start, final, board):
        """
        Проверяет, возможно ли совершить указанный ход конем.

        :param start: Кортеж (x,y) - координаты стартовой позиции.
        :param final: Кортеж (x,y) - координаты финальной позиции.
        :param board: Доска.
        :return: True, если ход возможно совершить, иначе False.
        """
        
        x1, y1 = start

        x2, y2 = final

        if  board.get_piece(x2, y2) and board.get_piece(x2, y2).color == self.color: #Финальная клетка не содержит фигуры того же цвета.
            return False

        return (abs(x2 - x1) == 1 and abs(y2 - y1) == 2) or (abs(x2 - x1) == 2 and abs(y2 - y1) == 1)

# Слон - Bishop ------------------------------------------------------------------------------------------------------
class Bishop(Piece):
    letter = {
        Color.WHITE: 'B',
        Color.BLACK: 'b'
    }

    def is_move_correct(self, start, final, board):
        """
        Проверяет, возможно ли совершить указанный ход слоном.

        :param start: Кортеж (x,y) - координаты стартовой позиции.
        :param final: Кортеж (x,y) - координаты финальной позиции.
        :param board: Доска.
        :return: True, если ход возможно совершить, иначе False.
        """
        x1, y1 = start
        
        x2, y2 = final

        if board.get_piece(x2, y2) and board.get_piece(x2, y2).color == self.color: #Финальная клетка не содержит фигуры того же цвета.
            return False
        
        if abs(x2 - x1) == abs(y2 - y1):

            if x2 > x1:
                directX = 1
            else:
                directX = -1
                
            if y2 > y1:
                directY = 1
            else:
                directY = -1
            
            x, y = x1 + directX, y1 + directY
            while x != x2 and y != y2:
                if board.get_piece(x, y):
                    return False
                x += directX
                y += directY
            return True

        return False
# Еж - Hedgehog --------------------------- К О С М О Д Е С А Н Т --------------------------------------------------
class Hedgehog(Piece):
    letter = {
        Color.WHITE: 'X',
        Color.BLACK: 'x'
    }

    def is_move_correct(self, start, final, board):
        """
        Проверяет, возможно ли совершить указанный ход ежом.

        :param start: Кортеж (x,y) - координаты стартовой позиции.
        :param final: Кортеж (x,y) - координаты финальной позиции.
        :param board: Доска.
        :return: True, если ход возможно совершить, иначе False.
        """
        x1, y1 = start
        
        x2, y2 = final

        if board.get_piece(x2, y2) and board.get_piece(x2, y2).color == self.color: #Финальная клетка не содержит фигуры того же цвета.
            return False
        
        if abs(x1-x2) == 1 and abs(y1-y2) == 1:
            return True
        return False

# Десантник - Trooper ------------------------------------------------------------------------------------------------------
class Trooper(Piece):
    letter = {
        Color.WHITE: 'T',
        Color.BLACK: 't'
    }

    def is_move_correct(self, start, final, board):
        """
        Проверяет, возможно ли совершить указанный ход десантником.

        :param start: Кортеж (x,y) - координаты стартовой позиции.
        :param final: Кортеж (x,y) - координаты финальной позиции.
        :param board: Доска.
        :return: True, если ход возможно совершить, иначе False.
        """
        x1, y1 = start
        
        x2, y2 = final

        if board.get_piece(x2, y2) and board.get_piece(x2, y2).color == self.color: #Финальная клетка не содержит фигуры того же цвета.
            return False
        
        if self.color == Color.WHITE:
            direct = -1
        else:
            direct = 1
        # Ход вперед
        if abs(y2-y1) <= 1 and x2 == x1 + direct and not(board.get_piece(x2, y2)):
            return True
        
        # Бьет
        if abs(y2 - y1) == 1 and x2 == x1 + direct and board.get_piece(x2, y2):
            return True
        return False

# Ускоритель - Accelerator ------------------------------------------------------------------------------------------------------
class Accelerator(Piece):
    letter = {
        Color.WHITE: '^',
        Color.BLACK: 'v'
    }

    def is_move_correct(self, start, final, board):
        """
        Проверяет, возможно ли совершить указанный ход десантником.

        :param start: Кортеж (x,y) - координаты стартовой позиции.
        :param final: Кортеж (x,y) - координаты финальной позиции.
        :param board: Доска.
        :return: True, если ход возможно совершить, иначе False.
        """
        x1, y1 = start
        
        x2, y2 = final

        if board.get_piece(x2, y2) and board.get_piece(x2, y2).color == self.color: #Финальная клетка не содержит фигуры того же цвета.
            return False
        
        if x1 == x2 and abs(y1 - y2) <= 3:
            return True
        return False

# Король - King -------------------------------------------------------------------------------------------------------------
class King(Piece):
    letter = {
        Color.WHITE: 'K',
        Color.BLACK: 'k'
    }

    def is_move_correct(self, start, final, board):
        """
        Проверяет, возможно ли совершить указанный ход королем.

        :param start: Кортеж (x,y) - координаты стартовой позиции.
        :param final: Кортеж (x,y) - координаты финальной позиции.
        :param board: Доска.
        :return: True, если ход возможно совершить, иначе False.
        """
        x1, y1 = start
        
        x2, y2 = final

        if board.get_piece(x2, y2) and board.get_piece(x2, y2).color == self.color: #Финальная клетка не содержит фигуры того же цвета.
            return False
        
        if abs(x2 - x1) <= 1 and abs(y2 - y1) <= 1:
            return True
    
# Ферзь - Queen ----------------------------------------------------------------------------------------------------------------------
class Queen(Piece):
    letter = {
        Color.WHITE: 'Q',
        Color.BLACK: 'q'
    }

    def is_move_correct(self, start, final, board):
        """
        Проверяет, возможно ли совершить указанный ход ферзем.

        :param start: Кортеж (x,y) - координаты стартовой позиции.
        :param final: Кортеж (x,y) - координаты финальной позиции.
        :param board: Доска.
        :return: True, если ход возможно совершить, иначе False.
        """
        x1, y1 = start
        
        x2, y2 = final

        if  board.get_piece(x2, y2) and board.get_piece(x2, y2).color == self.color: #Финальная клетка не содержит фигуры того же цвета.
            return False
        
        # Диагональ
        if abs(x2 - x1) == abs(y2 - y1):

            if x2 > x1:
                directX = 1
            else:
                directX = -1
                
            if y2 > y1:
                directY = 1
            else:
                directY = -1
            
            x, y = x1 + directX, y1 + directY
            while x != x2 and y != y2:
                if board.get_piece(x, y):
                    return False
                x += directX
                y += directY
            return True
        
        # Прямая
        if x1 == x2:

            if y2 > y1:
                direct = 1
            else:
                direct = -1
            for y in range(y1 + direct, y2, direct):
                if board.get_piece(x1, y):
                    return False
        if y1 == y2:
            
            if x2 > x1:
                direct = 1
            else:
                direct = -1
            for x in range(x1 + direct, x2, direct):
                if board.get_piece(x, y1):
                    return False
            return True

        return False
    
# Шашка - Checker ----------------------------------------------------------------- Ш А Ш К И ---------------------------------------
class Checker(Piece):
    letter = {
        Color.WHITE: 'C',
        Color.BLACK: 'c'
    }

    def is_move_correct(self, start, final, board):
        """
        Проверяет, возможно ли совершить указанный ход шашкой.

        :param start: Кортеж (x,y) - координаты стартовой позиции.
        :param final: Кортеж (x,y) - координаты финальной позиции.
        :param board: Доска.
        :return: True, если ход возможно совершить, иначе False.
        """
        x1, y1 = start
        
        x2, y2 = final

        if self.color == Color.WHITE:
            direct = -1
        else:
            direct = 1
    
        if abs(y2 - y1) == 1 and x2 == x1 + direct and not(board.get_piece(x2, y2)):
            return True

        # Переход через шашку противника
        if abs(y2 - y1) == 2 and x2 == x1 + 2 * direct:
            enemy_x = x1 + direct
            enemy_y = (y1 + y2) // 2
            enemy_piece = board.get_piece(enemy_x, enemy_y)
            if enemy_piece and enemy_piece.color != self.color and not board.get_piece(x2, y2):
                board.board[enemy_x][enemy_y] = None # Удаляем съеденную шашку
                return True

        return False

    def crown(self, cords, board):
        """
        Превращает шашку в дамку по достижению края доски.

        :param pos: Кортеж (x, y) позиции шашки.
        :param board: Объект доски.
        """
        x, y = cords
        if (self.color == Color.WHITE and x == 0) or (self.color == Color.BLACK and x == 7):
            board.board[x][y] = CheckerKing(self.color)

# Дамка - CrownedChecker ----------------------------------------------------------------------------------------------------------------------
class CrownedChecker(Piece):
    letter = {
        Color.WHITE: 'W',
        Color.BLACK: 'w'
    }

    def is_move_correct(self, start, final, board):
        """
        Проверяет, возможно ли совершить указанный ход дамкой.

        :param start: Кортеж (x,y) - координаты стартовой позиции.
        :param final: Кортеж (x,y) - координаты финальной позиции. 
        :param board: Доска.
        :return: True, если ход возможно совершить, иначе False.
        """
        x1, y1 = start
        
        x2, y2 = final

        if abs(x2 - x1) == abs(y2 - y1):

            if x2 > x1:
                directX = 1
            else:
                directX = -1
                
            if y2 > y1:
                directY = 1
            else:
                directY = -1
            
            x, y = x1 + directX, y1 + directY
            while x != x2 and y != y2:
                if board.get_piece(x, y):
                    return False
                x += directX
                y += directY
            return True
        return False

    
# Доска - Board ------------------------------------------------------------------------ Д О С К А ---------------------------------
class Board:
    def __init__(self, game_type):
        """
        Создает доску и расставляет на ней фигуры или шашки в зависимости от игры.

        :param game_type: Название игры.
        """
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.game_type = game_type
        self.setup_pieces()

    def setup_pieces(self):
        """
        Расставляет фигуры или шашки (в зависимости от игры) на доске.
        """
        if self.game_type == "chess": #---
                
            order = [Rook, Knight, Bishop,  King, Queen, Bishop, Knight, Rook] # Порядок фигур
            for x in range(8): # Пешки
                self.board[1][x] = Pawn(Color.BLACK)
                self.board[6][x] = Pawn(Color.WHITE)
            for x, piece in enumerate(order): #Фигуры
                self.board[0][x] = piece(Color.BLACK)
                self.board[7][x] = piece(Color.WHITE)

        elif self.game_type == "spacechess": #---
                
            order = [Rook, Knight, Hedgehog,  King, Queen, Hedgehog, Knight, Rook] # Порядок фигур
            self.board[5][1] = Accelerator(Color.WHITE)
            self.board[2][6] = Accelerator(Color.BLACK)
            for x in range(8): # труперы
                self.board[1][x] = Trooper(Color.BLACK)
                self.board[6][x] = Trooper(Color.WHITE)
            for x, piece in enumerate(order): #Фигуры
                self.board[0][x] = piece(Color.BLACK)
                self.board[7][x] = piece(Color.WHITE)

        elif self.game_type == "checkers": #---
            
            for x in range(0,8,2):
                self.board[1][x] = Checker(Color.BLACK) 
                self.board[5][x] = Checker(Color.WHITE)
                self.board[7][x] = Checker(Color.WHITE)  
            for x in range(1,8,2):
                self.board[6][x] = Checker(Color.WHITE)
                self.board[0][x] = Checker(Color.BLACK)
                self.board[2][x] = Checker(Color.BLACK)


    def show_board(self):
        """
        Выводит доску и ее содержимое.
        """
        print("   A B C D E F G H\n")
        for i, row in enumerate(self.board):
            print(8 - i, end="  ")
            for piece in row:
                print(str(piece) if piece else '.', end=" ")
            print(8 - i)
        print()
        print("   A B C D E F G H\n")

    def get_piece(self, x, y):
        """
        Возвращает название фигуры, находящейся на заданных координатах.

        :param x: Номер строки.
        :param y: Номер столбца.
        :return: Фигура, если клетка не пуста, иначе None.
        """
        return self.board[x][y]

    def move_piece(self, start, final):
        """
        Перемещает фигуру с начальной позиции на финальную позицию.

        :param start: Кортеж (x,y) - координаты стартовой позиции.
        :param final: Кортеж (x,y) - координаты финальной позиции. 
        :return: True, если ход совершен, иначе False.
        """
        x1, y1 = start
        
        x2, y2 = final
        
        piece = self.board[x1][y1]
        
        if piece:
            self.board[x2][y2] = piece
            self.board[x1][y1] = None
            # Перевод из пешки в дамки
            if isinstance(piece, Checker) and (x2 == 0 or x2 == 7):
                piece.crown((x2, y2), self)
            return True
        return False

# САМА ИГРА - GAME -------------------------------------------------------------------------- И Г Р А -------------------------------------
class Game:
    def __init__(self, game_type):
        """
        Начинает игру, белые начинают.

        :param game_type: Название игры.
        """
        self.board = Board(game_type)
        self.turn = Color.WHITE
        self.history = []

    def playing(self):
        """
        Игроки ходят по-очереди.
        """

        number = 1
        
        while True:
            self.board.show_board()
            if self.turn == Color.WHITE:
                print("Ходят белые! Общий номер хода -", number)
            else:
                print("Ходят черные! Общий номер хода -", number)
                      
            move = input("Введите координаты фигуры и желаймой позиции (Сначала буква, потом цифра): ")
            if move == "UNDO":
                if self.undo_move():
                    print("Доска возвращена на 1 ход назад.")
            elif self.make_move(move):
                if self.turn == Color.WHITE:
                    self.turn = Color.BLACK
                    number += 1
                else:
                    self.turn = Color.WHITE
                    number += 1
            else:
                print("Такой ход невозможен, попробуйте другой.\n")

    def make_move(self, move):
        """
        Выполняет ход на доске (duh).

        :param move: Строка с координатами хода. Пример - "a1 a2".
        :return: True, если ход совершен, иначе False.
        """
        try:
            start, final = move.split()
            
            x1, y1 = self.cut(start)
            
            x2, y2 = self.cut(final)
            
            piece = self.board.get_piece(x1, y1)
            if piece and piece.color == self.turn and piece.is_move_correct((x1, y1), (x2, y2), self.board):
                self.history.append(copy.deepcopy(self.board.board))
                self.board.move_piece((x1, y1), (x2, y2))
                return True
            return False
        except:
            return False
        

    def undo_move(self):
        if not self.history: # Ходов нет
            return False
        last_board = self.history.pop()
        self.board.board = last_board
        return True

    def cut(self, pos):
        """
        Переводит шахматные координаты в математические.

        :param pos: Шахматные координаты.
        :return: Кортеж (x, y) координат доски.
        """
        x = 8 - int(pos[1])
        y = ord(pos[0]) - ord('a')
        return x, y

class ChessGame(Game):
    def __init__(self):
        super().__init__("chess")

class CheckersGame(Game):
    def __init__(self):
        super().__init__("checkers")

class SpaceChessGame(Game):
    def __init__(self):
        super().__init__("spacechess")

if __name__ == "__main__":
    while(1):
        print("Меню выбора игры:")
        print("Введите '1' - Шахматы")
        print("Введите '2' - Шашки")
        print("Введите '3' - Космовоенные Шахматы")
        print("Введите '4' - Космовоенные Шахматы - Обучение")
        choice = input("Введите номер игры: ")

        if choice == '1':
            game = ChessGame()
            break
        elif choice == '2':
            game = CheckersGame()
            break
        elif choice == '3':
            game = SpaceChessGame()
            break
        elif choice == '4':
            print()
            print("   <<< Космовоенные Шахматы >>>\n")
            
            print("Все неизмененные фигуры - прежние.\n")
            
            print("X - еж. Передвигается как слон, но только на 1 клетку.")

            print("T - космодесантник. Ведет себя как пешка, но в начале не может пойти на 2 клетки.")
            print("Однако может ходить вперед, вперед-вправо и вперед-влево всегда. \n")

            print("^ - Космический корабли. Двигается только вправо и влево на 1-3 клетку.")

        else:
            print("Вам нужно ввести 1, 2, 3 или 4. Попробуйте еще раз.")
            print()
    game.playing()
