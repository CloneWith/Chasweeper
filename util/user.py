import os

class User:

    # A class to represent a user and their game statistics.
    # Attributes:
    # user_id : str
    #     The unique identifier for the user.
    # stats : dict
    #     A dictionary containing various game statistics for the user.
    #
    # Methods:
    # save_to_file():
    #     Saves the user's statistics to a file.
    # load_from_file(user_id):
    #     Loads a user's statistics from a file based on the user_id.
    # update_file():
    #     Updates the user's statistics in the file.
    # average_steps_used():
    #     Calculates the average number of steps used per game.

    def __init__(self, user_id, games_played=0, games_won=0, words_revealed=0, longest_word_revealed="", mines_stepped=0, highest_score_classic=0, highest_score_timed=0, min_steps_used=float('inf'), total_steps=0, games_played_steps=0):

        # Initialize a new user with the given statistics.
        # 
        # Parameters:
        # - user_id (str): The unique identifier for the user.
        # - games_played (int, optional): The number of games the user has played. Defaults to 0.
        # - games_won (int, optional): The number of games the user has won. Defaults to 0.
        # - words_revealed (int, optional): The number of words the user has revealed. Defaults to 0.
        # - longest_word_revealed (str, optional): The longest word the user has revealed. Defaults to an empty string.
        # - mines_stepped (int, optional): The number of mines the user has stepped on. Defaults to 0.
        # - highest_score_classic (int, optional): The highest score the user has achieved in classic mode. Defaults to 0.
        # - highest_score_timed (int, optional): The highest score the user has achieved in timed mode. Defaults to 0.
        # - min_steps_used (float, optional): The minimum steps the user has used in a game. Defaults to infinity.
        # - total_steps (int, optional): The total number of steps the user has taken. Defaults to 0.
        # - games_played_steps (int, optional): The number of games the user has played using steps. Defaults to 0.

        self.user_id = user_id
        self.stats = {
            "games_played": games_played,
            "games_won": games_won,
            "words_revealed": words_revealed,
            "longest_word_revealed": longest_word_revealed,
            "mines_stepped": mines_stepped,
            "highest_score_classic": highest_score_classic,
            "highest_score_timed": highest_score_timed,
            "min_steps_used": min_steps_used,
            "total_steps": total_steps,
            "games_played_steps": games_played_steps
        }

    def save_to_file(self):

        # Saves the user's statistics to a file.
        # 
        # This method checks if the './data' directory exists, and if not, it creates it.
        # Then, it appends the user's statistics to the 'user.txt' file in CSV format.
        # 
        # The statistics saved include:
        # - user_id: The unique identifier for the user.
        # - games_played: The number of games the user has played.
        # - games_won: The number of games the user has won.
        # - words_revealed: The number of words the user has revealed.
        # - longest_word_revealed: The longest word the user has revealed.
        # - mines_stepped: The number of mines the user has stepped on.
        # - highest_score_classic: The highest score the user has achieved in classic mode.
        # - highest_score_timed: The highest score the user has achieved in timed mode.
        # - min_steps_used: The minimum number of steps the user has used in a game.
        # - total_steps: The total number of steps the user has taken in all games.
        # - games_played_steps: The number of games the user has played using steps.
        # 
        # Raises:
        #     OSError: If there is an issue creating the directory or writing to the file.

        if not os.path.exists('./data'):
            os.makedirs('./data')
        with open('./data/user.txt', 'a') as file:
            file.write(f"{self.user_id},{self.stats['games_played']},{self.stats['games_won']},{self.stats['words_revealed']},{self.stats['longest_word_revealed']},{self.stats['mines_stepped']},{self.stats['highest_score_classic']},{self.stats['highest_score_timed']},{self.stats['min_steps_used']},{self.stats['total_steps']},{self.stats['games_played_steps']}\n")

    @staticmethod
    # @staticmethod decorator in Python is used to define a static method within a class. 
    # Static methods belong to the class itself rather than any instance of the class. 
    # They do not require access to instance-specific data or methods, and therefore, do not take the self or cls parameters.

    def load_from_file(user_id):

        # Load a user from the file based on the given user_id.
        #
        # Args:
        #     user_id (str): The ID of the user to load.
        # 
        # Returns:
        #     User: A User object if the user_id is found in the file, otherwise None.

        if not os.path.exists('./data/user.txt'):
            return None
        with open('./data/user.txt', 'r') as file:
            for line in file:
                data = line.strip().split(',')
                if data[0] == user_id:
                    user = User(data[0], int(data[1]), int(data[2]), int(data[3]), data[4], int(data[5]), int(data[6]), int(data[7]), float(data[8]), int(data[9]), int(data[10]))
                    return user
        return None

    def update_file(self):

        # Updates the user data file with the current user's statistics.
        # 
        # This method reads the user data from './data/user.txt', updates the statistics
        # for the current user (identified by `self.user_id`), and writes the updated
        # data back to the file. If the file does not exist, the method returns without
        # making any changes.
        # 
        # The user data file is expected to have the following format:
        # user_id,games_played,games_won,words_revealed,longest_word_revealed,
        # mines_stepped,highest_score_classic,highest_score_timed,min_steps_used,
        # total_steps,games_played_steps
        # 
        # Each line in the file corresponds to a different user.
        # 
        # Attributes:
        #     self.user_id (str): The ID of the current user.
        #     self.stats (dict): A dictionary containing the user's statistics with the
        #         following keys:
        #         - 'games_played': Number of games played.
        #         - 'games_won': Number of games won.
        #         - 'words_revealed': Number of words revealed.
        #         - 'longest_word_revealed': The longest word revealed.
        #         - 'mines_stepped': Number of mines stepped on.
        #         - 'highest_score_classic': Highest score in classic mode.
        #         - 'highest_score_timed': Highest score in timed mode.
        #         - 'min_steps_used': Minimum steps used.
        #         - 'total_steps': Total steps taken.
        #         - 'games_played_steps': Number of games played with steps.

        if not os.path.exists('./data/user.txt'):
            return
        lines = []
        with open('./data/user.txt', 'r') as file:
            for line in file:
                data = line.strip().split(',')
                if data[0] == self.user_id:
                    lines.append(f"{self.user_id},{self.stats['games_played']},{self.stats['games_won']},{self.stats['words_revealed']},{self.stats['longest_word_revealed']},{self.stats['mines_stepped']},{self.stats['highest_score_classic']},{self.stats['highest_score_timed']},{self.stats['min_steps_used']},{self.stats['total_steps']},{self.stats['games_played_steps']}\n")
                else:
                    lines.append(line)
        with open('./data/user.txt', 'w') as file:
            file.writelines(lines)

    def average_steps_used(self):

        # Calculate the average number of steps used per game.
        # 
        # Returns:
        #     float: The average number of steps used per game. Returns 0 if no games have been played.

        if self.stats["games_played_steps"] == 0:
            return 0
        return self.stats["total_steps"] / self.stats["games_played_steps"]