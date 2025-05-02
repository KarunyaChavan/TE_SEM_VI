def print_board(board):
    for row in board:
        print(' | '.join(row))
        print('-' * 5)

def is_winner(board, player):
    for i in range(3):
        if all([cell == player for cell in board[i]]) or all([board[j][i] == player for j in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2 - i] == player for i in range(3)]):
        return True
    return False

def is_full(board):
    return all(cell != ' ' for row in board for cell in row)

def evaluate(board):
    if is_winner(board, 'X'):
        return 1
    elif is_winner(board, 'O'):
        return -1
    else:
        return 0

def get_moves(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']

def minimax(board, is_max):
    if is_winner(board, 'X') or is_winner(board, 'O') or is_full(board):
        return evaluate(board)

    if is_max:
        best = -float('inf')
        for i, j in get_moves(board):
            board[i][j] = 'X'
            best = max(best, minimax(board, False))
            board[i][j] = ' '
        return best
    else:
        best = float('inf')
        for i, j in get_moves(board):
            board[i][j] = 'O'
            best = min(best, minimax(board, True))
            board[i][j] = ' '
        return best

def a_star_tic_tac_toe(board, player):
    best_score = -float('inf') if player == 'X' else float('inf')
    best_move = None

    for move in get_moves(board):
        i, j = move
        board[i][j] = player
        score = minimax(board, player == 'O')
        board[i][j] = ' '
        if (player == 'X' and score > best_score) or (player == 'O' and score < best_score):
            best_score = score
            best_move = move

    return best_move

# Game Loop
def play_game():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    print("You are O, AI is X")
    print_board(board)

    while True:
        # User move
        while True:
            try:
                row = int(input("Enter row (0-2): "))
                col = int(input("Enter col (0-2): "))
                if board[row][col] == ' ':
                    board[row][col] = 'O'
                    break
                else:
                    print("Cell already taken.")
            except (ValueError, IndexError):
                print("Invalid input. Enter numbers from 0 to 2.")

        print("\nYour move:")
        print_board(board)

        if is_winner(board, 'O'):
            print("🎉 You win!")
            break
        if is_full(board):
            print("Draw!")
            break

        # AI move
        print("AI is thinking...")
        ai_move = a_star_tic_tac_toe(board, 'X')
        if ai_move:
            board[ai_move[0]][ai_move[1]] = 'X'

        print("\nAI's move:")
        print_board(board)

        if is_winner(board, 'X'):
            print("💻 AI wins!")
            break
        if is_full(board):
            print("Draw!")
            break

# Start the game
play_game()
