import sunfish,threading,chess,chess.svg,random,np,variables,time
from time import sleep
from tkinter import *
from tk import *
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from PIL import ImageTk, Image, PngImagePlugin


########################################################################
# Global variables
board_coord = [["A8","B8","C8","D8","E8","F8","G8","H8"],
               ["A7","B7","C7","D7","E7","F7","G7","H7"],
               ["A6","B6","C6","D6","E6","F6","G6","H6"],
               ["A5","B5","C5","D5","E5","F5","G5","H5"],
               ["A4","B4","C4","D4","E4","F4","G4","H4"],
               ["A3","B3","C3","D3","E3","F3","G3","H3"],
               ["A2","B2","C2","D2","E2","F2","G2","H2"],
               ["A1","B1","C1","D1","E1","F1","G1","H1"]]
my_board = [["R2","N1","B1","Q2","K2","B3","N3","R2"],
            ["P1","P1","P1","P2","P2","P3","P3","P3"],
            [". ",". ",". ",". ",". ",". ",". ",". "],
            [". ",". ",". ",". ",". ",". ",". ",". "],
            [". ",". ",". ",". ",". ",". ",". ",". "],
            [". ",". ",". ",". ",". ",". ",". ",". "],
            ["p1","p1","p1","p2","p2","p3","p3","p3"],
            ["r2","n1","b1","q2","k2","b3","n3","r2"]]

# keep track of current piece and where it will move/attack
cur_piece = ""  # UCI coordinates
cp_x = 0
cp_y = 0
cp = ""         # piece name, e.g. pb (pawn-black)
move_to = ""    # second verse, same as the first
mt_x = 0
mt_y = 0
mt = ""

# for graveyard, how many of each have died
pw = 0
rw = 0
nw = 0
bw = 0
pb = 0
rb = 0
nb = 0
bb = 0

# for 3 move counter
move_counter = 0
my_moves = 0

# corps commanders dead
commander_1 = True
commander_2 = True

ez_mode = False
ez = ""

board = ""
panel = ""
window = ""
die = ""
die_number = ""
die_img = ""
black_labels = ""
black_pics = ""
black_list = ""
white_labels = ""
white_pics = ""
white_list = ""

last_move = ""


########################################################################
def is_capture() :
    global cp,mt
    print("cur_piece = ",cp)
    print("move_to = ",mt,"\n")
    cp_tmp = cp
    cp = cp[0:1]
    mt_tmp = mt
    mt = mt[0:1]

    if (cp == '.' and mt != '.') :
        tmp = cp
        cp = mt
        mt = tmp

    if (str(mt) != '.') :
        die = roll_die()
        print("Die result = ",die,"\n")

        if (str(cp.lower()) == "p") :
            if (mt.lower() == "p") :
                if (die >= 4) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            elif (mt.lower() == "r") :
                if (die >= 6) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            elif (mt.lower() == "b") :
                if (die >= 5) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            elif (mt.lower() == "n") :
                if (die >= 6) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            elif (mt.lower() == "q") :
                if (die >= 6) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            elif (mt.lower() == "k") :
                if (die >= 6) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            else :
                print("!!!!!!!!!!!!!!!!!\nERROR in is_capture()\ncp = ",cp,"\nmt = ",mt,"\n!!!!!!!!!!!!!!!!!")
                return False

        elif (cp.lower() == "r") :
            if (mt.lower() == "p") :
                if (die >= 5) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            elif (mt.lower() == "r") :
                if (die >= 6) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            elif (mt.lower() == "b") :
                if (die >= 5) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            elif (mt.lower() == "n") :
                if (die >= 5) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            elif (mt.lower() == "q") :
                if (die >= 4) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            elif (mt.lower() == "k") :
                if (die >= 4) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            else :
                print("!!!!!!!!!!!!!!!!!\nERROR in is_capture()\ncp = ",cp,"\nmt = ",mt,"\n!!!!!!!!!!!!!!!!!")
                return False

        elif (cp.lower() == "b") :
            if (mt.lower() == "p") :
                if (die >= 3) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            elif (mt.lower() == "r") :
                if (die >= 5) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            elif (mt.lower() == "b") :
                if (die >= 4) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            elif (mt.lower() == "n") :
                if (die >= 5) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            elif (mt.lower() == "q") :
                if (die >= 5) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            elif (mt.lower() == "k") :
                if (die >= 5) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            else :
                print("!!!!!!!!!!!!!!!!!\nERROR in is_capture()\ncp = ",cp,"\nmt = ",mt,"\n!!!!!!!!!!!!!!!!!")
                return False

        elif (cp.lower() == "n") :
            if (mt.lower() == "p") :
                if (die >= 2) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            elif (mt.lower() == "r") :
                if (die >= 5) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            elif (mt.lower() == "b") :
                if (die >= 4) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            elif (mt.lower() == "n") :
                if (die >= 4) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            elif (mt.lower() == "q") :
                if (die >= 6) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            elif (mt.lower() == "k") :
                if (die >= 6) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            else :
                print("!!!!!!!!!!!!!!!!!\nERROR in is_capture()\ncp = ",cp,"\nmt = ",mt,"\n!!!!!!!!!!!!!!!!!")
                return False
                
        elif (cp.lower() == "q") :
            if (mt.lower() == "p") :
                if (die >= 2) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            elif (mt.lower() == "r") :
                if (die >= 5) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            elif (mt.lower() == "b") :
                if (die >= 4) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            elif (mt.lower() == "n") :
                if (die >= 4) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            elif (mt.lower() == "q") :
                if (die >= 4) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            elif (mt.lower() == "k") :
                if (die >= 4) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            else :
                print("!!!!!!!!!!!!!!!!!\nERROR in is_capture()\ncp = ",cp,"\nmt = ",mt,"\n!!!!!!!!!!!!!!!!!")
                return False
                
        elif (cp.lower() == "k") :
            if (mt.lower() == "p") :
                if (die >= 0) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            elif (mt.lower() == "r") :
                if (die >= 5) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            elif (mt.lower() == "b") :
                if (die >= 4) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            elif (mt.lower() == "n") :
                if (die >= 4) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            elif (mt.lower() == "q") :
                if (die >= 4) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            elif (mt.lower() == "k") :
                if (die >= 4) :
                    graveyard(mt,cp_tmp,mt_tmp)
                    return True
                else :
                    return False
            else :
                print("!!!!!!!!!!!!!!!!!\nERROR in is_capture()\ncp = ",cp,"\nmt = ",mt,"\n!!!!!!!!!!!!!!!!!")
                return False

        else :
            print("!!!!!!!!!!!!!!!!!\nERROR in is_capture()\ncp = ",cp,"\nmt = ",mt,"\n!!!!!!!!!!!!!!!!!")
            return False
    else :
        return True


########################################################################
def graveyard(piece,cp_tmp,mt_tmp) :
    global pw,rw,nw,bw,pb,rb,nb,bb,black_list,black_labels,white_list,white_labels,cp,mt
    print(piece,"captured")     #\n","cp_tmp =",cp_tmp)
    if (piece.islower()) :
        piece += "w"
    else :
        piece += "b"
    piece = piece.lower()

    if (piece == "pw") :
        pw += 1
        piece += str(pw)
    if (piece == "rw") :
        rw += 1
        piece += str(rw)
    if (piece == "nw") :
        nw += 1
        piece += str(nw)
    if (piece == "bw") :
        bw += 1
        piece += str(bw)

    if (piece == "pb") :
        pb += 1
        piece += str(pb)
    if (piece == "rb") :
        rb += 1
        piece += str(rb)
    if (piece == "nb") :
        nb += 1
        piece += str(nb)
    if (piece == "bb") :
        bb += 1
        piece += str(bb)

    #print("!!!!!!!!!!!!!!!!!\nSearching list for %s\n!!!!!!!!!!!!!!!!!" % piece)

    arr_x = 0
    arr_y = 0
    black = False
    white = False
    for y in range (0,2) :
        for x in range (0,8) :
            if (white_list[y][x] == piece) :
                arr_x = x
                arr_y = y
                white = True
                #print("!!!!!!!!!!!!!!!!!\nFOUND white\n!!!!!!!!!!!!!!!!!")
                break
            elif (black_list[y][x] == piece) :
                arr_x = x
                arr_y = y
                black = True
                #print("!!!!!!!!!!!!!!!!!\nFOUND black\n!!!!!!!!!!!!!!!!!")
                break
    if (white) : 
        white_labels[arr_y][arr_x].config(height=0,width=0,image=white_pics[arr_y][arr_x])
    elif (black) : 
        black_labels[arr_y][arr_x].config(height=0,width=0,image=black_pics[arr_y][arr_x])
    
    cp = cp_tmp
    mt = mt_tmp

    return True


########################################################################
def roll_die() :
    global die_number,die_img,ez_mode
    roll_list = []
    rand_num = ""
    for i in range (0,6) :
        rand_num = random.randint(1,6)
        img = Image.open("{}.png".format(rand_num))
        die_img = ImageTk.PhotoImage(img)
        die.config(image=die_img)
        die.update()
        sleep(.2)
    img = Image.open("{}.png".format(rand_num))
    die_img = ImageTk.PhotoImage(img)
    die.config(image=die_img)
    die.update()
    if not ez_mode :
        return rand_num
    else :
        return 6


########################################################################
def draw_board(squares) :
    f = open ("tmp.svg","w")
    f.write(chess.svg.board(board,squares=squares,size=800))
    f.close	
    get_svg("tmp.svg")
    img = Image.open("tmp.png")
    cur_board_img = ImageTk.PhotoImage(img)
    panel.config(image=cur_board_img)
    panel.image=cur_board_img


########################################################################
def change_board() :
    global my_board,cp,cp_y,cp_x,mt_y,mt_x,my_moves
    my_board[cp_y][cp_x] = ". "
    if (len(cp) == 1) :
        my_board[mt_y][mt_x] = str(cp+str(my_moves+1))
    else :
        my_board[mt_y][mt_x] = str(cp[0:2]+" ")


########################################################################
def print_board() :
    global my_board
    for y in range(8) :
        for x in range(8) :
            print(my_board[y][x]," ",end="")
        print()
    print("\n----------------------------------------\n")


########################################################################
def skip_turn() :
    global my_moves
    board.push(chess.Move.null())
    variables.user_skip = True
    my_moves += 1

    if (my_moves < 3) :
            board.push(chess.Move.null())
            variables.ai_skip = True
    else :
        for i in range (0,3) :
            e.set()
            variables.ai_skip = False
            AI()
            window.update()
            if (i < 2) :
                board.push(chess.Move.null())
        my_moves = 0
        
    e.set()


########################################################################
def cheats() :
    global ez_mode
    if not ez_mode :
        ez_mode = True
        ez.config(bg="green")
    else :
        ez_mode = False
        ez.config(bg="white")


########################################################################
def get_svg(svg_file) :
	drawing = svg2rlg(svg_file)
	renderPM.drawToFile(drawing,"tmp.png",fmt="PNG")


########################################################################
def corps() :
    global my_moves,cp
    if (my_moves > 3) :
        my_moves = 0
    #print("cp[1:2] =",cp[1:2],"\nmy_moves =",my_moves+1)
    if (int(cp[1:2]) == int(my_moves+1)) :
        print ("Correct corp selected")
        return True
    else :
        print("Incorrect corp selected")
        return False


########################################################################
def AI() :
    global cur_piece,move_to,move_counter,cp,cp_x,cp_y,mt,mt_x,mt_y

    e.set()
    while (variables.ai_move == variables.last_ai) : # or (variables.ai_move == "wait") :
        time.sleep(.05)
    variables.last_ai = variables.ai_move

    #print("finding locations for AI move : ",variables.last_ai)
    cp = variables.last_ai[0:2].upper()         # set cp, cp_x, cp_y, mt, mt_x, mt_y for local board + graveyard
    #print("cp location = ",cp)

    for y in range (0,8) :
        for x in range (0,8) :
            if (cp == board_coord[y][x]) :
                cp = my_board[y][x]
                cp_y = y
                cp_x = x
                #print("cp =",cp,"\ncp_y =",cp_y,"\ncp_x =",cp_x)
                break

    mt = variables.last_ai[2:4].upper()
    print("mt location = ",mt)

    for y in range (0,8) :
        for x in range (0,8) :
            if (mt == board_coord[y][x]) :
                mt = my_board[y][x]
                mt_y = y
                mt_x = x
                #print("mt =",mt,"\nmt_y =",mt_y,"\nmt_x =",mt_x)
                break

    if (is_capture()) :
        print("AI captured ",mt)
        change_board()
        print_board()
        board.push(move=chess.Move.from_uci(variables.ai_move.lower()))
        draw_board("")
    else :
        board.push(chess.Move.null())
        variables.game_over = False
        variables.revert_board = True
        # need to revert sunfish board to previous state 


########################################################################
def select_piece(event) :               # shows available attacks/moves, pawns only show attacks
    global cur_piece,move_to,cp_x,cp_y,cp
    x_coord = event.x
    y_coord = event.y
    x_coord -= 31
    y_coord -= 31
    x = x_coord / 92
    y = y_coord / 92
    cp_x = int(x)
    cp_y = int(y)
    cp = my_board[cp_y][cp_x]
    cur_piece = board_coord[cp_y][cp_x]
    if corps():
        squares = board.attacks(getattr(chess,cur_piece))
    else :
        squares = ""
    draw_board(squares)


########################################################################
def move_piece(event) :
    global cur_piece,move_to,move_counter,my_moves,mt_x,mt_y,mt,ez_mode
    x_coord = event.x
    y_coord = event.y
    x_coord -= 31
    y_coord -= 31
    x = x_coord / 92
    y = y_coord / 92
    mt_x = int(x)
    mt_y = int(y)
    mt = my_board[mt_y][mt_x]
    move_to = board_coord[int(y)][int(x)]
    squares = ""
    variables.move_uci = cur_piece + move_to
    my_move = chess.Move.from_uci(variables.move_uci.lower())

    if (((my_move in board.legal_moves) and (corps())) or (ez_mode)) : 

        if (is_capture()) :
            #print(mt," captured")
            change_board()
            print ("variables.move_uci = ",variables.move_uci)
            board.push(move=my_move)
            draw_board(squares)
            window.update()
            print_board()
        else :
            variables.user_skip = True
            board.push(chess.Move.null())
            draw_board(squares)
            window.update()
            print_board()

        e.set()
        time.sleep(.1)
        my_moves += 1


        print("my_moves # = ",my_moves)
        if (my_moves <= 3) :
            board.push(chess.Move.null())
            variables.ai_skip = True
            e.set()
            print("game_over =",variables.game_over)
            if (variables.game_over == True) :
                img = Image.open("game_over.png")
                cur_board_img = ImageTk.PhotoImage(img)
                panel.config(image=cur_board_img)
                panel.image=cur_board_img
        if (my_moves >=3) :
            board.push(chess.Move.null())
            time.sleep(.1)
            for i in range (0,3) :
                tmp = variables.ai_move
                #e.set()
                while (variables.ai_move == tmp) :
                    variables.ai_skip = False
                    variables.user_skip = True
                    e.set()
                variables.ai_skip = True
                variables.user_skip = True
                e.clear()
                AI()
                window.update()
                if (i < 2) :
                    board.push(chess.Move.null())
                print("game_over =",variables.game_over)
                if (variables.game_over == True) :
                    img = Image.open("game_over.png").resize((750,400))
                    cur_board_img = ImageTk.PhotoImage(img)
                    panel.config(image=cur_board_img)
                    panel.image=cur_board_img
                    window.update()
            my_moves = 0
        
        e.set()

    else :
        print("!!!!!!!!!!!!!!!!!\nILLEGAL MOVE\n!!!!!!!!!!!!!!!!!")


########################################################################
def please_work(e,useless_number) :
    global board,panel,window,die,ez,black_labels,black_pics,black_list,white_labels,white_pics,white_list

    window = Tk()
    window.title("AI Chess Variant")
    window.geometry("1240x880")
    window.config(bg="white")

    board = chess.Board(chess.STARTING_BOARD_FEN)

    die_number = StringVar()
    die_number.set("")

    lh = 4
    lw = 10

    black_labels =   [["pb1","pb2","pb3","pb4","pb5","pb6","pb7","pb8"],    # Converts to an array of Labels 
                      ["rb1","nb1","bb1", "qb", "kb","bb2","nb2","rb2"]]
    black_pics =     [["pb1","pb2","pb3","pb4","pb5","pb6","pb7","pb8"],    # Converts to an array of Pictures
                      ["rb1","nb1","bb1", "qb", "kb","bb2","nb2","rb2"]]
    black_list =     [["pb1","pb2","pb3","pb4","pb5","pb6","pb7","pb8"],    # Array to find location in Labels
                      ["rb1","nb1","bb1", "qb", "kb","bb2","nb2","rb2"]]
    for y in range(0,2) : 
        for x in range (0,8) :
            name = black_labels[y][x]
            img = Image.open("{}.png".format(name[0:2]))
            black_pics[y][x] = ImageTk.PhotoImage(img)
            black_labels[y][x] = Label(window,height=lh,width=lw,bg="light grey")
            black_labels[y][x].grid(row=x,column=int((y+1)%2),padx=15,pady=15)

    f = open ("tmp.svg","w")
    f.write(chess.svg.board(board,size=800))
    f.close	
    get_svg("tmp.svg")
    img = Image.open("tmp.png")
    cur_board_img = ImageTk.PhotoImage(img)
    panel = Label(window,image=cur_board_img)
    panel.bind("<Button-1>",select_piece)
    panel.bind("<Button-3>",move_piece)
    panel.grid(row=0,column=2,rowspan=10)

    white_labels =  [["pw1","pw2","pw3","pw4","pw5","pw6","pw7","pw8"],
                     ["rw1","nw1","bw1", "qw", "kw","bw2","nw2","rw2"]]
    white_pics =    [["pw1","pw2","pw3","pw4","pw5","pw6","pw7","pw8"],
                     ["rw1","nw1","bw1", "qw", "kw","bw2","nw2","rw2"]]
    white_list =    [["pw1","pw2","pw3","pw4","pw5","pw6","pw7","pw8"],
                     ["rw1","nw1","bw1", "qw", "kw","bw2","nw2","rw2"]]
    for y in range(0,2) : 
        for x in range (0,8) :
            name = white_labels[y][x]
            img = Image.open("{}.png".format(name[0:2]))
            white_pics[y][x] = ImageTk.PhotoImage(img)
            white_labels[y][x] = Label(window,height=lh,width=lw,bg="light grey")
            white_labels[y][x].grid(row=x,column=y+3,padx=15,pady=15)

    die = Label(window,image="",bg="white")
    die.grid(row=10,column=2,pady=5)
    skip = Button(window,text="SKIP TURN",command=skip_turn,bg="white")
    skip.grid(row=10,column=4)

    ez = Button(window,text="EZ",command=cheats)       # disables legal moves check, debugging
    ez.grid(row=10,column=0)

    window.mainloop()


########################################################################
if __name__ == "__main__":
    e = threading.Event()
    t1 = threading.Thread(name="sunfish",target=sunfish.main,args=(e,1))
    t1.start()
    t2 = threading.Thread(name="GUI",target=please_work,args=(e,1))
    t2.start()
    t1.join()
    t2.join()