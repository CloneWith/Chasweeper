# This module provides a text-based menu interface for a puzzle game using the curses library.
# It includes functionality for user registration, game difficulty selection, and viewing user statistics.
# Classes:
#     Menu: Represents the main menu interface for the puzzle game.
# Functions:
#     __init__(self, stdscr): Initializes the menu with the given stdscr object.
#     load_users(self): Loads user data from a file and returns a list of User objects.
#     check_window_size(self): Checks if the terminal window size meets the minimum requirements.
#     print_menu(self, menu): Prints the given menu to the screen.
#     handle_enter(self): Handles the Enter key being pressed while navigating the menu.
#     start_game(self): Handles game starting logic.
#     start_game_with_difficulty(self, difficulty): Starts a new game with the given difficulty.
#     register(self): Opens a registration prompt to the user.
#     view_statistics(self): Shows the statistics of all users and allows the user to select a user to view their statistics.
#     run(self): Runs the main loop of the menu interface.
# Attributes:
#     stdscr: The curses window object.
#     current_row: The current row of the menu.
#     current_menu: The current menu being displayed.
#     current_user: The current user logged in.
#     users: A list of User objects.
#     menus: A dictionary of menu items, keyed by menu name.
#     descriptions: A dictionary of descriptions for each menu item.
#     ascii_art: A list of strings that form the ASCII art for the menu.

import curses
import os
import re
from util import diffcalc
from game.classicEasy import Board as EasyBoard
from game.classicHard import Board as HardBoard
from game.classicExpert import Board as ExpertBoard
from util.user import User
from util.user_statistics import UserStatistics


class Menu:
    def __init__(self, stdscr):
        
        # Initialize the menu with the given stdscr object.
        #
        # Args:
        #     stdscr: A curses window object
        #
        # Attributes:
        #     stdscr: The curses window object
        #     current_row: The current row of the menu
        #     current_menu: The current menu being displayed
        #     current_user: The current user logged in
        #     users: A list of User objects
        #     menus: A dictionary of menu items, keyed by menu name
        #     descriptions: A dictionary of descriptions for each menu item
        #     ascii_art: A list of strings that form the ASCII art for the menu

        self.stdscr = stdscr
        self.current_row = 0
        self.current_menu = "main"
        self.current_user = None
        self.users = self.load_users()
        self.menus = {
            "main": ["Start Game", "View Statistics", "Exit Game"],
            "start_game": [],
            "user_menu": ["Start Game", "View Statistics", "Logout", "Exit Game"],
            "classic_mode": ["Easy", "Hard", "Expert", "Back"]
        }
        self.descriptions = {
            "Start Game": "* Play some Wordweeper!",
            "View Statistics": "* Check data and statistics",
            "Exit Game": "* Exit the game",
            "Classic Mode": "* Play the classic mode",
            "Back": "* Go back to the previous menu",
            "Easy": "* Easy difficulty",
            "Hard": "* Hard difficulty",
            "Expert": "* Expert difficulty",
            "New player? Click here to register!": "* Register a new player",
            "Click here or press 'Enter' to register!": "* Register a new player",
            "Logout": "* Log out of your account"
        }
        self.ascii_art = [
            "  __          __           _                                   ",
            "  \\ \\        / /          | |                                  ",
            "   \\ \\  /\\  / /__  _ __ __| |_      _____  ___ _ __   ___ _ __ ",
            "    \\ \\/  \\/ / _ \\| '__/ _` \\ \\ /\\ / / _ \\/ _ \\ '_ \\ / _ \\ '__|",
            "     \\  /\\  / (_) | | | (_| |\\ V  V /  __/  __/ |_) |  __/ |   ",
            "      \\/  \\/ \\___/|_|  \\__,_| \\_/\\_/ \\___|\\___| .__/ \\___|_|   ",
            "                                              | |                ",
            "                                              |_|                "
        ]

    def load_users(self):

    # Loads user data from a file and returns a list of User objects.
    #
    # This function checks if the 'user.txt' file exists in the './data/' directory.
    # If the file exists, it reads user data from the file, where each line represents
    # a user and contains 11 comma-separated fields. It creates a User object for each
    # line with the correct number of fields and appends it to a list.
    # 
    # Returns:
    #     list: A list of User objects created from the data in 'user.txt'.

        users = []
        if os.path.exists('./data/user.txt'):
            with open('./data/user.txt', 'r') as file:
                for line in file:
                    data = line.strip().split(',')
                    if len(data) == 11:  # Ensure the correct number of fields
                        user = User(data[0], int(data[1]), int(data[2]), int(data[3]), data[4], int(data[5]), int(data[6]), int(data[7]), float(data[8]), int(data[9]), int(data[10]))
                        users.append(user)
        return users

    def check_window_size(self):

    # Checks if the terminal window size meets the minimum requirements.
    #
    # This function retrieves the current dimensions of the terminal window and
    # compares them against a predefined minimum height and width. If the window
    # is too small, a message is displayed prompting the user to increase the
    # window size. The function waits for user input before returning.
    #
    # Returns:
    #     bool: True if the window size is adequate, False otherwise.

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

    def print_menu(self, menu):

        # Prints the given menu to the screen.
        #
        # Args:
        #     menu (list): A list of strings, where each string is a menu item.

        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        menu_start_y = (h - len(self.ascii_art) - len([item for item in menu if item != ""])) // 2 + len(self.ascii_art)
        for idx, row in enumerate(self.ascii_art):
            self.stdscr.addstr(idx, (w - len(row)) // 2, row)
        for idx, row in enumerate(menu):
            if row == "":
                continue  # Skip empty lines for spacing
            x = 2  # Align menu items to the left
            y = menu_start_y + idx
            if idx == self.current_row:
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(y, x, row)
                self.stdscr.attroff(curses.color_pair(1))
                # Display description on the right side of the screen
                if row in self.descriptions:
                    self.stdscr.addstr(y, w - len(self.descriptions[row]) - 2, self.descriptions[row])
            else:
                self.stdscr.addstr(y, x, row)
        # Display logged in user on the top right corner
        if self.current_user:
            login_message = f"Logged in as {self.current_user.user_id}"
            self.stdscr.addstr(0, w - len(login_message) - 2, login_message)
        self.stdscr.refresh()

    def handle_enter(self):

        # Handles the Enter key being pressed while navigating the menu.
        #
        # Checks the currently selected menu item and performs the appropriate action.

        menu = self.menus[self.current_menu]
        if self.current_menu == "main":
            if menu[self.current_row] == "Start Game":
                diffcalc.update_words_file() # Calculate word complexity when starting the game
                self.start_game()
            elif menu[self.current_row] == "View Statistics":
                self.view_statistics()
            elif menu[self.current_row] == "Exit Game":
                exit()
        elif self.current_menu == "start_game":
            if menu[self.current_row] == "New player? Click here to register!" or menu[self.current_row] == "Click here or press 'Enter' to register!":
                self.current_menu = "register"
                self.register()
            elif self.current_row < len(self.users):
                self.current_user = self.users[self.current_row]
                self.current_menu = "user_menu"
                self.current_row = 0
        elif self.current_menu == "register":
            self.register()
        elif self.current_menu == "user_menu":
            if menu[self.current_row] == "Start Game":
                self.current_menu = "classic_mode"
                self.current_row = 0
            elif menu[self.current_row] == "View Statistics":
                self.view_statistics()
            elif menu[self.current_row] == "Logout":
                self.current_user = None
                self.current_menu = "main"
                self.current_row = 0
            elif menu[self.current_row] == "Exit Game":
                exit()
        elif self.current_menu == "classic_mode":
            if menu[self.current_row] == "Easy":
                self.start_game_with_difficulty("Easy")
            elif menu[self.current_row] == "Hard":
                self.start_game_with_difficulty("Hard")
            elif menu[self.current_row] == "Expert":
                self.start_game_with_difficulty("Expert")
            elif menu[self.current_row] == "Back":
                self.current_menu = "user_menu"
                self.current_row = 0

    def start_game(self):

        # Handle game starting logic
        #
        # If the user is not logged in, shows the user selection menu. If the user is logged in, shows the classic mode selection menu.

        if self.current_user is None:
            if not self.users:
                self.menus["start_game"] = ["Click here or press 'Enter' to register!"]
            else:
                self.menus["start_game"] = [user.user_id for user in self.users] + ["New player? Click here to register!"]
            self.current_menu = "start_game"
        else:
            self.current_menu = "classic_mode"
        self.current_row = 0

    def start_game_with_difficulty(self, difficulty):

        # Starts a new game with the given difficulty.
        # 
        # param difficulty: The difficulty of the game. Can be "Easy", "Hard", or "Expert".
        # type difficulty: str

        if difficulty == "Easy":
            board = EasyBoard(self.stdscr, self.current_user, size=7)
        elif difficulty == "Hard":
            board = HardBoard(self.stdscr, self.current_user, size=10)
        elif difficulty == "Expert":
            # Assuming Expert mode uses HardBoard with a larger size
            board = ExpertBoard(self.stdscr, self.current_user, size=12)
        board.run()

    def register(self):

        # Opens a registration prompt to the user. The user can enter a username,
        # and the function will validate the username and register the user if
        # the username is valid. The function will continue to prompt the user
        # until a valid username is entered.
        # 
        # return: None

        while True:
            self.stdscr.clear()
            self.stdscr.addstr(13, 10, "Enter user ID (Press ESC to cancel): ")
            curses.echo()
            user_id = ""
            while True:
                key = self.stdscr.getch()
                if key == 27:  # ESC key
                    self.current_menu = "main"
                    self.current_row = 0
                    return
                elif key in [10, 13]:  # Enter key
                    break
                else:
                    user_id += chr(key)
                    self.stdscr.addstr(13, 10 + len("Enter user ID (Press ESC to cancel): "), user_id)
                    self.stdscr.refresh()
            curses.noecho()

            # Validate username
            if len(user_id) > 16:
                self.stdscr.addstr(14, 10, "Username cannot be longer than 16 characters. Press any key to re-enter username.")
                self.stdscr.getch()
                continue
            if not re.match(r'^[A-Za-z0-9 _-]+$', user_id):
                self.stdscr.addstr(14, 10, "Username can only contain letters, numbers, spaces, underscores, and hyphens. Press any key to re-enter username.")
                self.stdscr.getch()
                continue
            if user_id[0] == ' ' or user_id[-1] == ' ':
                self.stdscr.addstr(14, 10, "Username cannot start or end with a space. Press any key to re-enter username.")
                self.stdscr.getch()
                continue
            if not re.match(r'^[A-Za-z0-9 _-]+$', user_id):
                self.stdscr.addstr(14, 10, "Username can only contain letters, numbers, spaces, underscores, and hyphens. Press any key to re-enter username.")
                self.stdscr.getch()
                continue

            if User.load_from_file(user_id):
                self.stdscr.addstr(14, 10, "User ID already exists. Press any key to re-enter username.")
                self.stdscr.getch()
                continue
            else:
                user = User(user_id)
                user.save_to_file()
                self.users.append(user)
                self.stdscr.addstr(14, 10, "Registration successful. Press any key to continue.")
                self.stdscr.getch()
                break
        self.current_menu = "main"
        self.current_row = 0

    def view_statistics(self):

        # Shows the statistics of all users and allows the user to select a user to view their statistics.
        # 
        # :return: None

        stats = UserStatistics(self.stdscr)
        stats.display()
        self.current_menu = "main"
        self.current_row = 0

    def run(self):

        # Runs the main loop of the menu interface.
        # This method initializes the curses settings, handles user input, and updates the menu display accordingly.
        # It supports navigation through the menu using arrow keys, mouse clicks, and the Enter key to select options.
        # The ESC key is used to navigate back to the main menu or exit the application.
        # The method performs the following actions:
        # - Disables the cursor.
        # - Initializes color pairs for the menu display.
        # - Sets up mouse event handling.
        # - Continuously checks for user input and updates the menu state.
        # Key bindings:
        # - Up arrow: Move the selection up.
        # - Down arrow: Move the selection down.
        # - Enter: Select the current menu item.
        # - ESC: Navigate back or exit the application.
        # - Mouse click: Select the menu item under the cursor.
        # Returns:
        #     None

        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
        while True:
            if not self.check_window_size():
                continue
            self.print_menu(self.menus[self.current_menu])
            key = self.stdscr.getch()
            if key == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
            elif key == curses.KEY_DOWN and self.current_row < len(self.menus[self.current_menu]) - 1:
                self.current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.handle_enter()
            elif key == 27:  # ESC key
                if self.current_menu == "main":
                    exit()
                elif self.current_menu == "start_game" or self.current_menu == "register":
                    self.current_menu = "main"
                    self.current_row = 0
                elif self.current_menu == "user_menu":
                    self.current_menu = "main"
                    self.current_row = 0
            elif key == curses.KEY_MOUSE:
                _, mx, my, _, _ = curses.getmouse()
                h, w = self.stdscr.getmaxyx()
                menu_start_y = (h - len(self.ascii_art) - len([item for item in self.menus[self.current_menu] if item != ""])) // 2 + len(self.ascii_art)
                for idx, row in enumerate(self.menus[self.current_menu]):
                    if row == "":
                        continue  # Skip empty lines for spacing
                    x = 2  # Align menu items to the left
                    y = menu_start_y + idx
                    if y == my:
                        self.current_row = idx
                        self.handle_enter()
                        break

if __name__ == "__main__":
    curses.wrapper(Menu)