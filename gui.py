import chess
import chess.svg
import tkinter as tk
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from PIL import Image, ImageTk, PngImagePlugin

def get_svg(svg_file):
	drawing = svg2rlg(svg_file)
	renderPM.drawToFile(drawing, "tmp.png", fmt="PNG")

window = tk.Tk()
board = chess.Board(chess.STARTING_BOARD_FEN)
squares = board.attacks(chess.A2)

f = open ("tmp.svg","w")
f.write(chess.svg.board(board, size=800))
f.close

get_svg("tmp.svg")

img = Image.open("tmp.png")
pimg = ImageTk.PhotoImage(img)
size = img.size
frame = tk.Canvas(window, width=size[0], height=size[1])
frame.pack()
frame.create_image(0,0,anchor='nw',image=pimg)
window.mainloop()