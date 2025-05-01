#Piece Movement Functions
def in_bounds(r, c):
    return 0 <= r < 8 and 0 <= c < 8

def enemy(piece, target):
    return target != ' ' and piece.isupper() != target.isupper()

def pawn_moves(board, r, c):
    moves = []
    direction = -1 if board[r][c].isupper() else 1  
    start_row = 6 if board[r][c].isupper() else 1

    if in_bounds(r + direction, c) and board[r + direction][c] == ' ':
        moves.append((r + direction, c))
        if r == start_row and board[r + 2 * direction][c] == ' ':
            moves.append((r + 2 * direction, c))

    for dc in [-1, 1]:
        nr, nc = r + direction, c + dc
        if in_bounds(nr, nc) and enemy(board[r][c], board[nr][nc]):
            moves.append((nr, nc))

    return moves

def rook_moves(board, r, c):
    moves = []
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        while in_bounds(nr, nc):
            if board[nr][nc] == ' ':
                moves.append((nr, nc))
            elif enemy(board[r][c], board[nr][nc]):
                moves.append((nr, nc))
                break
            else:
                break
            nr += dr
            nc += dc
    return moves

def bishop_moves(board, r, c):
    moves = []
    directions = [(-1,-1), (-1,1), (1,-1), (1,1)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        while in_bounds(nr, nc):
            if board[nr][nc] == ' ':
                moves.append((nr, nc))
            elif enemy(board[r][c], board[nr][nc]):
                moves.append((nr, nc))
                break
            else:
                break
            nr += dr
            nc += dc
    return moves

def queen_moves(board, r, c):
    return rook_moves(board, r, c) + bishop_moves(board, r, c)

def knight_moves(board, r, c):
    moves = []
    jumps = [(-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1)]
    for dr, dc in jumps:
        nr, nc = r + dr, c + dc
        if in_bounds(nr, nc):
            if board[nr][nc] == ' ' or enemy(board[r][c], board[nr][nc]):
                moves.append((nr, nc))
    return moves

def king_moves(board, r, c):
    moves = []
    directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if in_bounds(nr, nc):
            if board[nr][nc] == ' ' or enemy(board[r][c], board[nr][nc]):
                moves.append((nr, nc))
    return moves

# Movement Dictionary
piece_movement_dictionary = {
    'P': pawn_moves, 'p': pawn_moves,
    'R': rook_moves, 'r': rook_moves,
    'N': knight_moves, 'n': knight_moves,
    'B': bishop_moves, 'b': bishop_moves,
    'Q': queen_moves, 'q': queen_moves,
    'K': king_moves, 'k': king_moves,
}

# Board
def create_initial_board():
    return [
        ['r','n','b','q','k','b','n','r'],
        ['p','p','p','p','p','p','p','p'],
        [' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' '],
        ['P','P','P','P','P','P','P','P'],
        ['R','N','B','Q','K','B','N','R'],
    ]

#Display Board 
def print_board(board):
    print("  a b c d e f g h")
    for i, row in enumerate(board):
        print(f"{8 - i} " + ' '.join(row))
    print()

# --- Coordinate Conversion ---
def parse_position(pos_str):
    col = ord(pos_str[0]) - ord('a')
    row = 8 - int(pos_str[1])
    return row, col

def is_white(piece):
    return piece.isupper()

def is_black(piece):
    return piece.islower()

def move_piece(board, r1, c1, r2, c2):
    piece = board[r1][c1]
    board[r2][c2] = piece
    board[r1][c1] = ' '

    # Promotion
    if piece == 'P' and r2 == 0:
        promote = input("Promote pawn to (Q/R/B/N): ").strip().upper()
        board[r2][c2] = promote if promote in 'QRBN' else 'Q'
    elif piece == 'p' and r2 == 7:
        promote = input("Promote pawn to (q/r/b/n): ").strip().lower()
        board[r2][c2] = promote if promote in 'qrbn' else 'q'

def get_valid_moves(board, r, c):
    piece = board[r][c]
    move_func = piece_move_funcs.get(piece)
    return move_func(board, r, c) if move_func else []

#Check 
def find_king(board, white):
    target = 'K' if white else 'k'
    for r in range(8):
        for c in range(8):
            if board[r][c] == target:
                return r, c
    return None

def is_in_check(board, white):
    king_pos = find_king(board, white)
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece != ' ' and is_white(piece) != white:
                if king_pos in get_valid_moves(board, r, c):
                    return True
    return False

def has_legal_moves(board, white):
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece != ' ' and is_white(piece) == white:
                for r2, c2 in get_valid_moves(board, r, c):
                    temp = [row[:] for row in board]
                    move_piece(temp, r, c, r2, c2)
                    if not is_in_check(temp, white):
                        return True
    return False

#Game Loop 
def play_game():
    board = create_initial_board()
    white_turn = True

    while True:
        print_board(board)
        print("White's turn" if white_turn else "Black's turn")

        move_input = input("Enter move (e.g. e2 e4), or 'quit': ").strip().lower()
        if move_input in ['quit', 'exit']:
            print("Thanks for playing!")
            break

        try:
            start, end = move_input.split()
            r1, c1 = parse_position(start)
            r2, c2 = parse_position(end)

            piece = board[r1][c1]
            if piece == ' ':
                print("No piece at the starting square.")
                continue
            if white_turn and not is_white(piece):
                print("That's not your piece.")
                continue
            if not white_turn and not is_black(piece):
                print("That's not your piece.")
                continue

            if (r2, c2) not in get_valid_moves(board, r1, c1):
                print("Invalid move.")
                continue

            # Test Check
            test_board = [row[:] for row in board]
            move_piece(test_board, r1, c1, r2, c2)
            if is_in_check(test_board, white_turn):
                print("Move would leave your king in check.")
                continue

            # Make  move
            move_piece(board, r1, c1, r2, c2)
            white_turn = not white_turn

            # Check or Checkmate?
            if is_in_check(board, white_turn):
                if not has_legal_moves(board, white_turn):
                    print_board(board)
                    print("Checkmate! " + ("White" if not white_turn else "Black") + " wins.")
                    break
                else:
                    print("Check!")

        except Exception as e:
            print("Invalid input. Use format like 'e2 e4'.")

def main():
    play_game()

if __name__ == "__main__":
    main()

