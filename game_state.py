from board import Board
from pieces import King

class GameState:
    """
    Manages the overall state of the chess game.
    """
    def __init__(self):
        self.board = Board()  # Initialize the board
        self.current_turn = 'w'  # White starts the game
        self.move_log = []  # Log of all moves made
        self.is_check = False
        self.is_checkmate = False
        self.is_stalemate = False

    def make_move(self, start, end):
        """
        Attempts to make a move from `start` to `end`.
        Updates the game state and checks for special conditions like check or checkmate.
        """
        piece = self.board.grid[start[0]][start[1]]

        if piece is None or piece.color != self.current_turn:
            print("Invalid move: No piece to move or wrong turn!")
            return False

        valid_moves = piece.get_valid_moves(self.board)

        if end not in valid_moves:
            print("Invalid move: Move not allowed by piece rules!")
            return False

        # Save the current state for undo functionality
        move_snapshot = (piece, start, end, self.board.grid[end[0]][end[1]], self.board.en_passant_square)
        self.move_log.append(move_snapshot)

        # Move the piece and update the game state
        self.board.move_piece(start, end)

        # Check if the move puts the current player's king in check
        if self.is_king_in_check(self.current_turn):
            # Undo the move if it results in self-check
            self.undo_move()
            print("Invalid move: Cannot leave your king in check!")
            return False

        # Switch turns and update game state
        self.switch_turn()
        self.update_game_state()
        return True

    def undo_move(self):
        """
        Undoes the last move.
        """
        if not self.move_log:
            print("No moves to undo!")
            return

        # Restore the previous state
        last_move = self.move_log.pop()
        piece, start, end, captured_piece, en_passant_state = last_move

        # Restore the board state
        self.board.grid[start[0]][start[1]] = piece
        self.board.grid[end[0]][end[1]] = captured_piece
        piece.position = start
        if captured_piece:
            captured_piece.position = end

        # Restore en passant state
        self.board.en_passant_square = en_passant_state

        # Switch turns back
        self.switch_turn()

    def update_game_state(self):
        """
        Updates the game state after each move.
        """
        self.is_check = self.is_king_in_check(self.current_turn)
        if self.is_check:
            if self.no_valid_moves(self.current_turn):
                self.is_checkmate = True
        else:
            if self.no_valid_moves(self.current_turn):
                self.is_stalemate = True

    def is_king_in_check(self, color):
        """
        Determines if the king of the given color is in check.
        """
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece and piece.color == color and isinstance(piece, King):
                    return self.board.is_square_attacked(row, col, color)
        return False

    def no_valid_moves(self, color):
        """
        Determines if a player has any valid moves remaining.
        """
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece and piece.color == color:
                    valid_moves = piece.get_valid_moves(self.board)
                    # Simulate moves to check if they are valid
                    for move in valid_moves:
                        move_snapshot = (piece, (row, col), move, self.board.grid[move[0]][move[1]], self.board.en_passant_square)
                        self.move_log.append(move_snapshot)
                        self.board.move_piece((row, col), move)
                        if not self.is_king_in_check(color):
                            self.undo_move()
                            return False
                        self.undo_move()
        return True

    def switch_turn(self):
        """
        Switches the turn between white ('w') and black ('b').
        """
        self.current_turn = 'b' if self.current_turn == 'w' else 'w'

    def print_game_status(self):
        """
        Prints the current state of the game (check, checkmate, or stalemate).
        """
        if self.is_checkmate:
            print(f"Checkmate! {self.current_turn} loses.")
        elif self.is_stalemate:
            print("Stalemate!")
        elif self.is_check:
            print(f"{self.current_turn}'s king is in check.")

    def print_move_log(self):
        """
        Prints the move log for debugging or review purposes.
        """
        for i, move in enumerate(self.move_log, start=1):
            piece, start, end, _, _ = move
            print(f"{i}. {piece} moved from {start} to {end}")
