import curses
from menu import Menu

# Game launcher

def main(stdscr):
    menu = Menu(stdscr)
    menu.run()

if __name__ == "__main__":
    curses.wrapper(main)