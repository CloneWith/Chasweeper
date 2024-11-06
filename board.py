import curses
import random

class Board:
    def __init__(self, stdscr, size=7):
        self.stdscr = stdscr
        self.size = size
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.words = [
            "PYTHON", "CODE", "DEBUG", "ALGORITHM", "FUNCTION",
            "VARIABLE", "LOOP", "CONDITION", "ARRAY", "STRING",
            "COMPUTER", "PROGRAM", "LANGUAGE", "DEVELOPER", "SOFTWARE",
            "HARDWARE", "NETWORK", "DATABASE", "SECURITY", "ENCRYPTION"
        ]
        self.selected_words = []
        self.common_letters = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
        self.fill_board()
        self.exit_prompt = False
        self.menu_button_clicked = False

    def fill_board(self):
        # Filter out words longer than the board size
        valid_words = [word for word in self.words if len(word) <= self.size]

        # Randomly select 3 words to place on the board
        self.selected_words = random.sample(valid_words, 3)

        # Randomly place words on the board
        placed_letters = set()
        for word in self.selected_words:
            placed = False
            while not placed:
                direction = random.choice(['H', 'V'])  # H: Horizontal, V: Vertical
                if direction == 'H' and self.size - len(word) >= 0:
                    row = random.randint(0, self.size - 1)
                    col = random.randint(0, self.size - len(word))
                    if all(self.board[row][col + i] == ' ' for i in range(len(word))):
                        for i in range(len(word)):
                            self.board[row][col + i] = word[i]
                            placed_letters.add(word[i])
                        placed = True
                elif direction == 'V' and self.size - len(word) >= 0:
                    row = random.randint(0, self.size - len(word))
                    col = random.randint(0, self.size - 1)
                    if all(self.board[row + i][col] == ' ' for i in range(len(word))):
                        for i in range(len(word)):
                            self.board[row + i][col] = word[i]
                            placed_letters.add(word[i])
                        placed = True

        # Randomly fill some of the remaining empty cells with common letters
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == ' ' and random.random() < 0.3:  # 30% chance to fill the cell
                    # Avoid using letters that are already placed in words
                    available_letters = [letter for letter in self.common_letters if letter not in placed_letters]
                    self.board[i][j] = random.choice(available_letters)  # Randomly choose a common letter

        # Randomly place mines on the board
        mines_count = 0
        while mines_count < 5:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            if self.board[row][col] == ' ':
                self.board[row][col] = '*'
                mines_count += 1

    def draw_board(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        board_width = self.size * 4 + 1
        board_height = self.size * 2 + 1
        start_x = (w - board_width) // 2
        start_y = (h - board_height) // 2

        # Draw hints on the left-hand side
        hint_start_y = start_y
        self.stdscr.addstr(hint_start_y, 2, "Words left:")
        for idx, word in enumerate(self.selected_words):
            hint = " ".join("_" * len(word))
            self.stdscr.addstr(hint_start_y + idx + 1, 2, hint)

        for i in range(self.size + 1):
            for j in range(self.size):
                x = start_x + j * 4
                y = start_y + i * 2
                if i < self.size:
                    self.stdscr.addstr(y, x, '+---')
                else:
                    self.stdscr.addstr(y, x, '+---')
                if j == self.size - 1:
                    self.stdscr.addstr(y, x + 4, '+')
                if i < self.size:
                    self.stdscr.addstr(y + 1, x, f'| {self.board[i][j]} ')
                if i < self.size and j == self.size - 1:
                    self.stdscr.addstr(y + 1, x + 4, '|')

        # Ensure the bottom line is drawn correctly
        for j in range(self.size):
            x = start_x + j * 4
            y = start_y + self.size * 2
            self.stdscr.addstr(y, x, '+---')
        self.stdscr.addstr(y, x + 4, '+')

        # Draw the menu button and exit prompt on the same line
        if self.menu_button_clicked:
            self.stdscr.addstr(h - 2, w - 20, "[Click again to quit]", curses.A_REVERSE)
        else:
            self.stdscr.addstr(h - 2, w - 12, "[ Menu ]", curses.A_REVERSE)

        if self.exit_prompt:
            self.stdscr.addstr(h - 2, w - 50, "*Wanna quit? Press esc again to quit.")
        else:
            self.stdscr.addstr(h - 2, w - 50, "* Press 'esc' to quit")

        self.stdscr.refresh()

    def run(self):
        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
        self.draw_board()
        while True:
            key = self.stdscr.getch()
            if key == 27:  # ESC key
                if self.exit_prompt:
                    curses.endwin()
                    break
                else:
                    self.exit_prompt = True
                    self.draw_board()
            elif key == curses.KEY_MOUSE:
                _, mx, my, _, button_state = curses.getmouse()
                h, w = self.stdscr.getmaxyx()
                if my == h - 2 and w - 12 <= mx < w - 5:
                    if self.menu_button_clicked:
                        curses.endwin()
                        break
                    else:
                        self.menu_button_clicked = True
                        self.draw_board()
                else:
                    self.menu_button_clicked = False
                    self.exit_prompt = False
                    self.draw_board()
            else:
                self.menu_button_clicked = False
                self.exit_prompt = False
                self.draw_board()

if __name__ == "__main__":
    curses.wrapper(Board)