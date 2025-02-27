import random
from game_state import GameState
from board import Board
from pieces import ChessPiece, Pawn, Rook, Knight, Bishop, Queen, King

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3  # AI search depth (adjustable)

piece_values = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}

def evaluate_board(board: Board, ai_color: str):
    """
    Evaluates the board position for AI.
    Positive values favor AI, negative values favor opponent.
    """
    score = 0
    for row in range(8):
        for col in range(8):
            piece = board.grid[row][col]
            if piece:
                value = piece_values[piece.__class__.__name__[0]]
                score += value if piece.color == ai_color else -value
    return score

def find_best_move(game_state: GameState, depth=DEPTH):
    """ Finds the best move for AI using Minimax with Alpha-Beta Pruning. """
    best_move = None
    max_score = -CHECKMATE
    
    valid_moves = get_all_moves(game_state)
    random.shuffle(valid_moves)  # Add randomness for variety
    
    for move in valid_moves:
        game_state.make_move(move[0], move[1])
        score = minimax(game_state, depth - 1, -CHECKMATE, CHECKMATE, False)
        game_state.undo_move()
        
        if score > max_score:
            max_score = score
            best_move = move
    
    return best_move

def minimax(game_state: GameState, depth, alpha, beta, maximizing_player):
    """ Minimax algorithm with Alpha-Beta pruning for AI decision making. """
    if depth == 0 or game_state.is_checkmate or game_state.is_stalemate:
        return evaluate_board(game_state.board, game_state.current_turn)
    
    valid_moves = get_all_moves(game_state)
    if maximizing_player:
        max_score = -CHECKMATE
        for move in valid_moves:
            game_state.make_move(move[0], move[1])
            score = minimax(game_state, depth - 1, alpha, beta, False)
            game_state.undo_move()
            max_score = max(max_score, score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break  # Beta cut-off
        return max_score
    else:
        min_score = CHECKMATE
        for move in valid_moves:
            game_state.make_move(move[0], move[1])
            score = minimax(game_state, depth - 1, alpha, beta, True)
            game_state.undo_move()
            min_score = min(min_score, score)
            beta = min(beta, score)
            if beta <= alpha:
                break  # Alpha cut-off
        return min_score

def get_all_moves(game_state: GameState):
    """ Generates all legal moves for the current player. """
    moves = []
    for row in range(8):
        for col in range(8):
            piece = game_state.board.grid[row][col]
            if piece and piece.color == game_state.current_turn:
                for move in piece.get_valid_moves(game_state.board):
                    moves.append(((row, col), move))
    return moves
