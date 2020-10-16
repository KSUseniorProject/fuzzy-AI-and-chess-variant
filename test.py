import random
from time import sleep
from tkinter import *

import chess
import chess.svg
import np
from PIL import Image, ImageTk, PngImagePlugin
from reportlab.graphics import renderPDF, renderPM
from svglib.svglib import svg2rlg

board_coord = [["A8","B8","C8","D8","E8","F8","G8","H8"],
               ["A7","B7","C7","D7","E7","F7","G7","H7"],
               ["A6","B6","C6","D6","E6","F6","G6","H6"],
               ["A5","B5","C5","D5","E5","F5","G5","H5"],
               ["A4","B4","C4","D4","E4","F4","G4","H4"],
               ["A3","B3","C3","D3","E3","F3","G3","H3"],
               ["A2","B2","C2","D2","E2","F2","G2","H2"],
               ["A1","B1","C1","D1","E1","F1","G1","H1"]]
cur_board_img = ""
cur_board = ""
cur_piece = ""
cp_int = 0
move_to = ""
mt_int = 0
die_img = ""
move_counter = 0
my_moves = 0

def get_svg(svg_file) :
	drawing = svg2rlg(svg_file)
	renderPM.drawToFile(drawing,"tmp.png",fmt="PNG")

def select_piece(event) :               # shows available attacks/moves, pawns only show attacks
	global cur_piece,move_to,cp_int,mt_int
	x_coord = event.x
	y_coord = event.y
	x_coord -= 31
	y_coord -= 31
	x = x_coord / 92
	y = y_coord / 92
	cur_piece = board_coord[int(y)][int(x)]
#	print("cp_y = ", int(y))
#	print("cp_x = ", int(x))
	cp_int = (int(y)*8) + int(x)
	print("cp_int = ",cp_int)
	squares = board.attacks(getattr(chess,cur_piece))
	draw_board(squares)

def move_piece(event) :
    global cur_piece,move_to,move_counter,my_moves,cp_int,mt_int
    x_coord = event.x
    y_coord = event.y
    x_coord -= 31
    y_coord -= 31
    x = x_coord / 92
    y = y_coord / 92
    move_to = board_coord[int(y)][int(x)]
    mt_int = (int(y)*8) + int(x)
    print("mt_int = ",mt_int)
    squares = ""
    move_uci = cur_piece + move_to
    my_move = chess.Move.from_uci(move_uci.lower())
    if (my_move in board.legal_moves) : 
        if (is_capture()) :
#            board.push(move=my_move)
#            draw_board(squares)
#        else :
            board.push(move=my_move)
            draw_board(squares)
            my_moves += 1
            if (my_moves < 3) :
                board.push(chess.Move.null())
            else :
                for i in range (0,3) :
                    AI()
                    if (i < 2) :
                        board.push(chess.Move.null())
                my_moves = 0
        else :
            board.push(chess.Move.null())
    else :
        print("!!!!!!!!!!!!!!!!!\nILLEGAL MOVE\n!!!!!!!!!!!!!!!!!")

# call roll_die() on attack

#        if (chess.Board.is_checkmate() or chess.Board.is_stalemate()) :		# not working, implementing later
#            img = Image.open("game_over.png")
#            cur_board_img = ImageTk.PhotoImage(img)
#            panel.config(image=cur_board_img)

def AI() :
    global cur_piece,move_to,move_counter
    cur_piece = board_coord[1][move_counter]
    move_to = board_coord[2][move_counter]
    move_counter += 1
    squares = ""
    move_uci = cur_piece + move_to
    my_move = chess.Move.from_uci(move_uci.lower())
    if (is_capture()) :
        board.push(move=my_move)
        draw_board(squares)
    else :
        board.push(chess.Move.null())

def is_capture() :
    global cp_int,mt_int
    cp = board.piece_at(cp_int)
    mt = board.piece_at(mt_int)
    print("cur_piece = ",cp)
    print("move_to = ",mt)
    print(mt)
    if (str(mt) is not 'None') :
        roll_die()
        print("Rolling die")
    return True

def roll_die() :
    global die_number,die_img
    roll_list = []
    counter = 6
    rand_num = ""
    while (counter > 0) :
        rand_num = random.randint(1,6)
        roll_list.append(rand_num)
        counter -= 1
        img = Image.open("{}.png".format(rand_num))
        die_img = ImageTk.PhotoImage(img)
        die.config(image=die_img)
        die.update()
        sleep(.2)
    img = Image.open("{}.png".format(rand_num))
    die_img = ImageTk.PhotoImage(img)
    die.config(image=die_img)
    die.update()
    
#    if (roll_list[5] > 3) :
#        return true
#    else :
#        return false

def draw_board(squares) :
    f = open ("tmp.svg","w")
    f.write(chess.svg.board(board,squares=squares,size=800))
    f.close	
    get_svg("tmp.svg")
    img = Image.open("tmp.png")
    cur_board_img = ImageTk.PhotoImage(img)
    panel.config(image=cur_board_img)
    panel.image=cur_board_img

# graveyard images, determine dead character by comparing Board FENs

window = Tk()
window.title("AI Chess Variant")
window.geometry("1200x900")

board = chess.Board(chess.STARTING_BOARD_FEN)

die_number = StringVar()
die_number.set("")

f = open ("tmp.svg","w")
f.write(chess.svg.board(board,size=800))
f.close	
get_svg("tmp.svg")
img = Image.open("tmp.png")
cur_board_img = ImageTk.PhotoImage(img)

panel = Label(window, image=cur_board_img)
panel.bind("<Button-1>",select_piece)
panel.bind("<Button-3>",move_piece)
panel.pack()

die = Label(window,image="",height=50,width=50,font=("Arial",50))
die.pack()

window.mainloop()
