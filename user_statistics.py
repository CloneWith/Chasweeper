import curses
import os
from user import User

class UserStatistics:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.users = self.load_users()
        self.current_user = None

    def load_users(self):
        users = []
        if os.path.exists('./data/user.txt'):
            with open('./data/user.txt', 'r') as file:
                for line in file:
                    data = line.strip().split(',')
                    user = User(data[0], int(data[1]), int(data[2]), int(data[3]), data[4], int(data[5]), int(data[6]), int(data[7]), float(data[8]), int(data[9]), int(data[10]))
                    users.append(user)
        return users

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
            while True:
                key = size_prompt.getch()
                if key == curses.KEY_RESIZE:
                    h, w = self.stdscr.getmaxyx()
                    if h >= min_height and w >= min_width:
                        break
            return False
        return True

    def display(self):
        while True:
            if not self.check_window_size():
                continue
            if self.current_user is None:
                if not self.select_user():
                    break  # Exit the loop if ESC is pressed in select_user
            else:
                self.display_user_stats()

    def select_user(self):
        while True:
            if not self.check_window_size():
                continue
            self.stdscr.clear()
            h, w = self.stdscr.getmaxyx()

            if not self.users:
                self.stdscr.addstr(h // 2, (w - len("No users registered.")) // 2, "No users registered.", curses.A_BOLD)
                self.stdscr.addstr(h // 2 + 1, (w - len("Press ESC to return to the main menu.")) // 2, "Press ESC to return to the main menu.", curses.A_DIM)
                self.stdscr.refresh()
                while True:
                    if not self.check_window_size():
                        continue
                    key = self.stdscr.getch()
                    if key == 27:  # ESC key
                        return False
            else:
                self.stdscr.addstr(0, 0, "Select a user to view statistics:", curses.A_BOLD | curses.A_UNDERLINE)
                for idx, user in enumerate(self.users):
                    self.stdscr.addstr(idx + 2, 0, f"{idx + 1}. {user.user_id}")
                self.stdscr.addstr(len(self.users) + 3, 0, "Press ESC to return to the main menu.", curses.A_DIM)
                self.stdscr.refresh()

                while True:
                    if not self.check_window_size():
                        continue
                    key = self.stdscr.getch()
                    if key == 27:  # ESC key
                        return False
                    elif ord('1') <= key <= ord(str(len(self.users))):
                        self.current_user = self.users[key - ord('1')]
                        return True

    def display_user_stats(self):
        while True:
            if not self.check_window_size():
                continue
            self.stdscr.clear()
            h, w = self.stdscr.getmaxyx()
            stats = self.current_user.stats

            # Create a window for the statistics
            stats_win = curses.newwin(h, w, 0, 0)
            stats_win.clear()

            # Display the statistics
            stats_win.addstr(0, 0, f"Statistics for {self.current_user.user_id}", curses.A_BOLD | curses.A_UNDERLINE)
            stats_win.addstr(2, 0, f"Games Played: {stats['games_played']}")
            stats_win.addstr(3, 0, f"Games Won: {stats['games_won']}")
            stats_win.addstr(4, 0, f"Words Revealed: {stats['words_revealed']}")
            stats_win.addstr(5, 0, f"Longest Word Revealed: {stats['longest_word_revealed']}")
            stats_win.addstr(6, 0, f"Mines Stepped: {stats['mines_stepped']}")
            stats_win.addstr(7, 0, f"Highest Score (Classic Mode): {stats['highest_score_classic']}")
            stats_win.addstr(8, 0, f"Highest Score (Timed Mode): {stats['highest_score_timed']}")
            stats_win.addstr(9, 0, f"Minimum Steps Used: {stats['min_steps_used']}")
            stats_win.addstr(10, 0, f"Average Steps Used: {self.current_user.average_steps_used()}")
            stats_win.addstr(12, 0, "Press ESC to return to user selection.", curses.A_DIM)

            # Refresh the window to show the changes
            stats_win.refresh()

            # Wait for user input to return to user selection
            while True:
                if not self.check_window_size():
                    continue
                key = self.stdscr.getch()
                if key == 27:  # ESC key
                    self.current_user = None
                    return