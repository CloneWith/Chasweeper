# A module for the classic easy mode of The Puzzle Game.
# This module contains the Board class, which represents the game board and handles the game logic, 
# user input, and game state updates for the classic easy mode of The Puzzle Game.

import curses
import math
import random
import os

class Board:

    # A class to represent the game board for The Puzzle Game.
    # Attributes:
    # -----------
    # stdscr : curses.window
    #     The standard screen window for displaying the game.
    # user : User
    #     The user playing the game.
    # size : int, optional
    #     The size of the game board (default is 7).
    # board : list of list of str
    #     The game board matrix.
    # covered : list of list of bool
    #     Matrix indicating whether each cell is covered.
    # mine_hints : list of list of str
    #     Matrix containing hints for mines.
    # letter_hints : list of list of str
    #     Matrix containing hints for letters.
    # flagged : list of list of bool
    #     Matrix indicating whether each cell is flagged.
    # questioned : list of list of bool
    #     Matrix indicating whether each cell is questioned.
    # words : list of str
    #     List of words loaded from file.
    # word_complexity : dict
    #     Dictionary mapping words to their complexity.
    # selected_words : list of str
    #     List of words selected to be placed on the board.
    # revealed_words : set
    #     Set of words that have been revealed.
    # word_reveal_status : dict
    #     Dictionary tracking the reveal status of each word.
    # common_letters : str
    #     String of common letters used to fill the board.
    # exit_prompt : bool
    #     Flag indicating whether the exit prompt is displayed.
    # game_won : bool
    #     Flag indicating whether the game is won.
    # game_lose : bool
    #     Flag indicating whether the game is lost.
    # mine_lose : bool
    #     Flag indicating whether the game is lost due to stepping on mines.
    # move_count : int
    #     Counter for the number of moves made.
    # last_revealed : tuple
    #     Coordinates of the last revealed cell.
    # current_word : str
    #     The current word being revealed.
    # score : int
    #     The player's score.
    # base_penalty_random : int
    #     Base penalty for random clicks.
    # random_click_counter : int
    #     Counter for the number of random clicks.
    # mine_stepped_counter : int
    #     Counter for the number of mines stepped on.
    # random_click_cap : int
    #     Cap for the number of random clicks allowed.
    # user_stats : dict
    #     Dictionary containing the user's statistics.
    # Methods:
    # --------
    # load_words():
    #     Loads words and their complexity from a file.
    # load_user_stats():
    #     Loads user statistics from a file.
    # save_user_stats():
    #     Saves user statistics to a file.
    # fill_board():
    #     Fills the game board with words, mines, and hints.
    # calculate_mine_hint(row, col):
    #     Calculates the mine hint for a given cell.
    # calculate_letter_hint(row, col):
    #     Calculates the letter hint for a given cell.
    # display_user_info():
    #     Displays user information on the screen.
    # draw_board():
    #     Draws the game board on the screen.
    # calculate_base_score(word):
    #     Calculates the base score for a given word.
    # calculate_clean_reveal_bonus(clean_reveal, word):
    #     Calculates the bonus score for a clean reveal of a word.
    # calculate_total_score(word, clean_reveal):
    #     Calculates the total score for revealing a word.
    # check_revealed_words():
    #     Checks if any words have been fully revealed.
    # check_if_mine_stepped_lost():
    #     Checks if the game is lost due to stepping on too many mines.
    # adjust_random_click_cap():
    #     Adjusts the cap for the number of random clicks allowed.
    # award_bonus_points():
    #     Awards bonus points based on the number of words left and random clicks.
    # penalty_multiplier(random_click_counter, cap_value):
    #     Calculates the penalty multiplier for random clicks.
    # get_word_cells(word):
    #     Gets the coordinates of the cells containing a given word.
    # check_word_revealed(row, col, word, direction):
    #     Checks if a word is fully revealed starting from a given cell.
    # check_all_words_revealed():
    #     Checks if all selected words have been revealed.
    # check_window_size():
    #     Checks if the terminal window size is sufficient for the game.
    # update_stats(game_won, game_lose):
    #     Updates the user's statistics based on the game result.
    # run():
    #     Runs the main game loop.

    def __init__(self, stdscr, user, size=7):
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
        self.game_lose = False
        self.mine_lose = False
        self.move_count = 0  # Initialize move counter
        self.last_revealed = None  # Track the last revealed cell
        self.current_word = None  # Track the current word being revealed
        self.score = 0  # Initialize score
        self.base_penalty_random = 0
        self.random_click_counter = 0
        self.mine_stepped_counter = 0
        self.random_click_cap = 5  # Initial cap for random clicks
        self.user_stats = self.load_user_stats()

    def load_words(self):

        # Loads words and their complexities from a file.
        # 
        # The method reads a file named 'words.txt' located in the './data/' directory.
        # Each line in the file should contain a word and its complexity separated by a comma.
        # The method returns a list of words and a dictionary mapping each word to its complexity.
        # 
        # Returns:
        #     tuple: A tuple containing:
        #         - list: A list of words.
        #         - dict: A dictionary where keys are words and values are their complexities.

        words = []
        word_complexity = {}
        with open('./data/words.txt', 'r') as file:
            for line in file:
                word, complexity = line.strip().split(',')
                words.append(word)
                word_complexity[word] = int(complexity)
        return words, word_complexity

    def load_user_stats(self):

        # Load the user's statistics from a file.
        # 
        # This method reads the user's statistics from a file located at './data/user.txt'.
        # It checks if the file exists and reads its contents line by line. If a line matches
        # the user's ID and contains the correct number of fields, it parses the statistics
        # and returns them as a dictionary.
        # 
        # Returns:
        #     dict: A dictionary containing the user's statistics with the following keys:
        #     - 'games_played' (int): The number of games played by the user.
        #     - 'games_won' (int): The number of games won by the user.
        #     - 'words_revealed' (int): The number of words revealed by the user.
        #     - 'longest_word_revealed' (str): The longest word revealed by the user.
        #     - 'mines_stepped' (int): The number of mines stepped on by the user.
        #     - 'highest_score_classic' (int): The highest score achieved by the user in classic mode.
        #     - 'highest_score_timed' (int): The highest score achieved by the user in timed mode.
        #     - 'average_steps_used' (float): The average number of steps used by the user.
        #     - 'min_steps_used' (int): The minimum number of steps used by the user.
        #     - 'max_steps_used' (int): The maximum number of steps used by the user.

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

        # Saves the user's statistics to a file.
        # 
        # If the file './data/user.txt' exists, it reads the file and updates the
        # user's statistics if the user ID matches. If the file does not exist, it
        # creates a new file and writes the user's statistics.
        # 
        # The statistics include:
        # - games_played: Number of games played by the user.
        # - games_won: Number of games won by the user.
        # - words_revealed: Number of words revealed by the user.
        # - longest_word_revealed: The longest word revealed by the user.
        # - mines_stepped: Number of mines stepped on by the user.
        # - highest_score_classic: The highest score achieved by the user in classic mode.
        # - highest_score_timed: The highest score achieved by the user in timed mode.
        # - average_steps_used: The average number of steps used by the user.
        # - min_steps_used: The minimum number of steps used by the user.
        # - max_steps_used: The maximum number of steps used by the user.
        # 
        # The statistics are stored in a comma-separated format in the file.

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

        # Fills the game board with words, mines, and hints.
        # This method performs the following steps:
        #
        # 1. Resets the board and related variables.
        # 2. Filters out words longer than the board size.
        # 3. Randomly selects 3 words to place on the board.
        # 4. Initializes the reveal status for each selected word.
        # 5. Randomly places the selected words on the board either horizontally or vertically.
        # 6. Randomly fills some of the remaining empty cells with common letters.
        # 7. Generates a list of all possible positions for placing mines.
        # 8. Randomly places a specified number of mines on the board.
        # 9. Calculates mine hints for each cell.
        # 10. Calculates letter hints for each empty cell.
        #
        # Attributes:
        #     board (list): 2D list representing the game board.
        #     covered (list): 2D list indicating whether each cell is covered.
        #     mine_hints (list): 2D list containing mine hints for each cell.
        #     letter_hints (list): 2D list containing letter hints for each cell.
        #     flagged (list): 2D list indicating whether each cell is flagged.
        #     selected_words (list): List of words selected to be placed on the board.
        #     revealed_words (set): Set of words that have been revealed.
        #     word_reveal_status (dict): Dictionary tracking the reveal status of each word.
        #     move_count (int): Counter for the number of moves made.
        #     last_revealed (tuple): Coordinates of the last revealed cell.
        #     current_word (str): The current word being revealed.
        #     score (int): The player's score.

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

        # Randomly select 3 words to place on the board
        self.selected_words = random.sample(valid_words, 3)

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
                if self.board[i][j] == ' ' and random.random() < 0.15:  # Chance to fill the cell
                                                                        # Reduce this value to increase the number of empty cells
                    # Avoid using letters that are already placed in words
                    available_letters = [letter for letter in self.common_letters if letter not in placed_letters]
                    self.board[i][j] = random.choice(available_letters)  # Randomly choose a common letter

        # Generate a list of all possible positions
        possible_positions = [(i, j) for i in range(1, self.size - 1) for j in range(1, self.size - 1) if self.board[i][j] == ' ']

        # Randomly shuffle the list of possible positions
        random.shuffle(possible_positions)

        # Ensure there are enough positions to place mines
        num_mines = 6
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

        # Calculate the hint for the number of mines around a given cell in the board.
        # This function checks all 8 possible directions around the given cell (row, col)
        # to determine the presence of mines. It then generates a hint based on the 
        # configuration of the mines around the cell. The hint is represented using 
        # Braille patterns to indicate the positions of the mines.
        #
        # Args:
        #     row (int): The row index of the cell.
        #     col (int): The column index of the cell.
        #
        # Returns:
        #     list: A list of two characters representing the hint for the cell. Each 
        #           character is a Braille pattern indicating the presence of mines 
        #           around the cell.

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

        # If corner and top / bottom
        if top_left and bottom and hint[0] != '⡁':
            hint[0] = '⡁'
        if top_right and bottom and hint[1] != '⢈':
            hint[1] = '⢈'
        if bottom_left and top and hint[0] != '⡁':
            hint[0] = '⡁'
        if bottom_right and top and hint[1] != '⢈':
            hint[1] = '⢈'

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

        # Calculate the hint for a given cell in the puzzle game.
        # 
        # This method counts how many times the character in the specified cell
        # (row, col) appears in any of the selected words within the surrounding
        # 3x3 grid. The count is returned as a string. If the count is zero, a 
        # space character is returned instead.
        # 
        # Args:
        #     row (int): The row index of the cell.
        #     col (int): The column index of the cell.
        # 
        # Returns:
        #     str: The count of occurrences as a string, or a space if the count is zero.

        count = 0
        for i in range(max(0, row - 1), min(self.size, row + 2)):
            for j in range(max(0, col - 1), min(self.size, col + 2)):
                # Check if the character is part of any selected word
                if any(self.board[i][j] in word for word in self.selected_words):
                    count += 1
        return str(count) if count > 0 else ' '  # Return the count as a string, or a space if count is 0

    def display_user_info(self):

        # Displays the user's information in a separate window on the screen.
        # 
        # This method creates a new window using the curses library and displays
        # the player's ID, highest score in classic mode, number of games won, 
        # and win rate. The window is positioned at the top right corner of the 
        # screen.
        # 
        # The displayed information includes:
        # - Player ID
        # - Highest Score in Classic Mode
        # - Number of Games Won
        # - Win Rate (calculated as the percentage of games won out of games played)
        # 
        # The window is bordered and the text is formatted with some bold attributes.
        # 
        # Note:
        #     This method assumes that `self.stdscr` is a valid curses window object,
        #     `self.user` has an attribute `user_id`, and `self.user_stats` is a 
        #     dictionary containing the keys 'highest_score_classic', 'games_won', 
        #     and 'games_played'.
        # 

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

        # Draws the game board and various game-related information on the screen.
        # This method clears the screen and redraws the game board, hints, move counter,
        # score, mine stepped counter, and any game messages (win/lose). It uses the 
        # curses library to handle screen drawing.
        #
        # The board is drawn with cells that can be covered, flagged, questioned, or revealed.
        # The hints, move counter, score, and mine stepped counter are displayed on the left-hand side.
        # If the game is won or lost, appropriate messages are displayed.
        #
        # Attributes:
        #     self.stdscr (curses.window): The window object where the game is drawn.
        #     self.size (int): The size of the game board.
        #     self.selected_words (list): List of words to be found in the game.
        #     self.revealed_words (list): List of words that have been found.
        #     self.mine_stepped_counter (int): Counter for the number of mines stepped on.
        #     self.move_count (int): Counter for the number of moves made.
        #     self.score (int): The current score of the player.
        #     self.covered (list): 2D list indicating whether each cell is covered.
        #     self.flagged (list): 2D list indicating whether each cell is flagged.
        #     self.questioned (list): 2D list indicating whether each cell is questioned.
        #     self.mine_hints (list): 2D list of mine hints for each cell.
        #     self.letter_hints (list): 2D list of letter hints for each cell.
        #     self.board (list): 2D list representing the game board.
        #     self.exit_prompt (bool): Flag indicating whether the exit prompt is shown.
        #     self.game_won (bool): Flag indicating whether the game is won.
        #     self.game_lose (bool): Flag indicating whether the game is lost.
        #     self.mine_lose (bool): Flag indicating whether the game is lost due to stepping on mines.
        #
        # Returns:
        #     None

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

        # Display mine stepped counter
        self.stdscr.addstr(hint_start_y + len(self.selected_words) + 5, 2, "Mine stepped:")
        mine_display = ""
        for i in range(3):
            if i < self.mine_stepped_counter:
                mine_display += "✱ "
            else:
                mine_display += "_ "
        self.stdscr.addstr(hint_start_y + len(self.selected_words) + 6, 2, mine_display.strip())

        # Draw move counter below the hint section
        self.stdscr.addstr(hint_start_y + len(self.selected_words) + 2, 2, f"Moves: {self.move_count}")

        # Draw score below the move counter
        self.stdscr.addstr(hint_start_y + len(self.selected_words) + 3, 2, f"Score: {self.score}")

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
        if self.game_won and not self.game_lose:
            win_msg_y = h // 2 - 2
            self.stdscr.addstr(win_msg_y, w - 30, "Congratulations!")
            self.stdscr.addstr(win_msg_y + 1, w - 30, "You found all the words!")
            self.stdscr.addstr(win_msg_y + 3, w - 30, "Press N for New Game")

        # Draw the losing message if the game is lost
        if self.game_lose and not self.mine_lose:
            lose_msg_y = h // 2 - 2
            self.stdscr.addstr(lose_msg_y, w - 40, "Game Over!")
            self.stdscr.addstr(lose_msg_y + 1, w - 40, "Negative score? Better luck next time!")
            self.stdscr.addstr(lose_msg_y + 3, w - 40, "Press N for New Game")

        if self.mine_lose:
            lose_msg_y = h // 2 - 2
            self.stdscr.addstr(lose_msg_y, w - 40, "Game Over!")
            self.stdscr.addstr(lose_msg_y + 1, w - 40, "Stepped on too many mines!")
            self.stdscr.addstr(lose_msg_y + 3, w - 40, "Press N for New Game")

        self.stdscr.refresh()

    def calculate_base_score(self, word):

        # Calculate the base score for a given word.
        # 
        # The base score is determined by the length of the word and its complexity.
        # The complexity of the word is retrieved from the `word_complexity` dictionary.
        # If the word is not found in the dictionary, a default complexity of 1 is used.
        # 
        # Args:
        #     word (str): The word for which to calculate the base score.
        # 
        # Returns:
        #     int: The calculated base score for the word.

        word_length = len(word)
        word_complexity = self.word_complexity.get(word, 1)
        base_score = word_length * word_complexity
        return base_score

    def calculate_clean_reveal_bonus(self, clean_reveal, word):

        # Calculate the bonus score for a clean reveal of a word.
        # 
        # A clean reveal is when the word is revealed without any mistakes.
        # The bonus score is calculated based on the length of the word and its complexity.
        # 
        # Args:
        #     clean_reveal (bool): A flag indicating if the word was revealed cleanly.
        #     word (str): The word that was revealed.
        # 
        # Returns:
        #     int: The bonus score for the clean reveal.

        bonus_score = 0
        if clean_reveal:
            word_length = len(word)
            word_complexity = self.word_complexity.get(word, 1)
            bonus_score = 10 + word_length * word_complexity  # Example bonus for clean reveal
        return bonus_score

    def calculate_total_score(self, word, clean_reveal):

        # Calculate the total score for a given word based on its length, complexity, and whether it was revealed cleanly.
        # 
        # Args:
        #     word (str): The word for which the score is being calculated.
        #     clean_reveal (bool): A flag indicating if the word was revealed cleanly.
        # 
        # Returns:
        #     int: The total score for the given word.

        word_length = len(word)
        word_complexity = self.word_complexity.get(word, 1)
        base_score = word_length * word_complexity * 100  # Base score for each word
        clean_bonus = 0
        if clean_reveal:
            clean_bonus = (word_length * word_complexity * 50)  # Clean reveal bonus
        total_score = base_score + clean_bonus
        return total_score

    def check_revealed_words(self):

        # Checks if any of the selected words have been completely revealed on the board.
        # 
        # For each word in the selected words list, the method iterates through the board to find the starting 
        # letter of the word. If the starting letter is found, it checks if the word is revealed either 
        # horizontally ('H') or vertically ('V'). If the word is revealed and not already in the revealed words 
        # set, it performs the following actions:
        # 
        # - Verifies if the word is cleanly revealed (all cells of the word are in the word reveal status).
        # - Adds the word to the revealed words set.
        # - Resets the word reveal status for the word.
        # - Resets the current word.
        # - Increases the score based on the total score calculation for the word and whether it was cleanly revealed.
        # - Adjusts the random click cap.
        # - Awards bonus points.

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

    def check_if_mine_stepped_lost(self):

        # Checks if the player has stepped on a mine three times and updates the game state accordingly.
        # 
        # If the player has stepped on a mine three times, the game is marked as lost, 
        # the mine lose condition is set to True, and the game won condition is set to False.
        # 
        # Returns:
        #     bool: True if the player has stepped on a mine three times, otherwise False.

        if self.mine_stepped_counter == 3:
            self.game_lose = True
            self.mine_lose = True
            self.game_won = False
            return True

    def adjust_random_click_cap(self):

        # Adjusts the cap for random clicks based on the number of words left to be revealed.
        # 
        # This method updates the `random_click_cap` and potentially the `random_click_counter`
        # based on the number of words left to be revealed in the game. The cap and counter
        # are adjusted in three stages:
        # 
        # - Stage 1: When there are 3 words left, the random click cap is set to 10.
        # - Stage 2: When there are 2 words left, the random click cap is reduced to 9, and the
        #   random click counter is decreased by up to 5, but not below 0.
        # - Stage 3: When there is 1 word left, the random click cap is reduced to 7, and the
        #   random click counter is decreased by up to 3, but not below 0.

        words_left = len(self.selected_words) - len(self.revealed_words)
        if words_left == 3:
            self.random_click_cap = 10  # Stage 1 cap for random clicks
        elif words_left == 2:
            self.random_click_cap = 9  # Reduce Stage 2 cap for random clicks
            self.random_click_counter = max(0, self.random_click_counter - 5)
        elif words_left == 1:
            self.random_click_cap = 7  # Stage 3 cap for random clicks
            self.random_click_counter = max(0, self.random_click_counter - 3)

    def award_bonus_points(self):

        # Awards bonus points based on the number of words left to be revealed and the number of random clicks made.
        # 
        # The bonus points are awarded as follows:
        # - If 3 words are left and the random click counter is within the cap, 800 points multiplied by the remaining allowed clicks are added to the score.
        # - If 2 words are left and the random click counter is within the cap, 1200 points multiplied by the remaining allowed clicks are added to the score.
        # - If 1 word is left and the random click counter is within the cap, 1700 points multiplied by the remaining allowed clicks are added to the score.
        # 
        # The remaining allowed clicks are calculated as the difference between the random click cap and the current random click counter, with a minimum multiplier of 1.
        # 
        # Returns:
        #     None

        words_left = len(self.selected_words) - len(self.revealed_words)
        if words_left == 3 and self.random_click_counter <= self.random_click_cap:
            self.score += 800 * max(1, (self.random_click_cap - self.random_click_counter))  # Stage 1 bonus points
        elif words_left == 2 and self.random_click_counter <= self.random_click_cap:
            self.score += 1200 * max(1, (self.random_click_cap - self.random_click_counter)) # Stage 2 bonus points
        elif words_left == 1 and self.random_click_counter <= self.random_click_cap:
            self.score += 1700 * max(1, (self.random_click_cap - self.random_click_counter)) # Stage 3 bonus points

    def penalty_multiplier(self, random_click_counter, cap_value):

        # Calculate the penalty multiplier based on the number of random clicks.
        # The penalty multiplier is determined using an exponential function and a linear function
        # depending on the value of random_click_counter relative to cap_value.
        #
        # Explanation of this formula can be found at https://github.com/NaughtyChas/Wordweeper/pull/17#issuecomment-2468165644
        #
        # Parameters:
        # - random_click_counter (int): The number of random clicks made by the user.
        # - cap_value (int): The threshold value for determining the penalty.
        #
        # Returns:
        # - float: The calculated penalty multiplier.

        k = 0.01
        
        if random_click_counter <= (cap_value - 2):
            return (math.exp(k * (random_click_counter - cap_value)) - 0.6)
        elif (cap_value - 2) < random_click_counter <= cap_value:
            return (random_click_counter - (cap_value - 2)) / 2
        else:
            return math.exp(k * (random_click_counter - cap_value))


    def get_word_cells(self, word):

        # Find the cells on the board that contain the given word.
        # 
        # This method searches the board for the starting letter of the word and 
        # checks if the word can be revealed horizontally ('H') or vertically ('V') 
        # from that position. If the word is found, it collects the coordinates of 
        # the cells that contain the word.
        # 
        # Args:
        #     word (str): The word to search for on the board.
        # 
        # Returns:
        #     list of tuple: A list of tuples where each tuple represents the 
        #            coordinates (i, j) of a cell that contains part of the word.

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

        # Check if a word is fully revealed on the board in the specified direction.
        # 
        # Args:
        #     row (int): The starting row index of the word.
        #     col (int): The starting column index of the word.
        #     word (str): The word to check.
        #     direction (str): The direction of the word ('H' for horizontal, 'V' for vertical).
        # 
        # Returns:
        #     bool: True if the word is fully revealed, False otherwise.

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

        # Checks if all selected words have been revealed and updates the game state accordingly.
        # If all revealed but the score is negative, game_lose is set to True and game_won is set to False.
        # If all words are revealed with a positive score, game_won is set to True and game_lose is set to False.
        # 
        # Returns:
        #     bool: True if all selected words are revealed, otherwise False.

        all_revealed = all(word in self.revealed_words for word in self.selected_words)
        if all_revealed and self.score < 0:
            self.game_won = False
            self.game_lose = True
            return True
        elif all_revealed:
            self.game_won = True
            self.game_lose = False
            return True
        return False

    def check_window_size(self):

        # Checks if the terminal window size meets the minimum requirements.
        # This method retrieves the current terminal window size and compares it
        # against the minimum required dimensions (25 rows by 142 columns). If the
        # terminal window is too small, it displays a message prompting the user to
        # increase the window size and waits for user input before returning.
        #
        # Returns:
        #     bool: True if the terminal window size meets the minimum requirements,
        #           False otherwise.

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

    def update_stats(self, game_won, game_lose):

        # Updates the user's game statistics.
        # 
        # This method increments the number of games played, updates the number of games won if applicable,
        # and checks if the current score is higher than the recorded highest score for classic mode. 
        # If so, it updates the highest score. Finally, it saves the updated statistics.
        # 
        # Args:
        #     game_won (bool): Indicates if the game was won.
        #     game_lose (bool): Indicates if the game was lost.

        self.user_stats['games_played'] += 1
        if game_won and not game_lose:
            self.user_stats['games_won'] += 1
        if self.score > self.user_stats['highest_score_classic']:
            self.user_stats['highest_score_classic'] = self.score
        self.save_user_stats()

    def run(self):

        # Main game loop for the classic easy mode of the puzzle game.
        # This method handles the game logic, user input, and game state updates. It continuously checks the window size,
        # processes user inputs (keyboard and mouse), updates the game board, and manages the game state (win/lose conditions).
        # The loop continues until the user decides to exit the game by pressing the ESC key or 'q' key after winning.
        #
        # Key functionalities:
        # - Checks window size and redraws the board if necessary.
        # - Handles user inputs including ESC key for exit, 'n' key for new game, and mouse clicks for revealing cells.
        # - Updates game state based on user actions, including revealing cells, flagging cells, and checking for win/lose conditions.
        # - Calculates and applies penalties for revealing mines and random clicks.
        # - Updates and displays user information and game statistics.
        #
        # Returns:
        #     None

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
                            self.update_stats(self.game_won, self.game_lose)
                        curses.endwin()
                        return
                    else:
                        self.exit_prompt = True
                        self.draw_board()
                elif key == ord('n') and self.game_lose:
                    self.__init__(self.stdscr, self.user, self.size)
                    self.run()
                elif key == ord('n') and self.game_won:
                    self.__init__(self.stdscr, self.user, self.size)
                    self.run()
                elif self.game_lose and not self.game_won:
                    self.stdscr.refresh()
                elif self.check_all_words_revealed() and not self.game_lose:
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

                            # Instead of write mine penalty into a function, I've wrote it here.
                            # This is because the penalty is only applied when a mine is revealed.
                            # The penalty is calculated based on the number of revealed cells and the total number of cells.
                            # You can find more explanation about the punishment algorithm at:
                            # https://github.com/NaughtyChas/Wordweeper/pull/17#issuecomment-2467928859
                            
                            if self.board[cell_y][cell_x] == '✱':
                                self.mine_stepped_counter += 1
                                revealed_cells = sum(not self.covered[i][j] for i in range(self.size) for j in range(self.size))
                                total_cells = self.size * self.size
                                base_penalty = 1000
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

                                # Check if the revealed cell is part of a selected word,
                                # and apply the appropriate base penalty for random clicks.
                                
                                if (not is_part_of_word) or (is_part_of_word and self.random_click_counter == 0):
                                    self.random_click_counter += 1
                                    words_left = len(self.selected_words) - len(self.revealed_words)
                                    if words_left == 3:
                                        self.base_penalty_random = 700  # Penalty for random clicks
                                    elif words_left == 2:
                                        self.base_penalty_random = 1100  # Penalty for random clicks
                                    elif words_left == 1:
                                        self.base_penalty_random = 1500  # Penalty for random clicks
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
                                self.update_stats(self.game_won, self.game_lose)
                                self.draw_board()

                # Check if the player has stepped on a mine three times,
                # If so, the game is lost and the game will end.

                if self.check_if_mine_stepped_lost() and not self.game_won:
                    self.draw_board()
                    self.stdscr.refresh()
                elif key == ord('q') and self.game_won:
                    curses.endwin()
                    break
                else:
                    self.draw_board()

if __name__ == "__main__":
    curses.wrapper(Board)