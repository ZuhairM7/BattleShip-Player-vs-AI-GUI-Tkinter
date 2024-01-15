"""
Name: Zuhair Merali
UTEID: zsm386
On my honor, Zuhair Merali, this programming assignment is my own work
and I have not provided this code to any other student.

Complete the following:
1. What is the purpose of your program?
The purpose of my program is to create an engaging and interactive 
Battleship game, where the user can play against a sophisticated AI. 
The game is designed to challenge the user's strategic thinking and provide
 an enjoyable gaming experience. By implementing a smart AI, the program
aims to create a more dynamic and competitive environment, making it more
interesting and stimulating for the user.

2. List the major features of your program:
a. A dynamic game board that allows the user to place 5 different ships 
ranging in length from 5 to 1, either horizontally or vertically.

b. An intelligent AI that adapts its guessing strategy based on the highest
 length ship remaining and only guesses in spots where a whole ship of that
length could exist.

c. A hit detection system that enables the AI to continue guessing in the 
immediate vicinity (up, down, right, and left) once it scores a hit, 
increasing the likelihood of sinking the user's ships.

d. A direction reversal feature that allows the AI to change its direction 
if a miss occurs before sinking a ship, making it able to sink the ship

e. A user-friendly interface built with tkinter that provides a smooth and 
visually appealing gaming experience.
3. What 3rd party modules must be installed for the program to work?
No other 3rd party modules were used(only imported tkinter and random)
(Must be clear and explicit here or we won't be able to test your program.)

4. List the things your learned while doing this program. Python features,
techniques, third party modules, etc.
I learned how to really use tkinter effectively to display widgets in
an organized matter. I also learned how to implement a fairly complicated
AI that I am overall happy with. This AI through 20 test runs won against
me trying 6 out of 20 times which is fairly decent in my opinion

5. What was the most difficult thing you had to overcome or learn
to get this program to work?

The most difficult challenge I faced while developing this program was
understanding and implementing the AI's decision-making algorithm.
To overcome this, I had to break down the problem into smaller parts, 
devise a clear strategy for the AI, and thoroughly test the AI's behavior
to ensure it was behaving as intended.

6. What features would you add next?
a. Implementing images for the ships to enhance the visual appeal of the 
game.
b. Introducing a win streak counter to track the user's consecutive wins 
and add an element of progression to the game.
c. Adding difficulty levels to the AI to cater to players with different 
skill levels.
d. Implementing a 2 player mode.
"""""
import tkinter as tk
import random


class BattleShip(tk.Tk):
    def __init__(self):
        # Initialize all "private instance variables"
        super().__init__()
        self.title = None
        self.configure(bg="magenta")
        self.resizable = False
        self.geometry("1500x1500")
        self.player = None
        self.playerTwo = None
        self.but_array = [[tk.Button for _ in range(10)] for _ in
                          range(10)]
        self.player_ships = []
        self.ai_ships = []
        self.opp_array = None
        self.one = None
        self.two = None
        self.turn = None
        self.ships = 10
        self.direction = False
        self.horizontal = None
        self.vertical = None
        self.test = None
        self.start_game = None
        self.start = False
        self.new_turn = None
        self.rules = None
        self.info = None
        self.guessRandom = True
        self.mrg_button = None
        self.pick_direction = False
        self.ai_direction = ""
        self.mrg_row = 0
        self.mrg_col = 0
        self.orig_row = 0
        self.orig_col = 0

    def win(self):
        if self.player_wins():
            self.turn.configure(text="YOU WIN! Press reset to play again")
            self.start = False
            self.start_game.configure(text="Reset Game",
                                      command=self.reset)

        elif self.ai_wins():
            self.turn.configure(text="You Lost! Press reset to try again")
            self.start = False
            self.start_game.configure(text="Reset Game",
                                      command=self.reset)

    def reset(self):
        self.player_ships = []
        self.ai_ships = []
        self.start = False
        self.guessRandom = True
        self.mrg_button = None
        self.pick_direction = False
        self.ai_direction = ""
        self.mrg_row = 0
        self.mrg_col = 0
        self.orig_row = 0
        self.orig_col = 0
        self.ships = 10
        self.direction = False
        self.new_turn.configure(text="")
        self.make_button_grids()
        self.add_stuff_to_window()
        self.place_ai_ships()

    def make_button_grids(self):
        for row_size in range(10):
            for col_size in range(10):
                self.but_array[row_size][col_size] = \
                    tk.Button(self.player,
                              highlightbackground="white",
                              background="white", width=1, height=2)
                self.but_array[row_size][col_size].grid(row=row_size,
                                                        column=col_size)
                self.but_array[row_size][col_size].configure(
                    command=lambda row=row_size, col=col_size:
                    self.on_button_click(row, col))
        self.playerTwo = tk.Frame(self, bg="black")
        self.playerTwo.grid(row=1, column=2, padx=(100, 0), pady=100)

        self.opp_array = [[None for _ in range(10)] for _ in range(10)]

        for r in range(10):
            for c in range(10):
                self.opp_array[r][c] = tk.Button(self.playerTwo,
                                                 bg="white",
                                                 width=1, height=2)
                self.opp_array[r][c].grid(row=r, column=c)
                self.opp_array[r][c].configure(
                    command=lambda row=r, col=c: self.on_guess_click(row,
                                                                     col))

    def add_player_grid(self):
        self.player = tk.Frame(self, bg="black")
        self.player.grid(row=1, column=1, padx=(100, 0), pady=100)
        self.make_button_grids()

    def add_stuff_to_window(self):
        # Sets text color and font of title
        self.title = tk.Label(self, text="BattleShip Player vs AI",
                              fg="cyan", bg="black",
                              font=("Calibri", 25, "bold"))
        self.title.place(x=470, y=25)

        # Labels player one and twos grids
        self.one = tk.Label(self, text="Player One", fg="white",
                            bg="black",
                            font=("Calibri", 20, "bold"))
        self.one.place(x=270, y=50)

        self.two = tk.Label(self, text="AI", fg="white",
                            bg="black",
                            font=("Calibri", 20, "bold"))
        self.two.place(x=865, y=50)

        # Creates a label that shows turn and count of ships
        self.turn = tk.Label(self,
                             text=f"Player One place your ships : count "
                                  f"{self.ships - 5}", fg="magenta",
                             bg="black", font=("Calibri", 17, "bold"))
        self.turn.place(x=490, y=610)

        # Creates a label that gives direction on whose turn to attack
        self.new_turn = tk.Label(self, text="Player One Attack AI",
                                 fg="magenta", bg="black",
                                 font=("Calibri", 17, "bold"))
        self.new_turn.place(x=490, y=650)
        self.new_turn.place_forget()

        # Creates buttons that determine the direction of ship
        self.horizontal = tk.Button(self, text="Place Horizontally "
                                               "right(inclusive)",
                                    command=self.on_horizontal_click)
        self.horizontal.place(x=210, y=570)

        self.vertical = tk.Button(self,
                                  text="Place Vertically down(inclusive)",
                                  command=self.on_vertical_click)
        self.vertical.place(x=750, y=570)

        # Button used to start attacking
        self.start_game = tk.Button(self, text="Start Game",
                                    command=self.on_start_game_click)
        self.start_game.place(x=550, y=700)
        self.start_game.place_forget()

        # Creates a Text Area of rules
        rules_text = (
            "Player One starts by placing all 5 of their ships. The count "
            "increment stands for how many ships are left to place as well"
            "as the length of the ship. Once the user places "
            "their ships a Start Game button appears that they must press "
            "in order to start attacking. User may now guess by pressing"
            "one one of the white spaces on the AI board. If it turns "
            "green this indicates a hit and red indicates a miss. If you"
            "sink a ship the entire ship turns black. AI guesses at the "
            "same time. First to sink all ships WINS!"
        )

        self.rules = tk.Text(self, width=40, height=20, wrap=tk.WORD,
                             bg="cyan")
        self.rules.insert(tk.END, rules_text)
        self.rules.configure(state="disabled")
        self.rules.place(x=1200, y=150)

        self.info = tk.Label(self, text="Rules", bg="black", fg="black",
                             font=("Calibri", 20, "bold"))
        self.info.place(x=1200, y=50)

    def place_ai_ships(self):
        # Define ship sizes
        ship_sizes = [5, 4, 3, 2, 1]

        # Place AI ships on the grid
        for ship_size in ship_sizes:
            while True:
                # Randomly choose starting position and direction
                row = random.randint(0, 9)
                col = random.randint(0, 9)
                direction = random.choice(["horizontal", "vertical"])

                # Check if the ship can be placed horizontally
                if direction == "horizontal":
                    if col + ship_size <= 10:
                        valid = True
                        # Check if the ship overlaps with existing ships
                        for i in range(ship_size):
                            if self.opp_array[row][col + i].cget(
                                    "foreground") == "blue":
                                valid = False
                                break
                        if valid:
                            # Place the ship on the grid
                            # Uses foreground to denote ship
                            current_ai_ship = []
                            for i in range(ship_size):
                                self.opp_array[row][col + i].configure(
                                    foreground="blue",
                                    highlightbackground="white")
                                current_ai_ship.append(
                                    self.opp_array[row][col + i])
                            self.ai_ships.append(current_ai_ship)
                            break
                else:  # direction is "vertical"
                    # Check if the ship can be placed vertically
                    if row + ship_size <= 10:
                        valid = True
                        # Check if the ship overlaps with existing ships
                        for i in range(ship_size):
                            if self.opp_array[row + i][col].cget(
                                    "foreground") == "blue":
                                valid = False
                                break
                        if valid:
                            # Place the ship on the grid
                            current_ai_ship = []
                            for i in range(ship_size):
                                self.opp_array[row + i][col].configure(
                                    foreground="blue",
                                    highlightbackground="white")
                                current_ai_ship.append(
                                    self.opp_array[row + i][col])
                            self.ai_ships.append(current_ai_ship)
                            break

    def on_button_click(self, row, col):
        # Handle button click event for placing player ships
        if not self.start:
            if self.ships > 5:
                current_ship_buttons = []
                if not self.direction:
                    self.place_horizontally(row, col, current_ship_buttons)
                else:
                    self.place_vertically(row, col, current_ship_buttons)
                self.player_ships.append(current_ship_buttons)

    def valid_possible_guess(self, ai_row, ai_col):
        # Check if the AI's guess is valid based on the largest ship left
        highest_length_rem = len(self.player_ships[0])
        print(highest_length_rem)
        right_valid = True
        left_valid = True
        up_valid = True
        down_valid = True
        # Check if the guess is valid in each direction
        for i in range(highest_length_rem):
            if ai_row + i <= 9:
                color = self.but_array[ai_row + i][ai_col].cget(
                    "background")
                if color in ["red", "green", "black"]:
                    down_valid = False
            else:
                down_valid = False
            if ai_row - i >= 0:
                color = self.but_array[ai_row - i][ai_col].cget(
                    "background")
                if color in ["red", "green", "black"]:
                    up_valid = False
            else:
                up_valid = False
            if ai_col + i <= 9:
                color = self.but_array[ai_row][ai_col + i].cget(
                    "background")
                if color in ["red", "green", "black"]:
                    right_valid = False
            else:
                right_valid = False
            if ai_col - i >= 0:
                color = self.but_array[ai_row][ai_col - i].cget(
                    "background")
                if color in ["red", "green", "black"]:
                    left_valid = False
            else:
                left_valid = False
        return right_valid or left_valid or up_valid or down_valid

    def ai_random_guess(self):
        # Make a random guess by the AI
        valid_ai_guess = False

        while not valid_ai_guess:
            ai_row = random.randint(0, 9)
            ai_col = random.randint(0, 9)
            ai_button = self.but_array[ai_row][ai_col]
            ai_current_color = ai_button.cget("background")

            if ai_current_color not in ["red", "green",
                                        "black"] and \
                    self.valid_possible_guess(ai_row, ai_col):
                valid_ai_guess = True
                if ai_current_color == "blue":
                    # Hit
                    ai_button.configure(background="green",
                                        highlightbackground="green")
                    self.new_turn.configure(text="AI got a hit")
                    self.mrg_button = ai_button
                    self.mrg_row = ai_row
                    self.mrg_col = ai_col
                    self.guessRandom = False
                    self.orig_row = ai_row
                    self.orig_col = ai_col
                else:
                    # Miss
                    ai_button.configure(background="red",
                                        highlightbackground="red")
                    self.new_turn.configure(text="AI got a Miss")

    def set_guess_color(self, mrg_row, mrg_col):
        if self.but_array[mrg_row][mrg_col].cget(
                "highlightbackground") == "blue":
            self.but_array[mrg_row][mrg_col].configure(
                background="green", highlightbackground="green")
            self.pick_direction = True
            self.new_turn.configure(text="AI got a hit")
        else:
            self.but_array[mrg_row][mrg_col].configure(
                background="red", highlightbackground="red")
            self.new_turn.configure(text="AI got a miss")

    def continue_right(self):
        # Check if the AI can continue guessing to the right
        if self.mrg_button.cget(
                "background") == "green" and self.mrg_col + 1 <= 9 and \
                self.but_array[self.mrg_row][
                    self.mrg_col + 1].cget(
                    "background") not in ["red",
                                          "green",
                                          "black"]:
            self.set_guess_color(self.mrg_row, self.mrg_col + 1)
            self.mrg_button = \
                self.but_array[self.mrg_row][
                    self.mrg_col + 1]
            self.mrg_col = self.mrg_col + 1
            return True
        elif self.orig_col - 1 >= 0 and \
                self.but_array[self.orig_row][
                    self.orig_col - 1].cget(
                    "background") not in ["red",
                                          "green",
                                          "black"]:
            print("reverse right")
            self.ai_direction = "left"
            self.set_guess_color(self.orig_row, self.orig_col - 1)
            self.mrg_button = \
                self.but_array[self.orig_row][
                    self.orig_col - 1]
            self.mrg_col = self.orig_col - 1
            return True
        else:
            return False

    def continue_left(self):
        # Check if the AI can continue guessing to the left
        if self.mrg_button.cget(
                "background") == "green" and self.mrg_col - 1 >= 0 and \
                self.but_array[self.mrg_row][
                    self.mrg_col - 1].cget(
                    "background") not in ["red",
                                          "green",
                                          "black"]:
            self.set_guess_color(self.mrg_row, self.mrg_col - 1)
            self.mrg_button = \
                self.but_array[self.mrg_row][
                    self.mrg_col - 1]
            self.mrg_col = self.mrg_col - 1
            return True
        elif self.orig_col + 1 <= 9 and \
                self.but_array[self.orig_row][
                    self.orig_col + 1].cget(
                    "background") not in ["red",
                                          "green",
                                          "black"]:
            self.ai_direction = "right"
            self.set_guess_color(self.orig_row, self.orig_col + 1)
            self.mrg_button = \
                self.but_array[self.orig_row][
                    self.orig_col + 1]
            self.mrg_col = self.orig_col + 1
            return True
        else:
            return False

    def continue_up(self):
        # Check if the AI can continue guessing to the up
        if self.mrg_button.cget(
                "background") == "green" and self.mrg_row - 1 >= 0 and \
                self.but_array[self.mrg_row - 1][
                    self.mrg_col].cget(
                    "background") not in ["red",
                                          "green",
                                          "black"]:
            self.set_guess_color(self.mrg_row - 1, self.mrg_col)
            self.mrg_button = \
                self.but_array[self.mrg_row - 1][
                    self.mrg_col]
            self.mrg_row = self.mrg_row - 1
            return True
        elif self.mrg_row + 1 <= 9 and \
                self.but_array[self.orig_row + 1][
                    self.orig_col].cget(
                    "background") not in ["red",
                                          "green",
                                          "black"]:
            self.ai_direction = "down"
            self.set_guess_color(self.orig_row + 1, self.orig_col)
            self.mrg_button = \
                self.but_array[self.orig_row + 1][
                    self.orig_col]
            self.mrg_row = self.orig_row + 1
            return True
        else:
            return False

    def continue_down(self):
        # Check if the AI can continue guessing to the down
        if self.mrg_button.cget(
                "background") == "green" and self.mrg_row + 1 <= 9 and \
                self.but_array[self.mrg_row + 1][
                    self.mrg_col].cget(
                    "background") not in ["red",
                                          "green",
                                          "black"]:
            self.set_guess_color(self.mrg_row + 1,
                                 self.mrg_col)
            self.mrg_button = \
                self.but_array[self.mrg_row + 1][
                    self.mrg_col]
            self.mrg_row = self.mrg_row + 1
            return True
        elif self.orig_row - 1 >= 0 and \
                self.but_array[self.orig_row - 1][
                    self.orig_col].cget(
                    "background") not in ["red",
                                          "green",
                                          "black"]:
            self.ai_direction = "up"
            self.set_guess_color(self.orig_row - 1, self.orig_col)
            self.mrg_button = \
                self.but_array[self.orig_row - 1][
                    self.orig_col]
            self.mrg_row = self.orig_row - 1
            return True
        else:
            return False

    def back_to_random(self):
        self.guessRandom = True
        self.ai_random_guess()
        self.pick_direction = False
        self.ai_direction = ""

    def on_guess_click(self, row, col):
        if self.start:
            button = self.opp_array[row][col]
            current_color = button.cget("background")

            if current_color not in ["red", "green", "black"]:
                if button.cget("foreground") == "blue":
                    # Hit
                    button.configure(background="green",
                                     highlightbackground="green")
                    self.turn.configure(text="You got a Hit!")
                else:
                    # Miss
                    button.configure(background="red",
                                     highlightbackground="red")
                    self.turn.configure(text="You got a MISS!")

                # AI's guess
                if self.guessRandom or self.mrg_button.cget(
                        "background") == "black":
                    self.ai_random_guess()
                    self.pick_direction = False
                    self.ai_direction = ""
                else:
                    if self.pick_direction:
                        if self.ai_direction == "right":
                            if not self.continue_right():
                                self.back_to_random()
                        elif self.ai_direction == "left":
                            if not self.continue_left():
                                self.back_to_random()
                        elif self.ai_direction == "up":
                            if not self.continue_up():
                                self.back_to_random()
                        elif self.ai_direction == "down":
                            if not self.continue_down():
                                self.back_to_random()
                        else:
                            self.back_to_random()
                    else:
                        if self.but_array[self.orig_row][
                            self.orig_col].cget(
                            "background") == "green" and self.orig_col \
                                + 1 <= 9 and self.but_array[self.orig_row][
                                    self.orig_col + 1].cget(
                                    "background") not in ["red",
                                                          "green",
                                                          "black"]:
                            print("orig right")
                            self.set_guess_color(self.orig_row,
                                                 self.orig_col + 1)
                            self.mrg_button = \
                                self.but_array[self.orig_row][
                                    self.orig_col + 1]
                            self.mrg_col = self.orig_col + 1
                            self.mrg_row = self.orig_row
                            self.ai_direction = "right"
                            self.guessRandom = False
                        elif self.but_array[self.orig_row][
                            self.orig_col].cget(
                            "background") == "green" and self.orig_col - 1\
                                >= 0 and self.but_array[self.orig_row][
                                    self.orig_col - 1].cget(
                                    "background") not in ["red",
                                                          "green",
                                                          "black"]:
                            self.set_guess_color(self.orig_row,
                                                 self.orig_col - 1)
                            self.mrg_button = \
                                self.but_array[self.orig_row][
                                    self.orig_col - 1]
                            self.mrg_col = self.orig_col - 1
                            self.mrg_row = self.orig_row
                            self.ai_direction = "left"
                            self.guessRandom = False
                        elif self.but_array[self.orig_row][
                            self.orig_col].cget(
                            "background") == "green" and self.orig_row - 1\
                                >= 0 and self.but_array[self.orig_row - 1][
                                    self.orig_col].cget(
                                    "background") not in ["red",
                                                          "green",
                                                          "black"]:
                            self.set_guess_color(self.orig_row - 1,
                                                 self.orig_col)
                            self.mrg_button = \
                                self.but_array[self.orig_row - 1][
                                    self.orig_col]
                            self.mrg_row = self.orig_row - 1
                            self.mrg_col = self.orig_col
                            self.ai_direction = "up"
                            self.guessRandom = False
                        elif self.but_array[self.orig_row][
                            self.orig_col].cget(
                            "background") == "green" and self.orig_row + 1\
                                <= 9 and self.but_array[self.orig_row + 1][
                            self.orig_col].cget(
                            "background") not in ["red",
                                                  "green",
                                                  "black"]:
                            self.set_guess_color(self.orig_row + 1,
                                                 self.orig_col)
                            self.mrg_button = \
                                self.but_array[self.orig_row + 1][
                                    self.orig_col]
                            self.mrg_row = self.orig_row + 1
                            self.mrg_col = self.orig_col
                            self.ai_direction = "down"
                            self.guessRandom = False
            else:
                self.turn.configure(
                    text="You have already guessed this spot")
            self.check_sunken_ships()

    def check_sunken_ships(self):
        # Check for sunken player ships
        for ship in self.player_ships:
            if all(button.cget("background") == "green" for button in
                   ship):
                for button in ship:
                    button.configure(background="black",
                                     highlightbackground="black")
                self.player_ships.remove(ship)
                self.new_turn.configure(text="AI sunk a ship")

        # Check for sunken AI ships
        for ship in self.ai_ships:
            if all(button.cget("background") == "green" for button in
                   ship):
                ship_index = 0
                for button in ship:
                    button.configure(background="black",
                                     highlightbackground="black")
                    ship_index += 1
                self.ai_ships.remove(ship)
                self.turn.configure(text="You sunk a SHIP")
        self.win()

    def player_wins(self):
        if len(self.ai_ships) == 0:
            return True
        return False

    def ai_wins(self):
        if len(self.player_ships) == 0:
            return True
        return False

    def place_horizontally(self, row, col, current_ship_buttons):
        if col + (self.ships - 5) <= 10:
            valid = True
            for i in range(self.ships - 5):
                if self.but_array[row][col + i].cget(
                        "background") == "blue":
                    valid = False
                    break
            if valid:
                for i in range(self.ships - 5):
                    self.but_array[row][col + i].configure(
                        background="blue", highlightbackground="blue")
                    current_ship_buttons.append(
                        self.but_array[row][col + i])
                self.ships -= 1
                if self.ships >= 6:
                    self.turn.configure(
                        text="Player One place your ships : count " + str(
                            self.ships - 5))
                else:
                    self.start_game.place(x=550, y=700)
                    self.turn.configure(text="Press Start game to begin")

    def place_vertically(self, row, col, current_ship_buttons):
        if row + (self.ships - 5) <= 10:
            valid = True
            for i in range(self.ships - 5):
                if self.but_array[row + i][col].cget(
                        "background") == "blue":
                    valid = False
                    break
            if valid:
                for i in range(self.ships - 5):
                    self.but_array[row + i][col].configure(
                        background="blue", highlightbackground="blue")
                    current_ship_buttons.append(
                        self.but_array[row + i][col])
                self.ships -= 1
                if self.ships >= 6:
                    self.turn.configure(
                        text="Player One place your ships : count " + str(
                            self.ships - 5))
                else:
                    self.start_game.place(x=550, y=700)
                    self.turn.configure(text="Press Start game to begin")

    def on_horizontal_click(self):
        self.direction = False

    def on_vertical_click(self):
        self.direction = True

    def on_test_click(self):
        for r in range(10):
            for c in range(10):
                if self.but_array[r][c]['foreground'] == "white":
                    self.but_array[r][c].configure(bg="blue")

                if self.opp_array[r][c]['foreground'] == "white":
                    self.opp_array[r][c].configure(bg="blue")

    def on_start_game_click(self):
        self.new_turn.place(x=450, y=650)
        self.ships -= 1
        self.start = True
        self.start_game.grid_forget()


def main():
    battle_ship = BattleShip()
    battle_ship.add_player_grid()
    battle_ship.add_stuff_to_window()
    battle_ship.place_ai_ships()
    return battle_ship


if __name__ == '__main__':
    app = main()
    app.mainloop()
