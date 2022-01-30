import pygame as pg
import time
from main import is_valid, solve_sudoku, get_board, find_next_empty

pg.font.init()
font = pg.font.SysFont("comicsans", 28)


class Square:
    def __init__(self, row, col, width, height, value):
        self.row = row
        self.col = col
        self.value = value
        self.temp = 0
        self.width = width
        self.height = height
        self.is_selected = None

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val

    def draw(self, window):
        box_width = self.width / 9
        x = self.col * box_width
        y = self.row * box_width

        if self.temp != 0 and self.value == 0:
            number = font.render(str(self.temp), True, (128, 128, 128))
            window.blit(number, (x + (box_width - number.get_width()) / 2, y + (box_width - number.get_height()) / 2))
        elif self.value != 0:
            number = font.render(str(self.value), True, (0, 0, 0))
            pg.draw.rect(window, (0, 255, 0), (x, y, box_width, box_width), 0)
            window.blit(number, (x + (box_width - number.get_width()) / 2, y + (box_width - number.get_height()) / 2))

        if self.is_selected:
            pg.draw.rect(window, (255, 0, 0), (x, y, box_width, box_width), 3)

    def update_drawing(self, window, valid=True):
        box_width = self.width / 9
        x = self.col * box_width
        y = self.row * box_width

        pg.draw.rect(window, (255, 255, 255), (x, y, box_width, box_width), 0)
        number = font.render(str(self.value), True, (0, 0, 0))
        if valid:
            pg.draw.rect(window, (0, 255, 0), (x, y, box_width, box_width), 0)
        else:
            pg.draw.rect(window, (255, 0, 0), (x, y, box_width, box_width), 0)
        window.blit(number, (x + (box_width - number.get_width()) / 2, y + (box_width - number.get_height()) / 2))


class sudoku_matrix:
    board = get_board()

    def __init__(self, rows, cols, width, height, window):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.window = window
        self.squares = [[Square(i, j, width, height, self.board[i][j]) for j in range(cols)] for i in range(rows)]
        self.model = None
        self.selected_row_col = None
        self.strikes = 0

    def update_model(self):
        self.model = [[self.squares[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def draw_board(self):
        self.draw_squares()
        self.draw_matrix_lines()

    def draw_matrix_lines(self):
        box_width = self.width / 9

        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                line_size = 4
            else:
                line_size = 1

            pg.draw.line(self.window, (0, 0, 0), (0, i * box_width), (self.width, i * box_width), line_size)
            pg.draw.line(self.window, (0, 0, 0), (i * box_width, 0), (i * box_width, self.height), line_size)

    def draw_squares(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.squares[i][j].draw(self.window)

    def get_clicked_pos(self, positions):
        box_width = self.width / 9
        if positions[0] < self.width and positions[1] < self.height:
            y = positions[1] // box_width  # gives row number
            x = positions[0] // box_width  # gives column number
            return int(y), int(x)
        else:
            return None

    def select_square(self, position):
        self.selected_row_col = position

        for i in range(self.rows):
            for j in range(self.cols):
                self.squares[i][j].is_selected = False
        row, col = position
        self.squares[row][col].is_selected = True

    def update_temp_square(self, key):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.squares[i][j].is_selected and self.squares[i][j].value == 0:
                    self.squares[i][j].temp = key

    def clear(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.squares[i][j].is_selected:
                    self.squares[i][j].temp = 0

    def confirm_position(self):
        x, y = self.selected_row_col
        if self.squares[x][y].value == 0:
            self.squares[x][y].set(self.squares[x][y].temp)
            self.update_model()
        else:
            return True

        if is_valid(self.board, self.selected_row_col, self.squares[x][y].value) and solve_sudoku(self.model):
            return True
        else:
            self.squares[x][y].set(0)
            # self.squares[x][y].set_temp(0)
            self.update_model()
            return False

    def solve_sudoku_gui(self):
        self.update_model()
        position = find_next_empty(self.model)
        if not position:
            return True

        row, col = position
        for i in range(1, 10):
            if is_valid(self.model, position, i):
                self.squares[row][col].set(i)
                self.update_model()
                self.squares[row][col].update_drawing(self.window, True)
                self.draw_matrix_lines()
                pg.display.update()
                pg.time.delay(50)

                if self.solve_sudoku_gui():
                    return True

                self.squares[row][col].set(0)
                self.update_model()
                self.squares[row][col].update_drawing(self.window, False)
                self.draw_matrix_lines()
                pg.display.update()
                pg.time.delay(50)

        return False

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.squares[i][j].value == 0:
                    return False
        return True


def get_time(duration):
    minutes = duration // 60
    seconds = duration % 60
    msg = str(minutes) + "m " + str(seconds) + "s"
    return msg


def redraw_window(window, board, play_time):
    window.fill((255, 255, 255))
    if board.is_finished():
        display_msg = font.render("Game over with playtime:  " + get_time(play_time), True, (255, 0, 0))
        window.blit(display_msg, (15, 550))
    else:
        display_time = font.render("Time:  " + get_time(play_time), True, (255, 0, 0))
        window.blit(display_time, (540 - 200, 550))
        display_strikes = font.render("X " * min(10,board.strikes) , True, (255, 0, 0))
        window.blit(display_strikes, (15, 560))
    board.draw_board()
    pg.display.update()


def handle_key_events(event, board):
    key = None
    if event.key == pg.K_1:
        key = 1
    if event.key == pg.K_2:
        key = 2
    if event.key == pg.K_3:
        key = 3
    if event.key == pg.K_4:
        key = 4
    if event.key == pg.K_5:
        key = 5
    if event.key == pg.K_6:
        key = 6
    if event.key == pg.K_7:
        key = 7
    if event.key == pg.K_8:
        key = 8
    if event.key == pg.K_9:
        key = 9
    if event.key == pg.K_KP1:
        key = 1
    if event.key == pg.K_KP2:
        key = 2
    if event.key == pg.K_KP3:
        key = 3
    if event.key == pg.K_KP4:
        key = 4
    if event.key == pg.K_KP5:
        key = 5
    if event.key == pg.K_KP6:
        key = 6
    if event.key == pg.K_KP7:
        key = 7
    if event.key == pg.K_KP8:
        key = 8
    if event.key == pg.K_KP9:
        key = 9
    if event.key == pg.K_DELETE:
        board.clear()
        key = None
    if event.key == pg.K_SPACE:
        board.solve_sudoku_gui()
        key = None
    if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
        if board.confirm_position():
            print("Success")
        else:
            print("Wrong")
            board.strikes += 1
        key = None
    return key


def handle_mouse_events(board):
    position = pg.mouse.get_pos()
    clicked_pos = board.get_clicked_pos(position)
    board.select_square(clicked_pos)
    return clicked_pos


def main():
    window = pg.display.set_mode((540, 600))
    pg.display.set_caption("Sudoku GUI")

    board = sudoku_matrix(9, 9, 540, 540, window)

    game_start_time = time.time()
    play_time = None
    running = True
    key = None
    clock = pg.time.Clock()

    while running:
        if not board.is_finished():
            play_time = round(time.time() - game_start_time)
        clock.tick(20)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                key = handle_key_events(event, board)

            if event.type == pg.MOUSEBUTTONDOWN:
                handle_mouse_events(board)
                key = None

            if board.selected_row_col and key is not None:
                board.update_temp_square(key)

        redraw_window(window, board, play_time)
    print("\nGame over with playtime:  " + get_time(play_time))


if __name__ == "__main__":
    main()
