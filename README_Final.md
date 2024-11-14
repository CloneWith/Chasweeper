# README

## 1. Group members

Chen Jiahe

Wong Wing Man

Meng Xiangkun

Chan Ka Hei

Wei Yuetong

---

## 2. Contributions

Chen Jiahe

Wong Wing Man - Video producing / editing

Meng Xiangkun - Coding, Testing, Readme

Chan Ka Hei

Wei Yuetong

---

## 3. Background

Wordweeper is a game that combines crossword puzzle and Minesweeper. In a square grid of hidden tiles, each cell might contain a letter, a mine, or nothing. To win the game, the player has to find all the hidden words by revealing letters forming those words under the tiles. If three mines were to be uncovered, the player would automatically lose the game.

To encourage strategic planning and analytical thinking, a score deduction will be given when mine is triggered, and a higher score will be awarded when the player wins the game with fewer moves. The player should utilize the word hint (which hints the location of target letters) and Mine hint (which hints the location of mines) to find all the hidden words with the fewest moves possible whilst avoiding uncovering mines.  Red flag mark and question mark mark can be used to flag the tile where the player thinks might have a mine. It should be reminded that the ultimate goal of the game is not to clear the board but rather to locate the words as fast as one can without triggering mine.

The game consists of three difficulties: easy, hard, and expert. Higher difficulties come with a larger grid, longer and more complex words, more severe penalties when stepped on mines, and most importantly, a higher achievable score.

It‘s exactly a great chance for you to not only logical mind, but also consolidate the words we learned on the ENGG1330 ! Come and play Wordweeper!

We are waiting for you !

Video Links:

Game Trailer: https://www.youtube.com/watch?v=Z_8NRDn1PJ0&ab_channel=BBI
Demo video: https://www.youtube.com/watch?v=ejUL5SK2R08&ab_channel=BBI

---

## 4. Gameplay

- **Overview**
    
    Wordweeper is a combination of a word game and the famous puzzle game: “Minesweeper”.
    
    Like Minesweeper, the game features a grid contains different contents, including letters, empty cells, hints and mines. All the cells on the playfield will be covered at first, the goal is to uncover cells to successfully reveal all the words hidden in the board.
    
    During gameplay, players can make use of hints and other pieces of information, to strategize their move, in order to reveal all the words with minimized steps.
    

- **Operating Cells / Hint System:**
    
    Left click on cells to reveal them. When revealing cells, there can be different information displayed:
    
    - **Word hint**: If the revealed cell is not part of the word, and it is located near a word, it will display a number, indicating in the 3-by-3 area the number of letters belonging to a target word.
    - **Mine hint**: If the revealed cell is situated near a mine, it will display a dot in the mine’s direction. The dot indicates that in its 3-by-3 area there will be at least 1 mine in the 3 cells on that direction. Mine hint will be displayed in every cells if they met these conditions.
    - **Word cell**: These cells contain letters, not word hint or blank. The contained letter can be a part of the word, or they can be random.
    
    During gameplay, players can choose to place a mark on the cells. These are designed to assist players to organize information, no additional scoring will be awarded when placing these marks correctly. There will be two marks provided:
    
    - 🚩: This cell contain a mine.
    - ❔: This cell might contain a mine.
    
    Player can use `Ctrl + Left Click` to place a mark on a cell. Will display 🚩 at first, Ctrl + Left Click again to change the mark into ❔. Press again to revove the mark.
    
    There will be a hint displayed on the top left screen, displayed as:
    ```
    Words left:
    _ _ _ _ 
    _ _ _ _ _
    _ _ _ _ _ _
    
    ```
    
    …for indicating the words left in the board. Number of dashes indicate the length of the word.
    If there is a word being completely revealed, this display will update and it will display the words being successfully revealed on the lines.
    
- **Forming Words:**
    
    During gameplay, players has to uncover cells and reveal all the words in the board in order to win.
    
    Target words are being hinted on the left corner. If a player managed to reveal any of these words, they will receive an addition of score.
    

- **Scoring System Overview:**
    
    For our game we have designed a scoring system that can calculate the score depending on how well the game is being played by the players. The scoring system has to encourage players for making wise moves and execute strategized plays, not spamming on the board and brute-forcing the game.
    
    To simplify this system and make it easier to explain, we can break it down into two parts:
    
    - **Scoreing System - Awarding:**
    
    We’ve designed to make the scoring system change the amount of awarded points based on how well the player reveals all the word from the playfield.
    
    The only situation where player will be awarded scores is by revealing words from the board. The amount of score awarded will be calculated based on a base score, and depending on following factors:
    
    - **Word Complexity:** The complexity of the target word, measured by an integer. The complexity is being calculated by measuring the number of unique characters included:
        
        `complexity = len(set(word))`
        
    - **Word Length:** The length of the revealed word. The longer the word is, more points will be awarded after revealing it.
        
        `word_length = len(word)`
        
    
    - **Scoreing System - Penalty:**
    
    Awarding scoreing system generally will reward quite a lot scores, so what will make the plays different is more directly affected by the penalty scoreing system. Plays carrying out nice and neat moves will be less penaltized, and opposite for these non-strategized plays.
    
    Penalty system aims to encourage players to use hints and reveal cells wisely.
    
    The player will get penaltized by a reduction of score, depending on their way to play that game. Including:
    
    - **Random clicking / Brute-forcing**
    
    The player will get punished by gradually increase the amount of penalty score if they try to spamming the board. The calculation formula is:
    
    $$
    P(r, c) =
    \begin{cases}
    \left( e^{k (r - c)} - 0.6 \right) \cdot b & \text{for } r \leq (c - 2) \\
    \\
    \left( \frac{r - (c - 2)}{2} \right) \cdot b & \text{for } (c - 2) < r \leq c \\
    \\
    e^{k (r - c)} \cdot b & \text{for } r > c
    \end{cases}
    $$
    
    where:
    
    - **r**: Random click counter, record how many random clicks the player did so far.
    - **c**: Cap value, decide the point about when the punishment multiplier went below 1 to above 1.
    - **k**: Constant. Set to 0.01
    - **b**: Base penalty score for random clicking. Varies with stages.
    
    You can find more explaination about this algorithm here: [https://github.com/NaughtyChas/Wordweeper/pull/17#issuecomment-2468165644](https://github.com/NaughtyChas/Wordweeper/pull/17#issuecomment-2468165644)
    
    ---
    
    - **Dynamic Mine Penalty**
    
    The player will receive score reduction when they stepped on a mine, until they lose.
    
    The point of this algorithm is to adjust the amount of mine penalty points based on when the game is currently on, for instance, early stage or ending stage. The formula is:

    $$ Penalty\ =\ Base\ penalty\ ×\ ({e}^{\frac {(220\ -\ Total\ cells)} {3000}\ ×\ (Revealed\ cells\ -\ 5)}-\ \frac {Total\ cells} {900}) $$
        
    
    This formula can change the penalty value and the leniency for mine revealing, based on the size of the board and when the mine is being revealed. Should be functioning for Total cells value between 49 and 121. In short, mines revealed in the early stage will be punished less, and vice versa.
    
    You can find more explaination about this algorithm here:
    
    [https://github.com/NaughtyChas/Wordweeper/pull/17#issuecomment-2467928859](https://github.com/NaughtyChas/Wordweeper/pull/17#issuecomment-2467928859)
    
    ---
    
- **Difficulty System:**
    
    The game features three difficulties: Easy, Hard and Expert.
    
    Different difficulty will still have the same gameplay rule, but there will be something different:
    
    - **Playfield Size:** When difficulty goes up, the size of the board will get larger and larger. For instance, “Easy” features a 7x7 grid but “Expert” push that into 11x11.
    - **Number of words:** Latter difficulty include more words needed to reveal for winning.
    - **Number of mines:** Latter difficulty include more mines, but the at most 3 mines required for lose does not change. Be careful!
    - **Scoring:** Latter will have more severe punishment over score award by raevealing letters, so be prepared to get larger score, or otherwise!

- **User system:**
    
    The game includes a user system. This is required by other systems we built.
    
    Fresh start of the game require player register. The game will instruct players to enter their ID to complete registering. No password is required.
    
    Once the player has registered, the player can choose who to play on before entering the game, or register more players.
    
- **Statistics system:**
    
    This is powered by the user system. When user is logged in, the system will process the gameplay and record relevant information after they completed a round of game. These information will be process and stored in a text-based database.
    
    So far supported displayed stats include:
    
    - Number of games played
    - Number of games won
    - Highest score achieved
    
    Players can review these stats for yourself, or other players, by entering a dedicated page we’ve designed to display stats information in the menus.
    

---

## 5. Technical details

- **Game interaction / display**
    
    In this project we’ve used a built-in python package, curses, to deliver an interactive and visually intuitive experience to our players.
    
    Players can choose to interact with the program by clicking mouse buttons, or using arrow keys to navigate. This package allow us to create a satisfying gameplay for board interaction.
    

- **Object-Oriented Programming (OOP)**
    
    I decided to use OOP programming style throughout the entire project. By defining classes and objects, I’ve made the code to be more modular, making it easier to read, maintain and more importantly, upgradability.
    
- **Modular Project Structure**
    
    Instead of storing all code in one [main.py](http://main.py) file, I’ve seperated different types of code into seperate files. For instance [diffcalc.py](http://diffcalc.py) only handle word complexity calculation logic, and [menu.py](http://menu.py) is used to display menu, not including main game logic.
    
    This brings us easier management and capability to update the game.
    
- **Database storaging and accessing**
    
    I used file-based database to store necessary information for game, incuding words to be revealed, and user stats information. The program uses file reading and writing methods to interact with data, accessing, processing and write them back to the database.
    

- **Mathematics-based Calculation**
    
    I always believe that a good scoreing system can be driven by a suitable mathematics model, so we did that in our project. 
    
    Instead of using static scoreing system most of the other games does, I’ve decided to use mathematics modelling to calculate a score that is more flexible, more dynamic and more likely to guide our players to play the game in the desired way - make moves wisely. Our system can calculate a score which can reflect the players’ every single move, making our game more challenging and more fun to play.
    

---

## 6. Run the game

The game can be launched by executing `main.py` in the root project directory. You can execute this file by following steps:

1. Make sure that your terminal’s current directory is located in root directory.
2. Type `python main.py` to run the game.

The game requires “curses” supported terminal to run, otherwise the game won’t function properly, eventhough the program can actually run. Make sure your environment has “curses” package installed, and the terminal supports “curses” package features.

If you are running our game on Ed platform python workspaces, just simply launch a terminal and execute `python main.py`.

---

## 7. Features

Our game featuring an interactive interface, allowing our players to play the game with not only the keyboard, but also mouse. You can activate the menu tabs or board cells by left mouse button.

The game provides a balanced dynamic scoring system that will calculate and took every steps into account, which is competitive and fun to play for gamers who cares about scores.

Use the user statistics system to figure out if you are a Wordweeper master! Stats about yourself will be calculated for each game, check your stats to find out your skill.

So detailed even for the terminal window’s size, our game really has a fine reminder system. Enough reminder will help and lead gamers gradually have a good grasp of this game. With in-time tips, even when we make a wrong operation to the game, we don’t need to come back to see the instructions at the main menu, our game system will remind you immediately.

For different players we have different difficulties for you. We provide 3 difficulties from Easy to Expert, each of them features different difficulty index. As the difficulty increases, the more strategic it needs, the longer the words it has to spell. Choose your difficulty which mostly fits your playstyle.

Mind the mine! Danger is hidden just under the cell! Now it’s your show time!

---