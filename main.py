
# The board for sudoku
board = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]


def get_board():
    return board


def print_board(brd):
    for i in range(len(brd)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - ")
        for j in range(len(brd[0])):
            if j % 3 == 0 and j != 0:
                print("| ", end="")
            if j == 8:
                print(str(brd[i][j]))
            else:
                print(str(brd[i][j]) + " ", end="")


def find_next_empty(brd):
    for i in range(len(brd)):
        for j in range(len(brd[0])):
            if brd[i][j] == 0:
                return i, j
    return None


def is_valid(brd, pos, num):
    for i in range(len(brd[0])):
        if brd[pos[0]][i] == num and pos[1] != i:
            return False
    for i in range(len(brd)):
        if brd[i][pos[1]] == num and pos[0] != i:
            return False

    block_x = pos[0] // 3
    block_y = pos[1] // 3

    for i in range(block_x * 3, block_x * 3 + 3):
        for j in range(block_y * 3, block_y * 3 + 3):
            if brd[i][j] == num and (i, j) != pos:
                return False

    return True


def solve_sudoku(brd):
    position = find_next_empty(brd)
    if not position:
        return True

    row, col = position
    for i in range(1, 10):
        if is_valid(brd, position, i):
            brd[row][col] = i
            if solve_sudoku(brd):
                return True
            brd[row][col] = 0

    return False


if __name__ == "__main__":
    print("\nBoard Before Solving:\n")
    print_board(board)

    print()
    print("- " * 15)
    print("Board After Solving:\n")
    solve_sudoku(board)

    print_board(board)
