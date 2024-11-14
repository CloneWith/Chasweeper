import curses
from menu import Menu

# Game launcher

def main(stdscr):
    # The main function that initializes and runs the menu for the puzzle game.
    # Args:
    #     stdscr: The standard screen object provided by the curses library.
    menu = Menu(stdscr)
    menu.run()

if __name__ == "__main__":
    curses.wrapper(main)