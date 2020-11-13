#Sunfish is a simple, but strong chess engine written in Python
#Sunfish is self contained in a py file, so it was added to the project rather than
#create a separate virtual environment with PyPy to use it



from __future__ import print_function
import re, sys, time
from itertools import count
from collections import namedtuple
from multipledispatch import dispatch

###############################################################################
# Piece-Square tables. Tune these to change sunfish's behaviour
###############################################################################

piece = { 'P': 100, 'L' : 100, 'D' : 100, 'N': 280, 'C': 280, 'B': 10000, 'F': 10000 ,'R': 479, 'Q': 929, 'K': 60000 }
pst = {
    'P': ( 0,   0,   0,   0,   0,   0,   0,   0,
            78,  83,  86,  73, 102,  82,  85,  90,
             7,  29,  21,  44,  40,  31,  44,   7,
           -17,  16,  -2,  15,  14,   0,  15, -13,
           -26,   3,  10,   9,   6,   1,   0, -23,
           -22,   9,   5, -11, -10,  -2,   3, -19,
           -31,   8,  -7, -37, -36, -14,   3, -31,
             0,   0,   0,   0,   0,   0,   0,   0),
    'L': (0, 0, 0, 0, 0, 0, 0, 0,
          78, 83, 86, 73, 102, 82, 85, 90,
          7, 29, 21, 44, 40, 31, 44, 7,
          -17, 16, -2, 15, 14, 0, 15, -13,
          -26, 3, 10, 9, 6, 1, 0, -23,
          -22, 9, 5, -11, -10, -2, 3, -19,
          -31, 8, -7, -37, -36, -14, 3, -31,
          0, 0, 0, 0, 0, 0, 0, 0),
    'D': (0, 0, 0, 0, 0, 0, 0, 0,
          78, 83, 86, 73, 102, 82, 85, 90,
          7, 29, 21, 44, 40, 31, 44, 7,
          -17, 16, -2, 15, 14, 0, 15, -13,
          -26, 3, 10, 9, 6, 1, 0, -23,
          -22, 9, 5, -11, -10, -2, 3, -19,
          -31, 8, -7, -37, -36, -14, 3, -31,
          0, 0, 0, 0, 0, 0, 0, 0),
    'N': ( -66, -53, -75, -75, -10, -55, -58, -70,
            -3,  -6, 100, -36,   4,  62,  -4, -14,
            10,  67,   1,  74,  73,  27,  62,  -2,
            24,  24,  45,  37,  33,  41,  25,  17,
            -1,   5,  31,  21,  22,  35,   2,   0,
           -18,  10,  13,  22,  18,  15,  11, -14,
           -23, -15,   2,   0,   2,   0, -23, -20,
           -74, -23, -26, -24, -19, -35, -22, -69),
    'C': (-66, -53, -75, -75, -10, -55, -58, -70,
          -3, -6, 100, -36, 4, 62, -4, -14,
          10, 67, 1, 74, 73, 27, 62, -2,
          24, 24, 45, 37, 33, 41, 25, 17,
          -1, 5, 31, 21, 22, 35, 2, 0,
          -18, 10, 13, 22, 18, 15, 11, -14,
          -23, -15, 2, 0, 2, 0, -23, -20,
          -74, -23, -26, -24, -19, -35, -22, -69),
    'B': ( -59, -78, -82, -76, -23,-107, -37, -50,
           -11,  20,  35, -42, -39,  31,   2, -22,
            -9,  39, -32,  41,  52, -10,  28, -14,
            25,  17,  20,  34,  26,  25,  15,  10,
            13,  10,  17,  23,  17,  16,   0,   7,
            14,  25,  24,  15,   8,  25,  20,  15,
            19,  20,  11,   6,   7,   6,  20,  16,
            -7,   2, -15, -12, -14, -15, -10, -10),
    'F': (-59, -78, -82, -76, -23, -107, -37, -50,
          -11, 20, 35, -42, -39, 31, 2, -22,
          -9, 39, -32, 41, 52, -10, 28, -14,
          25, 17, 20, 34, 26, 25, 15, 10,
          13, 10, 17, 23, 17, 16, 0, 7,
          14, 25, 24, 15, 8, 25, 20, 15,
          19, 20, 11, 6, 7, 6, 20, 16,
          -7, 2, -15, -12, -14, -15, -10, -10),
    'R': (  35,  29,  33,   4,  37,  33,  56,  50,
            55,  29,  56,  67,  55,  62,  34,  60,
            19,  35,  28,  33,  45,  27,  25,  15,
             0,   5,  16,  13,  18,  -4,  -9,  -6,
           -28, -35, -16, -21, -13, -29, -46, -30,
           -42, -28, -42, -25, -25, -35, -26, -46,
           -53, -38, -31, -26, -29, -43, -44, -53,
-           -30, -24, -18,   5,  -2, -18, -31, -32),
    'Q': (   6,   1,  -8,-104,  69,  24,  88,  26,
            14,  32,  60, -10,  20,  76,  57,  24,
            -2,  43,  32,  60,  72,  63,  43,   2,
             1, -16,  22,  17,  25,  20, -13,  -6,
           -14, -15,  -2,  -5,  -1, -10, -20, -22,
           -30,  -6, -13, -11, -16, -11, -16, -27,
           -36, -18,   0, -19, -15, -15, -21, -38,
           -39, -30, -31, -13, -31, -36, -34, -42),
    'K': (   4,  54,  47, -99, -99,  60,  83, -62,
           -32,  10,  55,  56,  56,  55,  10,   3,
           -62,  12, -57,  44, -67,  28,  37, -31,
           -55,  50,  11,  -4, -19,  13,   0, -49,
           -55, -43, -52, -28, -51, -47,  -8, -50,
           -47, -42, -43, -79, -64, -32, -29, -32,
            -4,   3, -14, -50, -57, -18,  13,   4,
            17,  30,  -3, -14,   6,  -1,  40,  18)
}

capture_table = [[4, 4, 4, 4, 5, 1], [4, 4, 4, 4, 5, 2], [6, 6, 4, 4, 5, 2],
                 [5, 5, 5, 4, 5, 3], [4, 4, 5, 5, 6, 5], [6, 6, 6, 5, 6, 4]]

# Pad tables and join piece and pst dictionaries
for k, table in pst.items():
    padrow = lambda row: (0,) + tuple(x+piece[k] for x in row) + (0,)
    pst[k] = sum((padrow(table[i*8:i*8+8]) for i in range(8)), ())
    pst[k] = (0,)*20 + pst[k] + (0,)*20

###############################################################################
# Global constants
###############################################################################

# Our board is represented as a 120 character string. The padding allows for
# fast detection of moves that don't stay within the board.
A1, H1, A8, H8 = 91, 98, 21, 28
initial = (
    '         \n'  #   0 -  9
    '         \n'  #  10 - 19
    ' rcbqkfnr\n'  #  20 - 29
    ' dddpplll\n'  #  30 - 39
    ' ........\n'  #  40 - 49
    ' ........\n'  #  50 - 59
    ' ........\n'  #  60 - 69
    ' ........\n'  #  70 - 79
    ' LLLPPDDD\n'  #  80 - 89
    ' RNFQKBCR\n'  #  90 - 99
    '         \n'  # 100 -109
    '         \n'  # 110 -119
)

# Lists of possible moves for each piece type.
N, E, S, W, NE, NW, SE, SW = -10, 1, 10, -1, -9, -11, 11, 9 #finish combination math variables
directions = {
    'P': (N, N + W, N + E),
    'L': (N, NW, NE),
    'D': (N, NW, NE),
    'N': (N, E, NE, S, SW, SE, W, NW),
    'C': (N, E, NE, S, SW, SE, W, NW),
    'B': (N, NW, NE),
    'F': (N, NW, NE),
    'R': (N, E, NE, S, SW, SE, W, NW),
    'Q': (N, E, NE, S, SW, SE, W, NW),
    'K': (N, E, NE, S, SW, SE, W, NW)
}

# Mate value must be greater than 8*queen + 2*(rook+knight+bishop)
# King value is set to twice this value such that if the opponent is
# 8 queens up, but we got the king, we still exceed MATE_VALUE.
# When a MATE is detected, we'll set the score to MATE_UPPER - plies to get there
# E.g. Mate in 3 will be MATE_UPPER - 6
MATE_LOWER = piece['K'] - 10*piece['Q']
MATE_UPPER = piece['K'] + 10*piece['Q']

# The table size is the maximum number of elements in the transposition table.
TABLE_SIZE = 1e7

# Constants for tuning search
QS_LIMIT = 219
EVAL_ROUGHNESS = 13
DRAW_TEST = True


###############################################################################
# Chess logic
###############################################################################

class Position(namedtuple('Position', 'board score')):
    """ A state of a chess game
    board -- a 120 char representation of the board
    score -- the board evaluation
    wc -- the castling rights, [west/queen side, east/king side]
    bc -- the opponent castling rights, [west/king side, east/queen side]
    ep - the en passant square
    kp - the king passant square
    """

    @dispatch(int, str)
    def gen_moves(self, num_moves_made, piece_moved):
        # For each of our pieces, iterate through each possible 'ray' of moves,
        # as defined in the 'directions' map. The rays are broken e.g. by
        # captures or immediately in case of pieces such as knights.

        temp_board = Position(self.board, 0)
        for i, p in enumerate(self.board):
            if not p.isupper():
                continue
            if piece_moved == "N" or piece_moved == "C":
                for d in directions[piece_moved]:
                    temp_num_moves_made = num_moves_made
                    for j in count(i + d, d):
                        num = 0
                        q = temp_board.board[j]
                        # Stay inside the board, and off friendly pieces
                        if q.isspace() or q.isupper():
                            break
                        # Rook capture
                        if q.islower and not q == ".":
                            num_moves_made = 4
                        yield i, j
                        temp_board.move((i, j), 0)
                        temp_num_moves_made = temp_num_moves_made + 1
                        temp_board.gen_moves(temp_num_moves_made, piece_moved)

                        # Move it
                        num += 1
                        # Stop crawlers from sliding, and sliding after captures
                        if (p in 'PLDRNCBFRQK' or q.islower()) or (temp_num_moves_made >= 5):
                            break

            if piece_moved == "K" or piece_moved == "Q":
                if num_moves_made < 3:
                    for d in directions[p]:
                        for j in count(i + d, d):
                            num = 0
                            q = temp_board.board[j]
                            # Stay inside the board, and off friendly pieces
                            if q.isspace() or q.isupper():
                                break
                            if q.islower and not q == ".":
                                num_moves_made = 3
                            # Rook capture
                            yield i, j
                            temp_board.move((i, j), 0)
                            temp_board.rotate()
                            num_moves_made = num_moves_made + 1
                            temp_board.gen_moves(num_moves_made, piece_moved)

                            # Move it
                            num += 1
                            # Stop crawlers from sliding, and sliding after captures
                            if (p in 'PLDRNCBFRQK' or q.islower()) and (num_moves_made >= 3):
                                break

    @dispatch(int)
    def gen_moves(self, num_moves_made):
        # For each of our pieces, iterate through each possible 'ray' of moves,
        # as defined in the 'directions' map. The rays are broken e.g. by
        # captures or immediately in case of pieces such as knights.

        temp_board = Position(self.board, 0)
        for i, p in enumerate(self.board):
            if not p.isupper():
                continue
            if p == "N" or p == "C":
                for d in directions[p]:
                    num_moves_made = 0
                    for j in count(i + d, d):
                        num = 0
                        q = temp_board.board[j]
                        # Stay inside the board, and off friendly pieces
                        if q.isspace() or q.isupper():
                            break
                        if q.islower and not q == ".":
                                num_moves_made = 4
                            # Rook capture
                        temp_board.move((i, j), 0)
                        num_moves_made = num_moves_made + 1
                        for r, t in temp_board.gen_moves(num_moves_made, "N"):
                            yield r, t
                        yield i, j
                            # Move it
                        num += 1
                        # Stop crawlers from sliding, and sliding after captures
                        if (p in 'PLDRNCBFRQK' or q.islower()) and (num_moves_made >= 5):
                             break

            if p == "K" or p == "Q":
                for d in directions[p]:
                    num_moves_made = 0
                    for j in count(i + d, d):
                        num = 0
                        q = temp_board.board[j]
                        # Stay inside the board, and off friendly pieces
                        if q.isspace() or q.isupper():
                            break
                        if q.islower and not q == ".":
                            num_moves_made = 3
                        # Rook capture
                        yield i, j
                        temp_board.move((i, j), 0)
                        temp_board.rotate()
                        num_moves_made = num_moves_made + 1
                        temp_board.gen_moves(num_moves_made, "K")

                        # Move it
                        num += 1
                        # Stop crawlers from sliding, and sliding after captures
                        if (p in 'PLDRNCBFRQK' or q.islower()) and (num_moves_made >= 3):
                            break
            if p == "B" or p == "F" or p == "P" or "L" or p == "D" or p == "R":
                for d in directions[p]:
                    for j in count(i+d, d):
                        num = 0
                        q = self.board[j]
                        # Stay inside the board, and off friendly pieces
                        if q.isspace() or q.isupper():
                            break
                        # Rook capture


                        # Move it
                        yield i, j
                        num += 1
                        # Stop crawlers from sliding, and sliding after captures
                        if p in 'PLDRNCBFRQK' or q.islower() or (num == 3 and p in 'KQ') or (num == 5 and (p in 'N' or
                            p in 'C')):
                            break
                    '''
                    if p in 'KQ':   #checks to see if moving king or queen, pieces that can move more than once in a turn
                        move = input('Your move: ')
                        for move in range(0,2): #iterates up to three times, allows for moving up the three spaces with piece
                            print('Move #{}'.format(move+1))
                            move_again = input('Do you want to move again?(y/n): ') #gives player the option to move again if able to or prematurely end their turn
                            if move_again == 'y':
                                move = input('Your move: ')
                            else:
                                break
                    '''
    def rotate(self):
        ''' Rotates the board, preserving enpassant '''
        return Position(
            self.board[::-1].swapcase(), -self.score)

    def nullmove(self):
        ''' Like rotate, but clears ep and kp '''
        return Position(
            self.board[::-1].swapcase(), -self.score)

    @dispatch()
    def move(self):
        board = self.board
        score = self.score
        return Position(board, score).rotate()

    def user_move(self, u_move):
        match = re.match('([a-h][1-8])' * 2, u_move)
        move = parse(match.group(1)), parse(match.group(2))
        if u_move == "skip":
            self.append(self[-1].move())
        else:
            self.append(self[-1].move(move, 0))

    @dispatch(tuple, int)
    def move(self, move, count):
        i, j = move
        p, q = self.board[i], self.board[j]
        pieces = str(piece)
        put = lambda board, i, p: board[:i] + p + board[i+1:]
        # Copy variables and reset ep and kp
        board = self.board
        score = self.score + self.value(move)
        '''
        # attempt for iterations of king and queen movement
        if pieces in 'KQ':  # checks to see if moving king or queen, pieces that can move more than once in a turn
            # move = input('Your move: ')
            for move in range(0, 2):  # iterates up to three times, allows for moving up the three spaces with piece
                print('Move #{}'.format(move + 1))
                move_again = input(
                    'Do you want to move again?(y/n): ')  # gives player the option to move again if able to or prematurely end their turn
                if move_again == 'y':
                    move = input('Your move: ')
                else:
                    break
        '''
        board = put(board, j, board[i])
        board = put(board, i, '.')
        # Actual move
        if pieces in 'KQ':
            if count < 2:
                print("Move #{}".format(move+1))
                count += 1
                move_again = input("Do you want to move again?(y/n): ")
                if move_again == 'y':
                    move(self, move, count)
                else:
                    count = 2

        # Castling rights, we move the rook or capture the opponent's

        # We rotate the returned position, so it's ready for the next player
        return Position(board, score).rotate()

    def find_attacker(self, current_piece, position):
        board = self.board
        score = self.score
        chance1 = 7
        chance2 = 7
        chance3 = 7
        three_highest_attackers = ""
        opponent_view = Position(board, score).rotate()
        for i, j in opponent_view.gen_moves(0):
            match2 = re.match('([a-h])''([1-8])', i)
            if j == position:
                if board[(109-((ord(match2.group(2))-48)*10))-(ord(match2.group(1))-96)] == "K":
                    if current_piece == "K":
                        if chance1 >= 4:
                            chance1 = 4
                            three_highest_attackers[0] = "K"
                        if chance2 > 4 and chance2 >= chance1:
                            chance2 = 4
                            three_highest_attackers[1] = "K"
                        if chance3 > 4 and chance3 >= chance1 and chance3 >= chance2:
                            chance3 = 4
                            three_highest_attackers[2] = "K"
                    if current_piece == "Q":
                        if chance1 >= 4:
                            chance1 = 4
                            three_highest_attackers[0] = "K"
                        if chance2 > 4 and chance2 >= chance1:
                            chance2 = 4
                            three_highest_attackers[1] = "K"
                        if chance3 > 4 and chance3 >= chance1 and chance3 >= chance2:
                            chance3 = 4
                            three_highest_attackers[2] = "K"
                    if current_piece == "N":
                        if chance1 >= 4:
                            chance1 = 4
                            three_highest_attackers[0] = "K"
                        if chance2 > 4 and chance2 >= chance1:
                            chance2 = 4
                            three_highest_attackers[1] = "K"
                        if chance3 > 4 and chance3 >= chance1 and chance3 >= chance2:
                            chance3 = 4
                            three_highest_attackers[2] = "K"
                    if current_piece == "B":
                        if chance1 >= 4:
                            chance1 = 4
                            three_highest_attackers[0] = "K"
                        if chance2 > 4 and chance2 >= chance1:
                            chance2 = 4
                            three_highest_attackers[1] = "K"
                        if chance3 > 4 and chance3 >= chance1 and chance3 >= chance2:
                            chance3 = 4
                            three_highest_attackers[2] = "K"
                    if current_piece == "R":
                        if chance1 >= 5:
                            chance1 = 5
                            three_highest_attackers[0] = "K"
                        if chance2 > 5 and chance2 >= chance1:
                            chance2 = 5
                            three_highest_attackers[1] = "K"
                        if chance3 > 5 and chance3 >= chance1 and chance3 >= chance2:
                            chance3 = 5
                            three_highest_attackers[2] = "K"
                    if current_piece == "P":
                        if chance1 >= 1:
                            chance1 = 1
                            three_highest_attackers[0] = "K"
                        if chance2 > 1 and chance2 >= chance1:
                            chance2 = 1
                            three_highest_attackers[1] = "K"
                        if chance3 > 1 and chance3 >= chance1 and chance3 >= chance2:
                            chance3 = 1
                            three_highest_attackers[2] = "K"

                if board[(109-((ord(match2.group(2))-48)*10))-(ord(match2.group(1))-96)] == "Q":
                    if current_piece == "K":
                        if chance1 >= 4:
                            chance1 = 4
                            three_highest_attackers[0] = "Q"
                        if chance2 > 4 and chance2 >= chance1:
                            chance2 = 4
                            three_highest_attackers[1] = "Q"
                        if chance3 > 4 and chance3 >= chance1 and chance3 >= chance2:
                            chance3 = 4
                            three_highest_attackers[2] = "Q"
                    if current_piece == "Q":
                        if chance1 >= 4:
                            chance1 = 4
                            three_highest_attackers[0] = "Q"
                        if chance2 > 4 and chance2 >= chance1:
                            chance2 = 4
                            three_highest_attackers[1] = "Q"
                        if chance3 > 4 and chance3 >= chance1 and chance3 >= chance2:
                            chance3 = 4
                            three_highest_attackers[2] = "Q"
                    if current_piece == "N":
                        if chance1 >= 4:
                            chance1 = 4
                            three_highest_attackers[0] = "Q"
                        if chance2 > 4 and chance2 >= chance1:
                            chance2 = 4
                            three_highest_attackers[1] = "Q"
                        if chance3 > 4 and chance3 >= chance1 and chance3 >= chance2:
                            chance3 = 4
                            three_highest_attackers[2] = "Q"
                    if current_piece == "B":
                        if chance1 >= 4:
                            chance1 = 4
                            three_highest_attackers[0] = "Q"
                        if chance2 > 4 and chance2 >= chance1:
                            chance2 = 4
                            three_highest_attackers[1] = "Q"
                        if chance3 > 4 and chance3 >= chance1 and chance3 >= chance2:
                            chance3 = 4
                            three_highest_attackers[2] = "Q"
                    if current_piece == "R":
                        if chance1 >= 5:
                            chance1 = 5
                            three_highest_attackers[0] = "Q"
                        if chance2 > 5 and chance2 >= chance1:
                            chance2 = 5
                            three_highest_attackers[1] = "Q"
                        if chance3 > 5 and chance3 >= chance1 and chance3 >= chance2:
                            chance3 = 5
                            three_highest_attackers[2] = "Q"
                    if current_piece == "P":
                        if chance1 >= 2:
                            chance1 = 2
                            three_highest_attackers[0] = "Q"
                        if chance2 > 2 and chance2 >= chance1:
                            chance2 = 2
                            three_highest_attackers[1] = "Q"
                        if chance3 > 2 and chance3 >= chance1 and chance3 >= chance2:
                            chance3 = 2
                            three_highest_attackers[2] = "Q"

                if board[(109-((ord(match2.group(2))-48)*10))-(ord(match2.group(1))-96)] == "B":
                    if current_piece == "K":
                        if chance1 >= 5:
                            chance1 = 5
                            three_highest_attackers[0] = "B"
                        if chance2 > 5 and chance2 >= chance1:
                            chance2 = 5
                            three_highest_attackers[1] = "B"
                        if chance3 > 5 and chance3 >= chance1 and chance3 >= chance2:
                            chance3 = 5
                            three_highest_attackers[2] = "B"
                    if current_piece == "Q":
                        if chance1 >= 5:
                            chance1 = 5
                            three_highest_attackers[0] = "B"
                        if chance2 > 5 and chance2 >= chance1:
                            chance2 = 5
                            three_highest_attackers[1] = "B"
                        if chance3 > 5 and chance3 >= chance1 and chance3 >= chance2:
                            chance3 = 5
                            three_highest_attackers[2] = "B"
                    if current_piece == "N":
                        if chance1 >= 5:
                            chance1 = 5
                            three_highest_attackers[0] = "B"
                        if chance2 > 5 and chance2 >= chance1:
                            chance2 = 5
                            three_highest_attackers[1] = "B"
                        if chance3 > 5 and chance3 >= chance1 and chance3 >= chance2:
                            chance3 = 5
                            three_highest_attackers[2] = "B"
                    if current_piece == "B":
                        if chance1 >= 4:
                            chance1 = 4
                            three_highest_attackers[0] = "B"
                        if chance2 > 4 and chance2 >= chance1:
                            chance2 = 4
                            three_highest_attackers[1] = "B"
                        if chance3 > 4 and chance3 >= chance1 and chance3 >= chance2:
                            chance3 = 4
                            three_highest_attackers[2] = "B"
                    if current_piece == "R":
                        if chance1 >= 5:
                            chance1 = 5
                            three_highest_attackers[0] = "B"
                        if chance2 > 5 and chance2 >= chance1:
                            chance2 = 5
                            three_highest_attackers[1] = "B"
                        if chance3 > 5 and chance3 >= chance1 and chance3 >= chance2:
                            chance3 = 5
                            three_highest_attackers[2] = "B"
                    if current_piece == "P":
                        if chance1 >= 3:
                            chance1 = 3
                            three_highest_attackers[0] = "B"
                        if chance2 > 3 and chance2 >= chance1:
                            chance2 = 3
                            three_highest_attackers[1] = "B"
                        if chance3 > 3 and chance3 >= chance1 and chance3 >= chance2:
                            chance3 = 3
                            three_highest_attackers[2] = "B"

                if board[(109-((ord(match2.group(2))-48)*10))-(ord(match2.group(1))-96)] == "P":
                    if current_piece == "K":
                        if chance1 >= 6:
                            chance1 = 6
                            three_highest_attackers[0] = "P"
                        if chance2 > 6 and chance2 >= chance1:
                            chance2 = 6
                            three_highest_attackers[1] = "P"
                        if chance3 > 6 and chance3 >= chance1 and chance3 >= chance2:
                            chance3 = 6
                            three_highest_attackers[2] = "P"
                    if current_piece == "Q":
                        if chance1 >= 6:
                            chance1 = 6
                            three_highest_attackers[0] = "P"
                        if chance2 > 6 and chance2 >= chance1:
                            chance2 = 6
                            three_highest_attackers[1] = "P"
                        if chance3 > 6 and chance3 >= chance1 and chance3 >= chance2:
                            chance3 = 6
                            three_highest_attackers[2] = "P"
                    if current_piece == "N":
                        if chance1 >= 6:
                            chance1 = 6
                            three_highest_attackers[0] = "P"
                        if chance2 > 6 and chance2 >= chance1:
                            chance2 = 6
                            three_highest_attackers[1] = "P"
                        if chance3 > 6 and chance3 >= chance1 and chance3 >= chance2:
                            chance3 = 6
                            three_highest_attackers[2] = "P"
                    if current_piece == "B":
                        if chance1 >= 5:
                            chance1 = 5
                            three_highest_attackers[0] = "P"
                        if chance2 > 5 and chance2 >= chance1:
                            chance2 = 5
                            three_highest_attackers[1] = "P"
                        if chance3 > 5 and chance3 >= chance1 and chance3 >= chance2:
                            chance3 = 5
                            three_highest_attackers[2] = "P"
                    if current_piece == "R":
                        if chance1 >= 6:
                            chance1 = 6
                            three_highest_attackers[0] = "P"
                        if chance2 > 6 and chance2 >= chance1:
                            chance2 = 6
                            three_highest_attackers[1] = "P"
                        if chance3 > 6 and chance3 >= chance1 and chance3 >= chance2:
                            chance3 = 6
                            three_highest_attackers[2] = "P"
                    if current_piece == "P":
                        if chance1 >= 4:
                            chance1 = 4
                            three_highest_attackers[0] = "P"
                        if chance2 > 4 and chance2 >= chance1:
                            chance2 = 4
                            three_highest_attackers[1] = "P"
                        if chance3 > 4 and chance3 >= chance1 and chance3 >= chance2:
                            chance3 = 4
                            three_highest_attackers[2] = "P"
        return three_highest_attackers, chance1, chance2, chance3

    def value(self, move):
        i, j = move
        p, q = self.board[i], self.board[j]
        # Actual move
        score = pst[p][j] - pst[p][i]
        # Capture
        if q.islower():
            score += pst[q.upper()][119-j]

        # Special pawn stuff
        '''if p == 'P':
            if A8 <= j <= H8:
                score += pst['Q'][j] - pst['P'][j]
            if j == self.ep:
                score += pst['P'][119-(j+S)]'''
        return score

###############################################################################
# Search logic
###############################################################################


# lower <= s(pos) <= upper
Entry = namedtuple('Entry', 'lower upper')


class Searcher:
    def __init__(self):
        self.tp_score = {}
        self.tp_move = {}
        self.history = set()
        self.nodes = 0

    def bound(self, pos, gamma, depth, root=True):
        """ returns r where
                s(pos) <= r < gamma    if gamma > s(pos)
                gamma <= r <= s(pos)   if gamma <= s(pos)"""
        self.nodes += 1

        # Depth <= 0 is QSearch. Here any position is searched as deeply as is needed for
        # calmness, and from this point on there is no difference in behaviour depending on
        # depth, so so there is no reason to keep different depths in the transposition table.
        depth = max(depth, 0)

        # Sunfish is a king-capture engine, so we should always check if we
        # still have a king. Notice since this is the only termination check,
        # the remaining code has to be comfortable with being mated, stalemated
        # or able to capture the opponent king.
        if pos.score <= -MATE_LOWER:
            return -MATE_UPPER

        # We detect 3-fold captures by comparing against previously
        # _actually played_ positions.
        # Note that we need to do this before we look in the table, as the
        # position may have been previously reached with a different score.
        # This is what prevents a search instability.
        # FIXME: This is not true, since other positions will be affected by
        # the new values for all the drawn positions.
        if DRAW_TEST:
            if not root and pos in self.history:
                return 0

        # Look in the table if we have already searched this position before.
        # We also need to be sure, that the stored search was over the same
        # nodes as the current search.
        entry = self.tp_score.get((pos, depth, root), Entry(-MATE_UPPER, MATE_UPPER))
        if entry.lower >= gamma and (not root or self.tp_move.get(pos) is not None):
            return entry.lower
        if entry.upper < gamma:
            return entry.upper

        # Here extensions may be added
        # Such as 'if in_check: depth += 1'

        # Generator of moves to search in order.
        # This allows us to define the moves, but only calculate them if needed.
        def moves():
            count = 0
            # First try not moving at all. We only do this if there is at least one major
            # piece left on the board, since otherwise zugzwangs are too dangerous.
            if depth > 0 and not root and any(c in pos.board for c in 'RBNQFC'):
                yield None, -self.bound(pos.nullmove(), 1-gamma, depth-3, root=False)
            # For QSearch we have a different kind of null-move, namely we can just stop
            # and not capture anythign else.
            if depth == 0:
                yield None, pos.score
            # Then killer move. We search it twice, but the tp will fix things for us.
            # Note, we don't have to check for legality, since we've already done it
            # before. Also note that in QS the killer must be a capture, otherwise we
            # will be non deterministic.
            killer = self.tp_move.get(pos)
            if killer and (depth > 0 or pos.value(killer) >= QS_LIMIT):
                yield killer, -self.bound(pos.move(killer, count), 1 - gamma, depth - 1, root=False)
            # Then all the other moves
            for move in sorted(pos.gen_moves(0), key=pos.value, reverse=True):
            #for val, move in sorted(((pos.value(move), move) for move in pos.gen_moves()), reverse=True):
                # If depth == 0 we only try moves with high intrinsic score (captures and
                # promotions). Otherwise we do all moves.
                if depth > 0 or pos.value(move) >= QS_LIMIT:
                    yield move, -self.bound(pos.move(move, count), 1 - gamma, depth - 1, root=False)

        count = 0
        # Run through the moves, shortcutting when possible
        best = -MATE_UPPER
        for move, score in moves():
            best = max(best, score)
            if best >= gamma:
                # Clear before setting, so we always have a value
                if len(self.tp_move) > TABLE_SIZE: self.tp_move.clear()
                # Save the move for pv construction and killer heuristic
                self.tp_move[pos] = move
                break

        # Stalemate checking is a bit tricky: Say we failed low, because
        # we can't (legally) move and so the (real) score is -infty.
        # At the next depth we are allowed to just return r, -infty <= r < gamma,
        # which is normally fine.
        # However, what if gamma = -10 and we don't have any legal moves?
        # Then the score is actaully a draw and we should fail high!
        # Thus, if best < gamma and best < 0 we need to double check what we are doing.
        # This doesn't prevent sunfish from making a move that results in stalemate,
        # but only if depth == 1, so that's probably fair enough.
        # (Btw, at depth 1 we can also mate without realizing.)
        if best < gamma and best < 0 < depth:
            is_dead = lambda pos: any(pos.value(m) >= MATE_LOWER for m in pos.gen_moves(0))
            if all(is_dead(pos.move(m, count)) for m in pos.gen_moves(0)):
                in_check = is_dead(pos.nullmove())
                best = -MATE_UPPER if in_check else 0

        # Clear before setting, so we always have a value
        if len(self.tp_score) > TABLE_SIZE: self.tp_score.clear()
        # Table part 2
        if best >= gamma:
            self.tp_score[pos, depth, root] = Entry(best, entry.upper)
        if best < gamma:
            self.tp_score[pos, depth, root] = Entry(entry.lower, best)

        return best

    def search(self, pos, history=()):
        """ Iterative deepening MTD-bi search """
        self.nodes = 0
        if DRAW_TEST:
            self.history = set(history)
            # print('# Clearing table due to new history')
            self.tp_score.clear()

        # In finished games, we could potentially go far enough to cause a recursion
        # limit exception. Hence we bound the ply.
        for depth in range(1, 1000):
            # The inner loop is a binary search on the score of the position.
            # Inv: lower <= score <= upper
            # 'while lower != upper' would work, but play tests show a margin of 20 plays
            # better.
            lower, upper = -MATE_UPPER, MATE_UPPER
            while lower < upper - EVAL_ROUGHNESS:
                gamma = (lower+upper+1)//2
                score = self.bound(pos, gamma, depth)
                if score >= gamma:
                    lower = score
                if score < gamma:
                    upper = score
            # We want to make sure the move to play hasn't been kicked out of the table,
            # So we make another call that must always fail high and thus produce a move.
            self.bound(pos, lower, depth)
            # If the game hasn't finished we can retrieve our move from the
            # transposition table.
            yield depth, self.tp_move.get(pos), self.tp_score.get((pos, depth, True)).lower


###############################################################################
# User interface
###############################################################################


def parse(c):
    fil, rank = ord(c[0]) - ord('a'), int(c[1]) - 1
    return A1 + fil - 10*rank


def render(i):
    rank, fil = divmod(i - A1, 10)
    return chr(fil + ord('a')) + str(-rank + 1)


def print_pos(pos):
    print()
    uni_pieces = {'R': '♜', 'N': '♞', 'B': '♝', 'Q': '♛', 'K': '♚', 'P': '♟', 'C': '♞', 'F': '♝', 'L': '♟',
                  'D': '♟', 'r': '♖', 'n': '♘', 'c': '♘', 'b': '♗', 'f': '♗', 'q': '♕', 'k': '♔', 'p': '♙',
                  'd': '♙', 'l': '♙', '.': '·'}
    for i, row in enumerate(pos.board.split()):
        print(' ', 8-i, ' '.join(uni_pieces.get(p, p) for p in row))
    print('    a b c d e f g h \n\n')


def main():
    hist = [Position(initial, 0)]
    searcher = Searcher()
    count = 0
    while True:
        print_pos(hist[-1])

        '''if hist[-1].score <= -MATE_LOWER:
            print("You lost")
            break
        '''

        king_is_alive = False
        for i in range(0, 9):
            for j in range(0, 9):
                check = hist[-1].board[(109 - (i * 10)) - j]
                if check == "K":
                    king_is_alive = True
                    break
            if king_is_alive:
                break

        if not king_is_alive:
            print("You lost")
            break

            # Fire up the engine to look for a move.
        '''start = time.time()
        for _depth, move, score in searcher.search(hist[-1], hist):
            if time.time() - start > 1:
                break

            if score == MATE_UPPER:
                print("Checkmate!")


        def ai_move():
            return render(119 - move[0]) + render(119 - move[1])

            # The black player moves from a rotated position, so we have to
            # 'back rotate' the move before printing it.
        print(ai_move())
        skip = False

        def skip_ai():
            skip = True

        if skip:
            hist.append(hist[-1].move())
            hist[-1].board

        else:
            hist.append(hist[-1].move(move, count))
            hist[-1].board'''
        is_continue = True
        play = input("Do you want to move this turn y/n ")
        if play == "y":
            is_continue = True
        if play == "n":
            is_continue = False
        # We query the user until she enters a (pseudo) legal move.
        move = None

        different_count = 0

        while is_continue and different_count <= 2:
            while move not in hist[-1].gen_moves(0):
                match = re.match('([a-h][1-8])'*2, input('Your move: '))
                match2 = re.match('([a-h])''([1-8])', match.group(1))
                print(match.group(1))
                print((109-((ord(match2.group(2))-48)*10)))
                print((hist[-1].board[parse(match.group(1))]))
                '''if ((hist[-1].board[(109-((ord(match2.group(2))-48)*10))-(ord(match2.group(1))-96)]).lower() == 'q' or
                        (hist[-1].board[(109-((ord(match2.group(2))-48)*10))-(ord(match2.group(1))-96)]).lower() == 'k'
                        or (hist[-1].board[(109-((ord(match2.group(2))-48)*10))-(ord(match2.group(1))-96)]).lower()
                        == 'n'):'''
                different_count += 1

                different_count = 3
                if match:
                   move = parse(match.group(1)), parse(match.group(2))
                else:
                    # Inform the user when invalid input (e.g. "help") is entered
                    print("Please enter a move like g8f6")

        if is_continue:
            hist.append(hist[-1].move(move, count)) #possible need to back line up one tab
        else:
            hist.append(hist[-1].move())
        # After our move we rotate the board and print it again.
        # This allows us to see the effect of our move.
        print_pos(hist[-1].rotate())
        '''
        if hist[-1].score <= -MATE_LOWER:
            print("You won")
            break
        '''
        print_pos(hist[-1].rotate())

        king_is_alive = False
        for i in range(0, 9):
            for j in range(0, 9):
                check = hist[-1].board[(109 - (i * 10)) - j]
                if check == "K":
                    king_is_alive = True
                    break
            if king_is_alive:
                break

        if not king_is_alive:
            print("You won")
            break

        # Fire up the engine to look for a move.
        start = time.time()
        for _depth, move, score in searcher.search(hist[-1], hist):
            if time.time() - start > 1:
                break

        '''if score == MATE_UPPER:
            print("Checkmate!")'''


        def ai_move():
            return render(119 - move[0]) + render(119 - move[1])

        # The black player moves from a rotated position, so we have to
        # 'back rotate' the move before printing it.
        print(ai_move())
        skip = False

        def skip_ai():
            skip = True

        if skip:
            hist.append(hist[-1].move())
            hist[-1].board

        else:
            hist.append(hist[-1].move(move, count))
            hist[-1].board
        count = count + 1
        print("Round: " + str(count))


if __name__ == '__main__':
    main()