import pygame as pg
from engine import *
import time

SCREEN_SIZE = 600

x = 100
y = 50
s = SCREEN_SIZE - 2*x

pg.init()
scr = pg.display.set_mode((SCREEN_SIZE,SCREEN_SIZE))
pg.display.set_caption('Quarto')
done = False
clock = pg.time.Clock()

font = pg.font.SysFont(None,24)
larr = font.render("<<", True, (255,255,255))
rarr = font.render(">>", True, (255,255,255))
which_piece = font.render("Which piece to give your opponent?", True, (0,0,0))

game = Game(HumanPlayer(), HumanPlayer())

def draw_piece(x,y,id,zoom=False):
    if id == -1:
        return

    r = s/10
    c = (0,0,0)

    if id & 8 > 0:
        r = s/6
    if id & 4 > 0:
        c = (255,255,255)
    hole = id & 2 > 0
    circ = id & 1 > 0

    if zoom:
        r *= 1.1

    if circ:
        pg.draw.circle(scr, c, (x, y), r/2)
    else:
        pg.draw.rect(scr, c, pg.Rect(x - r/2, y - r/2, r, r))

    if hole:
        pg.draw.circle(scr, (127,127,127), (x, y), r/4)

def draw_board():
    pg.draw.rect(scr, (204,153,0), pg.Rect(x,y,s,s))
    for x_ in range(x, x + s + 1, int(s/4)):
        pg.draw.line(scr, (128,96,0), (x_, y), (x_, y + s), 2)

    for y_ in range(y, y + s + 1, int(s/4)):
        pg.draw.line(scr, (128,96,0), (x, y_), (x + s, y_), 2)

    b = game.board.b

    for i in range(4):
        for j in range(4):
            draw_piece(x + i * s/4 + s/8,y + j* s/4 + s/8, b[i,j])

pc_show = [0,7]

def show_remaining_pieces():
    pg.draw.rect(scr, (127,127,127), pg.Rect(0, SCREEN_SIZE - 100, SCREEN_SIZE, 100))
    k = 0
    for i in range(pc_show[0], min(pc_show[1], len(game.remaining_pieces))):
        (x,y) = pg.mouse.get_pos()
        focused = False#(x > k * s/4 + s/16) and (x < (k+1) * s/4 - s/16) and (y > SCREEN_SIZE - 100)

        draw_piece(k * s/4 + s/8, SCREEN_SIZE - 50, game.remaining_pieces[i], focused)
        k += 1

    scr.blit(which_piece, (SCREEN_SIZE/2 - which_piece.get_rect().width/2,SCREEN_SIZE-124))

def show_piece_buttons():
    lactive = False
    ractive = False
    if pc_show[0] > 0:
        scr.blit(larr, (0, SCREEN_SIZE-100))
        lactive = True

    if pc_show[1] < len(game.remaining_pieces):
        scr.blit(rarr, (SCREEN_SIZE-30, SCREEN_SIZE-100))
        ractive = True

    (x,y) = pg.mouse.get_pos()

    for e in pg.event.get():
        left, _, __ = pg.mouse.get_pressed()

        if left and e.type == pg.MOUSEBUTTONDOWN:
            if x < 48 and lactive:
                pc_show[0] = max(pc_show[0]-6,0)
                pc_show[1] = pc_show[0] + 6
            if x > SCREEN_SIZE - 48 and ractive:
                pc_show[0] += 6
                pc_show[1] += 6

while not done:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            done = True
        if e.type == pg.KEYDOWN:
            game.pass_keypress(e.key)
        """if len(game.board.open_squares) > 0: # TODO: Make turn based, make it wait for the turn

            ### Giving piece to other player ###

            cur = game.players[game.current_p]
            piece = -1

            if type(cur) == HumanPlayer:
                chosen = 6

                if e.type == pg.KEYDOWN:
                    if e.key == pg.K_1:
                        chosen = 0
                    elif e.key == pg.K_2:
                        chosen = 1
                    elif e.key == pg.K_3:
                        chosen = 2
                    elif e.key == pg.K_4:
                        chosen = 3
                    elif e.key == pg.K_5:
                        chosen = 4
                    elif e.key == pg.K_6:
                        chosen = 5
                    if chosen < pc_show[1] - pc_show[0] - 1 and chosen < len(game.remaining_pieces): # TODO Put together game loop in engine, link back here
                        piece = game.remaining_piece[pc_show[0] + chosen]
            elif type(cur) == AIPlayer:
                piece = cur.mdp.choice_function(game.board, game.remaining_pieces)

            #game.remove_piece(piece)

            ### Playing the chosen piece ###

            coord = (-1,-1)"""
    # How to get the GUI to handle the display while engine handles game operation, but interacts with GUI input?

    ### PIECE CHOICE PHASE, executed by current_p

    ### PIECE PLACE PHASES, executed by !current_p

    scr.fill((255,255,255))
    draw_board()

    show_remaining_pieces()
    show_piece_buttons()

    pg.display.update()
    clock.tick(30)