import tkinter as tk

# ─── A* Algorithm ──────────────────────────────────────────────────────────────
def is_winner(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)): return True
        if all(board[j][i] == player for j in range(3)): return True
    if all(board[i][i] == player for i in range(3)): return True
    if all(board[i][2-i] == player for i in range(3)): return True
    return False

def is_full(board):
    return all(board[i][j] != '' for i in range(3) for j in range(3))

def evaluate(board):
    if is_winner(board, 'X'):
        return 100
    if is_winner(board, 'O'):
        return -100

    score = 0
    for i in range(3):
        row = [board[i][j] for j in range(3)]
        col = [board[j][i] for j in range(3)]
        score += evaluate_line(row)
        score += evaluate_line(col)

    diag1 = [board[i][i] for i in range(3)]
    diag2 = [board[i][2-i] for i in range(3)]
    score += evaluate_line(diag1)
    score += evaluate_line(diag2)

    return score

def evaluate_line(line):
    score = 0
    if line.count('X') == 2 and line.count('') == 1:
        score += 10
    elif line.count('O') == 2 and line.count('') == 1:
        score -= 10
    elif line.count('X') == 1 and line.count('') == 2:
        score += 1
    elif line.count('O') == 1 and line.count('') == 2:
        score -= 1
    return score

def get_moves(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']

def astar_best_move(board, player):
    best_move = None
    best_score = float('-inf') if player == 'X' else float('inf')

    for i, j in get_moves(board):
        board[i][j] = player
        score = evaluate(board)
        board[i][j] = ''

        if (player == 'X' and score > best_score) or (player == 'O' and score < best_score):
            best_score = score
            best_move = (i, j)

    return best_move

# ─── UI ───────────────────────────────────────────────────────────────────────

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe: You (O) vs AI (X)")
        self.root.resizable(False, False)
        self.buttons = [[None]*3 for _ in range(3)]
        self.board = [['']*3 for _ in range(3)]

        for i in range(3):
            for j in range(3):
                btn = tk.Button(root, text='', font=('Helvetica', 32), width=4, height=2,
                                command=lambda r=i, c=j: self.human_move(r, c))
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.buttons[i][j] = btn

        self.status = tk.Label(root, text="Your turn", font=('Helvetica', 16))
        self.status.grid(row=3, column=0, columnspan=3, pady=(10, 0))

    def human_move(self, i, j):
        if self.board[i][j]:
            return
        self._mark(i, j, 'O')

        if is_winner(self.board, 'O'):
            self.status['text'] = "🎉 You win!"
            self.disable_all_buttons()
            return
        if is_full(self.board):
            self.status['text'] = "Draw!"
            return

        self.status['text'] = "AI is thinking..."
        self.root.update()

        ai_move = astar_best_move(self.board, 'X')
        if ai_move:
            self._mark(ai_move[0], ai_move[1], 'X')

        if is_winner(self.board, 'X'):
            self.status['text'] = "💥 AI wins!"
            self.disable_all_buttons()
        elif is_full(self.board):
            self.status['text'] = "Draw!"
        else:
            self.status['text'] = "Your turn"

    def _mark(self, i, j, player):
        self.board[i][j] = player
        self.buttons[i][j]['text'] = player
        self.buttons[i][j]['fg'] = 'red' if player == 'X' else 'blue'

    def disable_all_buttons(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]['state'] = 'disabled'

# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()
