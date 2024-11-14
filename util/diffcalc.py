def calculate_complexity(word):

    # Calculate the complexity of a given word.
    # 
    # The complexity is defined as the number of unique characters in the word.
    # 
    # Args:
    #     word (str): The word for which to calculate the complexity.
    # 
    # Returns:
    #     int: The complexity of the word, i.e., the number of unique characters.

    complexity = len(set(word))
    return complexity

def update_words_file():

    # Reads a file containing words and their complexity levels, calculates the complexity for words 
    # that do not have it, and writes the updated information back to the file.
    #
    # The function performs the following steps:
    # 1. Reads the words and their complexity levels from './data/words.txt'.
    # 2. If a word does not have a complexity level, it calculates the complexity using the 
    #    `calculate_complexity` function.
    # 3. Writes the updated words and their complexity levels back to './data/words.txt'.
    # 4. Prints a message indicating whether any words were updated with new complexity levels.
    #
    # Note:
    # - The file './data/words.txt' should contain words and their complexity levels separated by commas.
    # - If a word does not have a complexity level, it should be followed by a comma with no value after it.
    #
    # Raises:
    # - IOError: If there is an issue reading from or writing to the file.

    words = []
    with open('./data/words.txt', 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 2:
                word, complexity = parts
            else:
                word = parts[0]
                complexity = None
            words.append((word, complexity))

    updated = False
    with open('./data/words.txt', 'w') as file:
        for word, complexity in words:
            if complexity is None:
                complexity = calculate_complexity(word)
                updated = True
            file.write(f'{word},{complexity}\n')

    if updated:
        print("Words file updated with complexity levels.")
    else:
        print("All words already have complexity levels.")

if __name__ == "__main__":
    update_words_file()