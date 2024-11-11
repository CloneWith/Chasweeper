import os

class User:
    def __init__(self, user_id, games_played=0, games_won=0, words_revealed=0, longest_word_revealed="", mines_stepped=0, highest_score_classic=0, highest_score_timed=0, min_steps_used=float('inf'), total_steps=0, games_played_steps=0):
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
        if not os.path.exists('./data'):
            os.makedirs('./data')
        with open('./data/user.txt', 'a') as file:
            file.write(f"{self.user_id},{self.stats['games_played']},{self.stats['games_won']},{self.stats['words_revealed']},{self.stats['longest_word_revealed']},{self.stats['mines_stepped']},{self.stats['highest_score_classic']},{self.stats['highest_score_timed']},{self.stats['min_steps_used']},{self.stats['total_steps']},{self.stats['games_played_steps']}\n")

    @staticmethod
    def load_from_file(user_id):
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
        if self.stats["games_played_steps"] == 0:
            return 0
        return self.stats["total_steps"] / self.stats["games_played_steps"]