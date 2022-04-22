import random


"""this is a game, to win the game you have to open all the squares that not contains bombs"""


class MSSquare:
    def __init__(self, has_mine, hidden, neighbor_mines):
        self.__has_mine = has_mine
        self.__hidden = hidden
        self.__neighbor_mines = neighbor_mines

    @property
    def has_mine(self):
        return self.__has_mine

    @has_mine.setter
    def has_mine(self, has_mine):
        self.__has_mine = has_mine

    @property
    def hidden(self):
        return self.__hidden

    @hidden.setter
    def hidden(self, hidden):
        self.__hidden = hidden

    @property
    def neighbor_mines(self):
        return self.__neighbor_mines

    @neighbor_mines.setter
    def neighbor_mines(self, neighbor_mines):
        self.__neighbor_mines = neighbor_mines


def print_a_board_and_check_for_win(board):
    """this function get a list of squares and:
     1)print the board to the screen
     2)return how many squares are still hidden
    """
    hidden = 0
    print(" +-----" + "+-----" * (len(board) - 1) + "+")
    for y in range(len(board)):
        # loop on the board lines indexes
        print(f"{y + 1}|", end="")
        for x in range(len(board)):
            # loop on the squares indexes of every line
            if x == len(board) - 1:
                if board[y][x].hidden:
                    print("     |")
                    hidden += 1
                elif board[y][x].has_mine:
                    print("  X  |")
                else:
                    print(f"  {(board[y][x]).neighbor_mines}  |")
            elif board[y][x].hidden:
                print("     |", end="")
                hidden += 1
            elif board[y][x].has_mine:
                print("  X  |", end="")
            else:
                print(f"  {(board[y][x]).neighbor_mines}  |", end="")

        print(" +-----" + "+-----" * (len(board) - 1) + "+")
    print("  ", end="")
    for i in range(len(board)):
        # loop for printing the bottom line
        if i == len(board) - 1:
            print(f"  {i + 1}  ")
        else:
            print(f"  {i + 1}   ", end="")
    return hidden


def build_a_board(size, num_mines):
    # this function initialize the board at the begging of a game
    board = [[MSSquare(False, True, 0) for i in range(size)] for x in range(size)]
    # list compression to build the basic board without any mines
    neighbor_square = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
    for i in range(num_mines):
        # loop to set the bombs in random places
        while True:
            # loop to determine random square and set a bomb in it the random square already got a bomb running again
            y, x = random.randint(0, size - 1), random.randint(0, size - 1)
            if board[y][x].has_mine:
                continue
            board[y][x] = MSSquare(True, True, 1)
            for square in neighbor_square:
                # loop to add 1 to neighbor_mines for every neighbor squares
                if 0 <= y + square[0] <= size - 1 and 0 <= x + square[1] <= size - 1:
                    board[y + square[0]][x + square[1]].neighbor_mines += 1
            break
    return board


def open_all_zeros(y, x, board, already_checked):
    # if the user choose a square that have 0 in neighbor_mines this
    # recursive function will open all the squares that have zero neighbor_mines and those who
    # next to them that next to this square
    if [y, x] in already_checked:
        return
    already_checked.append([y, x])
    neighbor_square = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
    if board[y][x].neighbor_mines == 0:
        for square in neighbor_square:
            # check all the neighbor squares if 0 or nor and if they are send every one of them back to open_all_zeros
            if 0 <= y + square[0] <= len(board) - 1 and 0 <= x + square[1] <= len(board) - 1:
                board[y + square[0]][x + square[1]].hidden = False
                open_all_zeros(y + square[0], x + square[1], board, already_checked)


def main():
    print("Welcome to Minesweeper! ")
    while True:
        input_size = input("please enter your board size(between 4-9): ").strip()
        if not input_size.isdigit():
            print("board size must be a number")
            continue
        input_size = int(input_size)
        if 4 <= input_size <= 9:
            break
    while True:
        input_num_mines = input(f"how many mines do you want? (not more then {input_size * 2}): ").strip()
        if not input_num_mines.isdigit():
            print("please enter a number")
            continue
        input_num_mines = int(input_num_mines)
        if 0 < input_num_mines <= input_size * 2:
            break
    board = build_a_board(input_size, input_num_mines)
    print_a_board_and_check_for_win(board)
    while True:
        print("please enter your choice:")
        y = input("row: ").strip()
        if len(y) != 1 or not y.isdigit() or int(y) > input_size:
            print(f"please enter a row number smaller then {input_size}")
            continue
        x = input("column: ").strip()
        if len(x) != 1 or not x.isdigit() or int(x) > input_size:
            print(f"please enter a column number smaller then {input_size}")
            continue
        x, y = int(x)-1,int(y)-1
        board[y][x].hidden = False
        open_all_zeros(y, x, board, [])
        still_hidden = print_a_board_and_check_for_win(board)
        if still_hidden == input_num_mines:
            print("""
                                         _ _
                                        | | |
 _   _  ___  _   _  __      _____  _ __ | | |
| | | |/ _ \| | | | \ \ /\ / / _ \| '_ \| | |
| |_| | (_) | |_| |  \ V  V / (_) | | | |_|_|
 \__, |\___/ \__,_|   \_/\_/ \___/|_| |_(_|_)
  __/ |
 |___/

   """)
            break
        if board[y][x].has_mine:
            print("\nyou hit a mine, you lost..\n                   try again!")
            break
        print(f'{still_hidden-input_num_mines} still hidden. Keep trying!')


main()
