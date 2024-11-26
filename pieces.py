class ChessPiece:
    # Base class for all chess pieces.
    def __init__(self, color, position):
        # 'w' for white, 'b' for black
        self.color = color  
        # (row, col)
        self.position = position  

    def get_valid_moves(self, board):
        # Abstract method to be overridden by subclasses (Polymorphism)
        raise NotImplementedError("This method should be implemented by subclasses")

    def __repr__(self):
        # String representation for debugging.
        return f"{self.color}{self.__class__.__name__[0]}"


class Pawn(ChessPiece):
    def get_valid_moves(self, board):
        moves = []
        # White moves up, Black moves down
        direction = -1 if self.color == 'w' else 1  
        row, col = self.position

        # Move forward
        if board.is_empty(row + direction, col):
            moves.append((row + direction, col))
            # Initial double step
            if (self.color == 'w' and row == 6) or (self.color == 'b' and row == 1):
                if board.is_empty(row + 2 * direction, col):
                    moves.append((row + 2 * direction, col))

        # Captures
        for capture_col in [col - 1, col + 1]:
            if board.is_enemy(row + direction, capture_col, self.color):
                moves.append((row + direction, capture_col))

        # En passant
        if board.en_passant_square:
            if (row + direction, col - 1) == board.en_passant_square or \
               (row + direction, col + 1) == board.en_passant_square:
                moves.append(board.en_passant_square)

        return moves


class Rook(ChessPiece):
    def get_valid_moves(self, board):
        moves = []
        # Vertical and horizontal
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  

        for d in directions:
            for i in range(1, 8):
                new_row = self.position[0] + i * d[0]
                new_col = self.position[1] + i * d[1]

                if board.is_on_board(new_row, new_col):
                    if board.is_empty(new_row, new_col):
                        moves.append((new_row, new_col))
                    elif board.is_enemy(new_row, new_col, self.color):
                        moves.append((new_row, new_col))
                        break
                    else:
                        break
                else:
                    break

        return moves


class Knight(ChessPiece):
    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        knight_moves = [
            (row + 2, col + 1), (row + 2, col - 1),
            (row - 2, col + 1), (row - 2, col - 1),
            (row + 1, col + 2), (row + 1, col - 2),
            (row - 1, col + 2), (row - 1, col - 2)
        ]

        for r, c in knight_moves:
            if board.is_on_board(r, c) and (board.is_empty(r, c) or board.is_enemy(r, c, self.color)):
                moves.append((r, c))

        return moves


class Bishop(ChessPiece):
    def get_valid_moves(self, board):
        moves = []
        directions = [(1, 1), (-1, -1), (1, -1), (-1, 1)]  # Diagonal moves

        for d in directions:
            for i in range(1, 8):
                new_row = self.position[0] + i * d[0]
                new_col = self.position[1] + i * d[1]

                if board.is_on_board(new_row, new_col):
                    if board.is_empty(new_row, new_col):
                        moves.append((new_row, new_col))
                    elif board.is_enemy(new_row, new_col, self.color):
                        moves.append((new_row, new_col))
                        break
                    else:
                        break
                else:
                    break

        return moves


class Queen(ChessPiece):
    def get_valid_moves(self, board):
        moves = []

        # Combine rook and bishop movement
        rook_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        bishop_directions = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
        all_directions = rook_directions + bishop_directions

        for d in all_directions:
            for i in range(1, 8):
                new_row = self.position[0] + i * d[0]
                new_col = self.position[1] + i * d[1]

                if board.is_on_board(new_row, new_col):
                    if board.is_empty(new_row, new_col):
                        moves.append((new_row, new_col))
                    elif board.is_enemy(new_row, new_col, self.color):
                        moves.append((new_row, new_col))
                        break
                    else:
                        break
                else:
                    break

        return moves


class King(ChessPiece):
    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (-1, -1), (1, -1), (-1, 1)
        ]

        for d in directions:
            new_row = row + d[0]
            new_col = col + d[1]

            if board.is_on_board(new_row, new_col):
                if board.is_empty(new_row, new_col) or board.is_enemy(new_row, new_col, self.color):
                    if not board.is_square_attacked(new_row, new_col, self.color):  # Avoid moving into check
                        moves.append((new_row, new_col))

        # Castling (to be implemented based on game state)
        if board.can_castle_kingside(self.color):
            moves.append((row, col + 2))
        if board.can_castle_queenside(self.color):
            moves.append((row, col - 2))

        return moves
