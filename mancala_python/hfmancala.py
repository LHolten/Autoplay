'''Human Friendly Mancala. Run this file to play against the evolved agents. Setup below.'''

import neuralnetwork as nn
import poparchives as popa
import numpy as np

# ---------------------------------------------------------------------------

# SETUP:

# Load in generation to play against.
# Change the filename to the generation who's agents you want to play against.
population = popa.load("gen0.pkl")

# 0 or 1 depending on whether human goes first or second. (0 means first.)
human = 0

# Rank of the agent in the generation. (0 is first, 1 is second, ..., -1 is last.)
# Change this if you want to try different agents in the same generation.
rank = 0

# ---------------------------------------------------------------------------

# CLASS DEFINITION:


class Human_Friendly_Mancala:

    def __init__(self):
        """Game creation."""
        start_stones = 4
        self.board = [start_stones]*6 + [0] + [start_stones]*6 + [0]
        self.player = 0
        self.is_active = True
        self.result = None

        self.print_board(self.board)

    def valid_choice(self, pit: int):
        """Determines if the pit is valid (on the correct side and not empty).

        Arguments:
            pit {int} -- The chosen pit.

        Returns:
            bool -- True if valid, False if invalid.
        """

        # Calculates what the chosen pit is on the board based on the player.
        board_pit = self.player*7 + pit

        if pit in range(6) and self.board[board_pit] != 0:
            return True

        else:
            # Error messages
            if pit not in range(6):
                print("Invalid Input. Pit out of range.")
            elif self.board[board_pit] == 0:
                print("Chosen pit is empty.")
            else:
                print("Invalid input.")
            return False

    def take_turn(self, pit: int):
        """Takes a turn in the game.

        Arguments:
            pit {int} -- Chosen pit to take the stones out of.
        """

        # Calculates what the chosen pit is on the board based on the player.
        board_pit = self.player*7 + pit

        print("* Player {} picked pit [{}] (board pit [{}]) with [{}] stones.".format(
            self.player, pit, board_pit, self.board[board_pit]))

        # Picks up stones from the pit.
        stones_in_hand = self.board[board_pit]
        self.board[board_pit] = 0

        # Moves stones around the board (anti-clockwise).
        steps = 0
        while stones_in_hand > 0:
            # Increments steps.
            steps += 1
            # Checks that the the pit is not the opponent's mancala (which is skipped when dropping stones).
            if (board_pit + steps) % 14 != (13 + self.player*7) % 14:
                # Drops a stone into the pit.
                self.board[(board_pit + steps) % 14] += 1
                stones_in_hand -= 1

        # Last pit is found (needed for special rules).
        last_pit = (board_pit + steps) % 14
        ### print("* The last pit was [{}]".format(last_pit))

        # Determines if the last stone landed in the Mancala (collection pit) which means an extra turn.
        if last_pit == 6 + self.player*7:
            print("* The last stone landed in the mancala, player {} takes an additional turn!".format(self.player))

        else:
            # Determines if the last stone landed in an empty pit on your own side which means a capture. (Exception when opposing pit is empty).
            if (last_pit >= self.player*7) and (last_pit < 6 + self.player*7) and (self.board[last_pit] == 1) and (self.board[12 - last_pit] != 0):
                print("* The last stone landed in your own empty pit, capture!")
                self.board[6 + self.player*7] += 1 + self.board[12 - last_pit]
                self.board[last_pit] = 0
                self.board[12 - last_pit] = 0

            # Normal turn where no special rules were invoked
            else:
                print("* No special rules invoked.")
                pass

            # Switches player
            print("##### End of player {}'s turn ######".format(self.player))
            self.player = (self.player + 1) % 2

        self.print_board(self.board)

        # Checks if there are no stones on either side of the board
        if self.board[:6] == [0]*6 or self.board[7:13] == [0]*6:
            print("* No stones on one side of the board. End of game!")

            # Ends game
            self.is_active = False

            # Tallies up stones
            self.board[6] += sum(self.board[:6])
            self.board[13] += sum(self.board[7:13])

            self.result = (self.board[6], self.board[13])

            # Announces winner
            if self.board[6] > self.board[13]:
                print("* Player 0 wins! Score was [{} : {}]".format(
                    self.board[6], self.board[13]))

            elif self.board[6] < self.board[13]:
                print("* Player 1 wins! Score was [{} : {}]".format(
                    self.board[6], self.board[13]))

            else:
                print("* It's a draw! Score was [{} : {}]".format(
                    self.board[6], self.board[13]))

    @staticmethod
    def print_board(boardstate: list):
        """Prints the board.

        Arguments:
            boardstate {list} -- The state of the board.
        """

        # Converts the board list into how the board would look in real life so it is recognisable to humans.
        print()
        print("-"*25)
        print("Current boardstate:")
        print(boardstate[:-8:-1])
        print("  ", boardstate[:7])
        print("-"*25)
        print()

# ---------------------------------------------------------------------------

# RUNNING THE GAME:

if __name__ == "__main__":
    # Pick agent.
    agent = population[rank]
    print("#"*50)
    print("Playing against the agent born in generation {} with {} total wins.".format(
        agent.gen, agent.wins))

    # Create mancala game object.
    game = Human_Friendly_Mancala()

    # Run the game.
    while game.is_active:
        print("Player {}'s turn:".format(game.player))

        # Checks if it's the human's turn.
        if game.player == human:
            user_input = input()

            # Allows for exit out of game.
            if user_input in "exit quit esc end":
                break

            # Validates input and takes turn.
            else:
                try:
                    int(user_input)
                except:
                    print("Invalid input.")
                else:
                    if game.valid_choice(int(user_input)):
                        game.take_turn(int(user_input))

        # Agent plays takes its turn.
        else:
            # Takes the game board and changes into a column vector for the agents to process.
            board_input = np.array(game.board).reshape((len(game.board), 1))

            # Calculates output of the neural network for the given boardstate input.
            output = agent.choose(board_input)

            # Reshapes the output into a list of prioritised choices.
            choices = np.argsort(output.reshape((1, 6)))

            # Test each choice in turn until it finds a valid move.
            n = 0
            while not game.valid_choice(choices[0][n]):
                n += 1

            # Agent takes the first valid move from prioritised choice list.
            print(choices[0][n])
            game.take_turn(choices[0][n])