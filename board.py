from pieces import ChessPiece, Pawn, Rook, Knight, Bishop, Queen, King

class Board:
    # Represents the chessboard and manages piece placement, movement, and utility methods.
    def __init__(self):
        # 8x8 board initialized with None (empty squares)
        self.grid = [[None for _ in range(8)] for _ in range(8)]

        # Tracks the en passant square (if applicable)
        self.en_passant_square = None

        # Initialize pieces on the board
        self.initialize_pieces()

    def initialize_pieces(self):
        # Sets up the board with the initial piece placement for a standard chess game.
        # Place pawns
        for col in range(8):
            self.grid[1][col] = Pawn('b', (1, col))
            self.grid[6][col] = Pawn('w', (6, col))

        # Place rooks
        self.grid[0][0] = Rook('b', (0, 0))
        self.grid[0][7] = Rook('b', (0, 7))
        self.grid[7][0] = Rook('w', (7, 0))
        self.grid[7][7] = Rook('w', (7, 7))

        # Place knights
        self.grid[0][1] = Knight('b', (0, 1))
        self.grid[0][6] = Knight('b', (0, 6))
        self.grid[7][1] = Knight('w', (7, 1))
        self.grid[7][6] = Knight('w', (7, 6))

        # Place bishops
        self.grid[0][2] = Bishop('b', (0, 2))
        self.grid[0][5] = Bishop('b', (0, 5))
        self.grid[7][2] = Bishop('w', (7, 2))
        self.grid[7][5] = Bishop('w', (7, 5))

        # Place queens
        self.grid[0][3] = Queen('b', (0, 3))
        self.grid[7][3] = Queen('w', (7, 3))

        # Place kings
        self.grid[0][4] = King('b', (0, 4))
        self.grid[7][4] = King('w', (7, 4))

    def is_on_board(self, row, col):
        # Checks if the given position is within board boundaries.
        return 0 <= row < 8 and 0 <= col < 8

    def is_empty(self, row, col):
        # Checks if the given square is empty.
        return self.is_on_board(row, col) and self.grid[row][col] is None

    def is_enemy(self, row, col, color):
        # Checks if the piece on the given square is an enemy piece.
        if not self.is_on_board(row, col):
            return False
        piece = self.grid[row][col]
        return piece is not None and piece.color != color

    def move_piece(self, start, end):
        # Moves a piece from the start position to the end position.
        # Handles captures, updates positions, and resets en passant.
        piece = self.grid[start[0]][start[1]]
        target = self.grid[end[0]][end[1]]

        # Update the grid
        self.grid[start[0]][start[1]] = None
        self.grid[end[0]][end[1]] = piece

        # Update the piece's position
        piece.position = (end[0], end[1])

        # Handle en passant
        if isinstance(piece, Pawn) and abs(start[0] - end[0]) == 2:
            self.en_passant_square = (end[0] + (1 if piece.color == 'b' else -1), end[1])
        else:
            self.en_passant_square = None

        # Handle captures
        if target is not None:
            self.capture_piece(target)

    def capture_piece(self, piece):
        # Handles capturing a piece (removing it from the board).
        print(f"{piece} captured!")

    def can_castle_kingside(self, color):
        # Checks if kingside castling is possible for the given color.
        if color == 'w':
            return isinstance(self.grid[7][4], King) and isinstance(self.grid[7][7], Rook)
        elif color == 'b':
            return isinstance(self.grid[0][4], King) and isinstance(self.grid[0][7], Rook)
        return False

    def can_castle_queenside(self, color):
        # Checks if queenside castling is possible for the given color.
        if color == 'w':
            return isinstance(self.grid[7][4], King) and isinstance(self.grid[7][0], Rook)
        elif color == 'b':
            return isinstance(self.grid[0][4], King) and isinstance(self.grid[0][0], Rook)
        return False

    def is_square_attacked(self, row, col, color):
        # Determines if a square is attacked by an enemy piece.
        for r in range(8):
            for c in range(8):
                piece = self.grid[r][c]
                if piece is not None and piece.color != color:
                    if (row, col) in piece.get_valid_moves(self):
                        return True
        return False

    def print_board(self):
        # Prints the board to the console for debugging.
        for row in self.grid:
            print(" ".join([str(piece) if piece else '--' for piece in row]))
