


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
        

gb = GameBoard()
gb.display()

while True:
    gb.get_move()
    gb.change_turn()

