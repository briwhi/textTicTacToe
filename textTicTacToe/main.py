


class GameBoard:
    def __init__(self):
        self.board = [
            ['   ', '|', '   ', '|', '   '],
            ['---', '-', '---', '-', '---'],
            ['   ', '|', '   ', '|', '   '],
            ['---', '-', '---', '-', '---'],
            ['   ', '|', '   ', '|', '   '],
                ]
        self.gameOver = False
        self.turn = ' X '
        self.winner = ' '

    def display(self):
        for line in self.board:
            row = ''
            for column in line:
                row += column
            print(row)

    def get_move(self):
        column = int(input(f'Enter column for {self.turn}: '))
        row = int(input(f'Enter row for {self.turn}: '))
        if column == 1:
            column = 0
        elif column == 3:
            column = 4
        if row == 1:
            row = 0
        elif row == 3:
            row = 4
        self.board[row][column] = self.turn
        self.display()

    def change_turn(self):
        if self.turn == ' X ':
            self.turn = ' O '
        else:
            self.turn = ' X '

    def check_win(self):
        wins = []
        for r in (0, 2, 4):
            wins.append([self.board[0][r], self.board[2][r], self.board[4][r]])
            wins.append([self.board[r][0], self.board[r][2], self.board[r][4]])
        wins.append([self.board[0][0], self.board[2][2], self.board[4][4]])
        wins.append([self.board[4][0], self.board[2][2], self.board[0][4]])
        for team in (' X ', ' O '):
            for w in wins:
                if w.count(team) == 3:
                    self.winner = team
                    self.gameOver = True


gb = GameBoard()
gb.display()

while not gb.gameOver:
    gb.get_move()
    gb.check_win()
    gb.change_turn()

print(f"{gb.winner} wins")
