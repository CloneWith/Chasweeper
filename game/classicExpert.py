import curses
import math
import random
import os

class Board:
    def __init__(self, stdscr, user, size=11):
        self.stdscr = stdscr
        self.user = user
        self.size = size
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.covered = [[True for _ in range(size)] for _ in range(size)]
        self.mine_hints = [[' ' for _ in range(size)] for _ in range(size)]  # Initialize mine hints matrix
        self.letter_hints = [[' ' for _ in range(size)] for _ in range(size)]  # Initialize letter hints matrix
        self.flagged = [[False for _ in range(size)] for _ in range(size)]  # Initialize flagged matrix
        self.questioned = [[False for _ in range(size)] for _ in range(size)]  # Initialize questioned matrix
        self.words, self.word_complexity = self.load_words()  # Load words and their complexity from file
        self.selected_words = []
        self.revealed_words = set()
        self.word_reveal_status = {}  # Track the reveal status of each word
        self.common_letters = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
        self.fill_board()
        self.exit_prompt = False
        self.game_won = False
        self.move_count = 0  # Initialize move counter
        self.last_revealed = None  # Track the last revealed cell
        self.current_word = None  # Track the current word being revealed
        self.score = 0  # Initialize score
        self.base_penalty_random = 0
        self.random_click_counter = 0
        self.random_click_cap = 5  # 've just typed in a random value, this value will get updated.
        self.user_stats = self.load_user_stats()

    def load_words(self):
        words = []
        word_complexity = {}
        with open('./data/words.txt', 'r') as file:
            for line in file:
                word, complexity = line.strip().split(',')
                words.append(word)
                word_complexity[word] = int(complexity)
        return words, word_complexity

    def load_user_stats(self):
        user_stats = {}
        if os.path.exists('./data/user.txt'):
            with open('./data/user.txt', 'r') as file:
                for line in file:
                    data = line.strip().split(',')
                    if len(data) == 11 and data[0] == self.user.user_id:  # Ensure the correct number of fields and match user ID
                        user_stats = {
                            'games_played': int(data[1]),
                            'games_won': int(data[2]),
                            'words_revealed': int(data[3]),
                            'longest_word_revealed': data[4],
                            'mines_stepped': int(data[5]),
                            'highest_score_classic': int(data[6]),
                            'highest_score_timed': int(data[7]),
                            'average_steps_used': float(data[8]),
                            'min_steps_used': int(data[9]),
                            'max_steps_used': int(data[10])
                        }
                        break
        return user_stats

    def save_user_stats(self):
        if os.path.exists('./data/user.txt'):
            with open('./data/user.txt', 'r') as file:
                lines = file.readlines()
            with open('./data/user.txt', 'w') as file:
                for line in lines:
                    data = line.strip().split(',')
                    if len(data) == 11 and data[0] == self.user.user_id:
                        data[1] = str(self.user_stats['games_played'])
                        data[2] = str(self.user_stats['games_won'])
                        data[3] = str(self.user_stats['words_revealed'])
                        data[4] = self.user_stats['longest_word_revealed']
                        data[5] = str(self.user_stats['mines_stepped'])
                        data[6] = str(self.user_stats['highest_score_classic'])
                        data[7] = str(self.user_stats['highest_score_timed'])
                        data[8] = str(self.user_stats['average_steps_used'])
                        data[9] = str(self.user_stats['min_steps_used'])
                        data[10] = str(self.user_stats['max_steps_used'])
                        file.write(','.join(data) + '\n')
                    else:
                        file.write(line)
        else:
            with open('./data/user.txt', 'w') as file:
                file.write(f"{self.user.user_id},{self.user_stats['games_played']},{self.user_stats['games_won']},{self.user_stats['words_revealed']},{self.user_stats['longest_word_revealed']},{self.user_stats['mines_stepped']},{self.user_stats['highest_score_classic']},{self.user_stats['highest_score_timed']},{self.user_stats['average_steps_used']},{self.user_stats['min_steps_used']},{self.user_stats['max_steps_used']}\n")

    def fill_board(self):
        # Reset the board and related variables
        self.board = [[' ' for _ in range(self.size)] for _ in range(self.size)]
        self.covered = [[True for _ in range(self.size)] for _ in range(self.size)]
        self.mine_hints = [[' ' for _ in range(self.size)] for _ in range(self.size)]
        self.letter_hints = [[' ' for _ in range(self.size)] for _ in range(self.size)]
        self.flagged = [[False for _ in range(self.size)] for _ in range(self.size)]
        self.selected_words = []
        self.revealed_words = set()
        self.word_reveal_status = {}
        self.move_count = 0
        self.last_revealed = None
        self.current_word = None
        self.score = 0

        # Filter out words longer than the board size
        valid_words = [word for word in self.words if len(word) <= self.size]

        # Randomly select 7 words to place on the board
        self.selected_words = random.sample(valid_words, 7)

        # Initialize the reveal status for each selected word
        for word in self.selected_words:
            self.word_reveal_status[word] = []

        # Randomly place words on the board
        placed_letters = set()
        word_positions = []
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
                            word_positions.append((row, col + i))
                        placed = True
                elif direction == 'V' and self.size - len(word) >= 0:
                    row = random.randint(0, self.size - len(word))
                    col = random.randint(0, self.size - 1)
                    if all(self.board[row + i][col] == ' ' for i in range(len(word))):
                        for i in range(len(word)):
                            self.board[row + i][col] = word[i]
                            placed_letters.add(word[i])
                            word_positions.append((row + i, col))
                        placed = True

        # Randomly fill some of the remaining empty cells with common letters
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == ' ' and random.random() < 0.17:  # Chance to fill the cell
                                                                        # Reduce this value to increase the number of empty cells
                    # Avoid using letters that are already placed in words
                    available_letters = [letter for letter in self.common_letters if letter not in placed_letters]
                    self.board[i][j] = random.choice(available_letters)  # Randomly choose a common letter

        # Generate a list of all possible positions
        possible_positions = [(i, j) for i in range(1, self.size - 1) for j in range(1, self.size - 1) if self.board[i][j] == ' ']

        # Randomly shuffle the list of possible positions
        random.shuffle(possible_positions)

        # Ensure there are enough positions to place mines
        num_mines = 12
        if len(possible_positions) < num_mines:
            num_mines = len(possible_positions)

        # Place mines in the first num_mines positions from the shuffled list
        for i in range(num_mines):
            row, col = possible_positions[i]
            self.board[row][col] = '✱'

        # Calculate mine hints for each cell
        for i in range(self.size):
            for j in range(self.size):
                self.mine_hints[i][j] = self.calculate_mine_hint(i, j)

        # Calculate letter hints for each empty cell
        for i in range(self.size):
            for j in range(self.size):
                self.letter_hints[i][j] = self.calculate_letter_hint(i, j)

    def calculate_mine_hint(self, row, col):
        hint = [' ', ' ']

        def has_mine_in_direction(dir_row, dir_col):
            new_row = row + dir_row
            new_col = col + dir_col
            if 0 <= new_row < self.size and 0 <= new_col < self.size:
                if self.board[new_row][new_col] == '✱':
                    return True
            return False

        # Check for mines in all 8 directions
        top = has_mine_in_direction(-1, 0)
        bottom = has_mine_in_direction(1, 0)
        left = has_mine_in_direction(0, -1)
        right = has_mine_in_direction(0, 1)
        top_left = has_mine_in_direction(-1, -1)
        bottom_left = has_mine_in_direction(1, -1)
        top_right = has_mine_in_direction(-1, 1)
        bottom_right = has_mine_in_direction(1, 1)

        # Special case: three mines in a same row
        if top and top_left and top_right:
            hint[0] = '⠁'
            hint[1] = '⠈'  # Top, top-left, and top-right can be represented as ⠁⠈

        if bottom and bottom_left and bottom_right:
            hint[0] = '⡀'
            hint[1] = '⢀'  # Bottom, bottom-left, and bottom-right can be represented as ⡀⢀

        # Special case: three mines in a same column
        if left and top_left and bottom_left:
            hint[0] = '⡁'
        if right and top_right and bottom_right:
            hint[1] = '⢈'
        
        # Special case: three mines on the same direction
        if top and top_left and left:
            hint[0] = '⠁'
        if top and top_right and right:
            hint[1] = '⠈'
        if bottom and bottom_left and left:
            hint[0] = '⡀'
        if bottom and bottom_right and right:
            hint[1] = '⢀'

        # Special case: three mines forming < or > shape
        if top and left and bottom:
            hint[0] = '⡁'
            # Top and left
            if top and left:
                hint[0] = '⠁'  # Top and left, use ⠁ for top
            # Bottom and left
            if bottom and left:
                hint[0] = '⡀'  # Bottom and left, use ⡀

        if top and right and bottom:
            hint[1] = '⢈'
            # Top and right
            if top and right:
                hint[1] = '⠈'  # Top and right, use ⠈ for right
            # Right and bottom
            if right and bottom:
                hint[1] = '⢀'  # Right and bottom, use ⢀

        # Bottom and bottom-left/bottom-right
        if bottom and bottom_left:
            hint[0] = '⡀'  # Bottom and bottom-left only needs one dot (⡀)
        elif bottom and bottom_right:
            hint[1] = '⢀'  # Bottom and bottom-right only needs one dot (⢀)

        ### Special cases: two mines in same row or column
        # Top and top-left/top-right
        if top and top_left:
            hint[0] = '⠁'  # Top and top-left only needs one dot (⠁)
        elif top and top_right:
            hint[1] = '⠈'  # Top and top-right only needs one dot (⠈)

        ### Special cases: opposite directions
        # Left and right
        if left and right:
            hint[0] = '⡀'
            hint[1] = '⠈'  # Left and right can be represented as ⡀⠈

        # Top and bottom
        if top and bottom:
            if hint[0] == ' ':
                hint[0] = '⠁'
            if hint[1] == ' ':
                hint[1] = '⢀'  # Top and bottom can be represented as ⠁⢀

        # Special case: two mines in the same row on corners
        if top_left and top_right:
            hint[0] = '⠁'
            hint[1] = '⠈'  # Top-left and top-right can be represented as ⠁⠈

        if bottom_left and bottom_right:
            hint[0] = '⡀'
            hint[1] = '⢀'  # Bottom-left and bottom-right can be represented as ⡀⢀

        if left and top_left and hint[0] == ' ':
            hint[0] = '⠁'  # Combine left and top-left as one dot (⠁)
        elif left and bottom_left and hint[0] == ' ':
            hint[0] = '⡀'  # Combine left and bottom-left as one dot (⡀)
        elif top_left and bottom_left and hint[0] == ' ':
            hint[0] = '⡁'  # Combine top-left and bottom-left as ⡁
        else:
            if left:
                hint[0] = '⡀'
            if top_left:
                hint[0] = '⠁'
            if bottom_left:
                hint[0] = '⡀'

        if right and top_right and hint[1] == ' ':
            hint[1] = '⠈'  # Combine right and top-right as one dot (⠈)
        elif right and bottom_right and hint[1] == ' ':
            hint[1] = '⢀'  # Combine right and bottom-right as one dot (⢀)
        elif top_right and bottom_right and hint[1] == ' ':
            hint[1] = '⢈'  # Combine top-right and bottom-right as ⢈
        else:
            if right:
                hint[1] = '⠈'
            if top_right:
                hint[1] = '⠈'
            if bottom_right:
                hint[1] = '⢀'

        # Updated `if top:` condition
        if top:
            if not (hint[0] in ['⠁', '⡁'] or hint[1] in ['⢈', '⠈']):
                if hint[0] == ' ':
                    hint[0] = '⠁'
                elif hint[1] == ' ':
                    hint[1] = '⠈'
                elif hint[0] == '⡀':
                    hint[0] = '⡁'
                elif hint[1] == '⢀':
                    hint[1] = '⢈'

        if bottom:
            if not (hint[0] in ['⡀', '⡁'] or hint[1] in ['⢈', '⢀']):
                if hint[0] == ' ':
                    hint[0] = '⡀'
                elif hint[1] == ' ':
                    hint[1] = '⢀'
                elif hint[0] == '⠁':
                    hint[0] = '⡁'
                elif hint[1] == '⠈':
                    hint[1] = '⢈'
            
            

        return hint

    def calculate_letter_hint(self, row, col):
        count = 0
        for i in range(max(0, row - 1), min(self.size, row + 2)):
            for j in range(max(0, col - 1), min(self.size, col + 2)):
                # Check if the character is part of any selected word
                if any(self.board[i][j] in word for word in self.selected_words):
                    count += 1
        return str(count) if count > 0 else ' '  # Return the count as a string, or a space if count is 0

    def display_user_info(self):
        h, w = self.stdscr.getmaxyx()
        user_info_win = curses.newwin(7, 40, 1, w - 41)
        user_info_win.border('|', '|', '-', '-', '+', '+', '+', '+')
        user_info_win.addstr(1, 2, f"Player: ")
        user_info_win.addstr(1, 12, f"{self.user.user_id}", curses.A_BOLD)
        user_info_win.addstr(3, 2, f"Highest Score: ")
        user_info_win.addstr(3, 17, f"{self.user_stats.get('highest_score_classic', 'N/A')}", curses.A_BOLD)
        user_info_win.addstr(4, 2, f"Games Won: ")
        user_info_win.addstr(4, 13, f"{self.user_stats.get('games_won', 0)}", curses.A_BOLD)
        user_info_win.addstr(5, 2, f"Win rate: ")
        games_played = self.user_stats.get('games_played', 1)
        win_rate = (self.user_stats.get('games_won', 0) / games_played * 100) if games_played > 0 else 0
        user_info_win.addstr(5, 12, f"{win_rate:.2f}%", curses.A_BOLD)
        user_info_win.refresh()

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
            if word in self.revealed_words:
                self.stdscr.addstr(hint_start_y + idx + 1, 2, word)
            else:
                hint = " ".join("_" * len(word))
                self.stdscr.addstr(hint_start_y + idx + 1, 2, hint)

        # Draw move counter below the hint section
        self.stdscr.addstr(hint_start_y + len(self.selected_words) + 2, 2, "Moves: ")
        self.stdscr.addstr(hint_start_y + len(self.selected_words) + 2, 9, f"{self.move_count}", curses.A_BOLD)

        # Draw score below the move counter
        self.stdscr.addstr(hint_start_y + len(self.selected_words) + 3, 2, "Score: ")
        self.stdscr.addstr(hint_start_y + len(self.selected_words) + 3, 9, f"{self.score}", curses.A_BOLD)

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
                    if self.covered[i][j]:
                        if self.flagged[i][j]:
                            self.stdscr.addstr(y + 1, x, '|🚩▒')
                        elif self.questioned[i][j]:
                            self.stdscr.addstr(y + 1, x, '|❔▒')
                        else:
                            self.stdscr.addstr(y + 1, x, '|▒▒▒')
                    else:
                        mine_hint = self.mine_hints[i][j]
                        letter_hint = self.letter_hints[i][j]
                        if self.board[i][j] == ' ':
                            cell_content = f'{mine_hint[0]}{letter_hint}{mine_hint[1]}'
                        else:
                            cell_content = f'{mine_hint[0]}{self.board[i][j]}{mine_hint[1]}'
                        self.stdscr.addstr(y + 1, x, f'|{cell_content}')
                if i < self.size and j == self.size - 1:
                    self.stdscr.addstr(y + 1, x + 4, '|')

        # Ensure the bottom line is drawn correctly
        for j in range(self.size):
            x = start_x + j * 4
            y = start_y + self.size * 2
            self.stdscr.addstr(y, x, '+---')
        self.stdscr.addstr(y, x + 4, '+')

        if self.exit_prompt:
            self.stdscr.addstr(h - 2, w - 50, "* Wanna quit? Press esc again to quit.")
        else:
            self.stdscr.addstr(h - 2, w - 50, "* Press 'esc' to quit")

        # Draw the winning message if the game is won
        if self.game_won:
            win_msg_y = h // 2 - 2
            self.stdscr.addstr(win_msg_y, w - 30, "Congratulations!")
            self.stdscr.addstr(win_msg_y + 1, w - 30, "You found all the words!")
            self.stdscr.addstr(win_msg_y + 3, w - 30, "Press N for New Game")

        self.stdscr.refresh()

    def calculate_base_score(self, word):
        word_length = len(word)
        word_complexity = self.word_complexity.get(word, 1)
        base_score = word_length * word_complexity
        return base_score

    def calculate_clean_reveal_bonus(self, clean_reveal, word):
        bonus_score = 0
        if clean_reveal:
            word_length = len(word)
            word_complexity = self.word_complexity.get(word, 1)
            bonus_score = 10 + word_length * word_complexity  # Example bonus for clean reveal
        return bonus_score

    def calculate_total_score(self, word, clean_reveal):
        word_length = len(word)
        word_complexity = self.word_complexity.get(word, 1)
        base_score = word_length * word_complexity * 100  # Increase base score
        clean_bonus = 0
        if clean_reveal:
            clean_bonus = (word_length * word_complexity * 50)  # Increase clean reveal bonus
        total_score = base_score + clean_bonus
        return total_score

    def check_revealed_words(self):
        for word in self.selected_words:
            revealed = True
            for i in range(self.size):
                for j in range(self.size):
                    if self.board[i][j] == word[0]:
                        if self.check_word_revealed(i, j, word, 'H') or self.check_word_revealed(i, j, word, 'V'):
                            if word not in self.revealed_words:
                                clean_reveal = all(cell in self.word_reveal_status[word] for cell in self.get_word_cells(word))
                                self.revealed_words.add(word)
                                self.word_reveal_status[word] = []  # Reset word reveal status
                                self.current_word = None  # Reset current word
                                self.score += self.calculate_total_score(word, clean_reveal)
                                self.adjust_random_click_cap()
                                self.award_bonus_points()

    def adjust_random_click_cap(self):
        words_left = len(self.selected_words) - len(self.revealed_words)
        if words_left == 7:
            self.random_click_cap = 22  # Stage 1 random click cap
        elif words_left == 6:
            self.random_click_cap = 19  # Stage 2 random click cap
            self.random_click_counter = max(0, self.random_click_counter - 10)  # Reduce random click counter if player revealed a word
        elif words_left == 5:
            self.random_click_cap = 17  # Stage 3 random click cap
        elif words_left == 4:
            self.random_click_cap = 15  # same here
            self.random_click_counter = max(0, self.random_click_counter - 9)
        elif words_left == 3:
            self.random_click_cap = 12  #
            self.random_click_counter = max(0, self.random_click_counter - 8)
        elif words_left == 2:
            self.random_click_cap = 11  
            self.random_click_counter = max(0, self.random_click_counter - 7)
        elif words_left == 1:
            self.random_click_cap = 9
            self.random_click_counter = max(0, self.random_click_counter - 5)

    def award_bonus_points(self):
        words_left = len(self.selected_words) - len(self.revealed_words)
        if words_left == 7 and self.random_click_counter <= self.random_click_cap:
            self.score += 800 * max(1, (self.random_click_cap - self.random_click_counter))  # Stage 1 bonus points
        elif words_left == 6 and self.random_click_counter <= self.random_click_cap:
            self.score += 700 * max(1, (self.random_click_cap - self.random_click_counter)) # Stage 2 bonus points
        elif words_left == 5 and self.random_click_counter <= self.random_click_cap:
            self.score += 650 * max(1, (self.random_click_cap - self.random_click_counter))  # Stage 1 bonus points
        elif words_left == 4 and self.random_click_counter <= self.random_click_cap:
            self.score += 500 * max(1, (self.random_click_cap - self.random_click_counter)) # Stage 2 bonus points
        elif words_left == 3 and self.random_click_counter <= self.random_click_cap:
            self.score += 450 * max(1, (self.random_click_cap - self.random_click_counter))  # Stage 3 bonus points
        elif words_left == 2 and self.random_click_counter <= self.random_click_cap:
            self.score += 400 * max(1, (self.random_click_cap - self.random_click_counter)) # Stage 4 bonus points
        elif words_left == 1 and self.random_click_counter <= self.random_click_cap:
            self.score += 350 * max(1, (self.random_click_cap - self.random_click_counter)) # Stage 5 bonus points

    def penalty_multiplier(self, random_click_counter, cap_value):
        k = 0.01
        
        if random_click_counter <= (cap_value - 2):
            return (math.exp(k * (random_click_counter - cap_value)) - 0.6)
        elif (cap_value - 2) < random_click_counter <= cap_value:
            return (random_click_counter - (cap_value - 2)) / 2
        else:
            return math.exp(k * (random_click_counter - cap_value))


    def get_word_cells(self, word):
        cells = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == word[0]:
                    if self.check_word_revealed(i, j, word, 'H'):
                        cells.extend([(i, j + k) for k in range(len(word))])
                    elif self.check_word_revealed(i, j, word, 'V'):
                        cells.extend([(i + k, j) for k in range(len(word))])
        return cells

    def check_word_revealed(self, row, col, word, direction):
        if direction == 'H':
            if col + len(word) > self.size:
                return False
            for i in range(len(word)):
                if self.board[row][col + i] != word[i] or self.covered[row][col + i]:
                    return False
        elif direction == 'V':
            if row + len(word) > self.size:
                return False
            for i in range(len(word)):
                if self.board[row + i][col] != word[i] or self.covered[row + i][col]:
                    return False
        return True

    def check_all_words_revealed(self):
        return all(word in self.revealed_words for word in self.selected_words)

    def check_window_size(self):
        h, w = self.stdscr.getmaxyx()
        min_height = 25
        min_width = 142

        if h < min_height or w < min_width:
            size_prompt = curses.newwin(h, w, 0, 0)
            size_prompt.clear()
            message = "Terminal window is too small! Please increase the window size."
            y = h // 2
            x = (w - len(message)) // 2
            size_prompt.addstr(y, x, message, curses.A_BOLD)
            size_prompt.refresh()
            size_prompt.getch()  # Wait for user input
            return False
        return True

    def update_stats(self, game_won):
        self.user_stats['games_played'] += 1
        if game_won:
            self.user_stats['games_won'] += 1
        if self.score > self.user_stats['highest_score_classic']:
            self.user_stats['highest_score_classic'] = self.score
        self.save_user_stats()

    def run(self):
        while True:
            if not self.check_window_size():
                continue

            curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
            self.draw_board()
            while True:
                if not self.check_window_size():
                    break
                
                self.display_user_info()
                key = self.stdscr.getch()
                if key == 27:  # ESC key
                    if self.exit_prompt:
                        if not self.game_won:
                            self.update_stats(self.game_won)
                        curses.endwin()
                        return
                    else:
                        self.exit_prompt = True
                        self.draw_board()
                elif key == ord('n') and self.game_won:
                    self.__init__(self.stdscr, self.user, self.size)
                    self.run()
                elif self.check_all_words_revealed():
                    self.game_won = True
                    self.stdscr.refresh()
                elif key == curses.KEY_MOUSE and not self.game_won:
                    _, mx, my, _, button_state = curses.getmouse()
                    h, w = self.stdscr.getmaxyx()
                    start_x = (w - (self.size * 4 + 1)) // 2
                    start_y = (h - (self.size * 2 + 1)) // 2
                    if start_y <= my < start_y + self.size * 2 and start_x <= mx < start_x + self.size * 4:
                        cell_x = (mx - start_x) // 4
                        cell_y = (my - start_y) // 2
                        if button_state & curses.BUTTON1_CLICKED and (button_state & curses.BUTTON_CTRL):  # Ctrl + Left click
                            if self.covered[cell_y][cell_x]:
                                if self.flagged[cell_y][cell_x]:
                                    self.flagged[cell_y][cell_x] = False
                                    self.questioned[cell_y][cell_x] = True
                                elif self.questioned[cell_y][cell_x]:
                                    self.questioned[cell_y][cell_x] = False
                                else:
                                    self.flagged[cell_y][cell_x] = True
                                self.draw_board()
                        elif self.covered[cell_y][cell_x]:
                            self.covered[cell_y][cell_x] = False
                            self.move_count += 1  # Increment move counter
                            if self.board[cell_y][cell_x] == '✱':
                                revealed_cells = sum(not self.covered[i][j] for i in range(self.size) for j in range(self.size))
                                total_cells = self.size * self.size
                                base_penalty = 1500         # Base penalty for revealing a mine
                                k = (220 - total_cells) / 3000
                                penalty = int((math.exp(k * (revealed_cells - 5)) - total_cells / 900) * base_penalty)
                                self.score -= int(penalty)  # Dynamic penalty for revealing a mine
                                for word in self.selected_words:
                                    self.word_reveal_status[word] = []  # Reset word reveal status for all words
                                self.current_word = None  # Reset current word
                            else:
                                self.last_revealed = (cell_y, cell_x)
                                # Check if the revealed cell is part of a selected word
                                is_part_of_word = False
                                for word in self.selected_words:
                                    if self.board[cell_y][cell_x] in word:
                                        is_part_of_word = True
                                        if self.current_word is None:
                                            self.current_word = word
                                        if self.current_word == word:
                                            self.word_reveal_status[word].append((cell_y, cell_x))
                                if (not is_part_of_word) or (is_part_of_word and self.random_click_counter == 0):
                                    self.random_click_counter += 1
                                    words_left = len(self.selected_words) - len(self.revealed_words)
                                    if words_left == 7:
                                        self.base_penalty_random = 200  # Base penalty for random clicks
                                    elif words_left == 6:
                                        self.base_penalty_random = 300  # same here
                                    elif words_left == 5:
                                        self.base_penalty_random = 400
                                    elif words_left == 4:
                                        self.base_penalty_random = 800
                                    elif words_left == 3:
                                        self.base_penalty_random = 1100
                                    elif words_left == 2:
                                        self.base_penalty_random = 1500
                                    elif words_left == 1:
                                        self.base_penalty_random = 1700
                                    else:
                                        self.base_penalty_random = 0
                                    
                                if self.random_click_cap is not None:
                                    penalty_multiplier_value = self.penalty_multiplier(self.random_click_counter, self.random_click_cap)
                                    penalty_random = int(self.base_penalty_random * penalty_multiplier_value)
                                    self.score -= penalty_random
                                self.check_revealed_words()  # This will now only score for full word reveals
                            self.draw_board()
                            if self.check_all_words_revealed():
                                self.game_won = True
                                self.update_stats(self.game_won)
                                self.draw_board()
                elif key == ord('q') and self.game_won:
                    curses.endwin()
                    break
                else:
                    self.exit_prompt = False
                    self.draw_board()

if __name__ == "__main__":
    curses.wrapper(Board)