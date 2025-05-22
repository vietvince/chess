import pygame as p
from game_state import GameState
from ai import find_best_move

# Pygame setup
WIDTH, HEIGHT = 512, 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
FPS = 15
IMAGES = {}

# Load images once
def load_images():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK',
              'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

# Draw board squares
def draw_board(screen):
    colors = [p.Color("light gray"), p.Color("dark green")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row + col) % 2]
            p.draw.rect(screen, color, p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Draw pieces on board
def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board.grid[row][col]
            if piece is not None:
                name = piece.color + piece.__class__.__name__[0]
                screen.blit(IMAGES[name], p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_game_state(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = GameState()
    load_images()
    running = True
    sq_selected = ()
    player_clicks = []
    player_color = 'w'  # 'w' for white, 'b' for black

    while running:
        human_turn = gs.current_turn == player_color

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN and human_turn:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sq_selected == (row, col):
                    sq_selected = ()
                    player_clicks = []
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)
                if len(player_clicks) == 2:
                    moved = gs.make_move(player_clicks[0], player_clicks[1])
                    sq_selected = ()
                    player_clicks = []

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undo_move()

        if not human_turn:
            ai_move = find_best_move(gs)
            if ai_move:
                gs.make_move(ai_move[0], ai_move[1])

        draw_game_state(screen, gs)

        if gs.is_checkmate:
            print("Checkmate!")
        elif gs.is_stalemate:
            print("Stalemate!")

        clock.tick(FPS)
        p.display.flip()

if __name__ == "__main__":
    main()
