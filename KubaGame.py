# Author: Xiuzhu Shao
# Date: 05/23/2021
# Description: This project is an implementation to play the board game Kuba. It consists of a KubaPlayer class that
# represents the player's name, player's color ('W' or 'B'), number of red marbles captured by the player, and number
# of opponent's marbles captured by the player. It also contains the KubaGame class. This class stores the state of the
# board, contains methods for moving pieces left,right,forward, and backwards, and also tracks the current turn and the
# winner of the game. The rules for Kuba can be found here:
# https://sites.google.com/site/boardandpieces/list-of-games/kuba

import copy

class KubaPlayer:
    """
    Represents a Kuba player. This class
    holds the player's name, the player's
    color, the number of red marbles captured
    by the player, and the number of opponent's
    marbles captured by the player.

    The class contains get methods for each
    of these data members as well as methods
    for incrementing the number of red marbles
    and opponent's marbles in the player's inventory.
    """
    def __init__(self, name, color):
        """
        Initializes player object with the
        following attributes:
        name, color, # of red marbles in
        inventory, # of opponent's marbles
        in inventory.
        """
        self._name = name
        self._color = color
        self._red = 0
        self._opponent_marbles = 0

    def get_name(self):
        """
        Returns the player's name.
        """
        return self._name

    def get_color(self):
        """
        Returns the player's color.
        """
        return self._color

    def get_red(self):
        """
        Returns number of red marbles
        captured by the player.
        """
        return self._red

    def get_opponent_marbles(self):
        """
        Returns number of marbles
        of the opponent's color
        that the player has captured.
        """
        return self._opponent_marbles

    def add_red(self):
        """
        Adds a red marble to
        player's inventory.
        """
        self._red += 1

    def add_opponent_marbles(self):
        """
        Adds a marble of the opponent's
        color to the player's inventory.
        """
        self._opponent_marbles += 1


class KubaGame:
    """
    Represents a game of Kuba. This class will
    initialize two KubaPlayer objects in a list,
    as well as the game board. The class contains
    methods for pushing a marble either left, right,
    forwards, or backwards. The class also tracks
    which player's turn it is to play, the winner,
    the number of red, white, and black marbles on
    the board, as well as the no-go move for the
    next turn.
    """
    def __init__(self, pc_tup_1, pc_tup_2):
        """
        Initializes a game object consisting of
        several data members: players list consisting
        of two KubaPlayer objects; the winner and name of
        the player whose turn it is, both initialized
        to None; the board with 13 red marbles, 8 white
        marbles, and 8 black marbles; the no-go
        move (representing the move which would reverse
        the board condition to the previous state left
        by the opponent), also initialized to None; the
        current marble that is captured by the current player
        (stored as a string, initialized to none), and a
        temporary board temp_board, also initialized to
        None.
        """
        self._players = [KubaPlayer(pc_tup_1[0], pc_tup_1[1]),
                         KubaPlayer(pc_tup_2[0], pc_tup_2[1])]
        self._winner = None
        self._turn = None
        self._board = [
            [ "W", "W", "X", "X", "X", "B", "B" ],
            [ "W", "W", "X", "R", "X", "B", "B" ],
            [ "X", "X", "R", "R", "R", "X", "W" ],
            [ "X", "R", "R", "R", "R", "R", "X" ],
            [ "X", "X", "R", "R", "R", "X", "X" ],
            [ "B", "B", "X", "R", "X", "W", "W" ],
            [ "B", "B", "X", "X", "X", "W", "W" ],
        ]
        self._red = 13
        self._white = 8
        self._black = 8
        self._no_go_move = None
        self._captured_marble = None
        self._temp_board = None

    def print_board(self):
        """
        Prints the entire board.
        """
        for row in self._board:
            print(row)

    def get_current_turn(self):
        """
        Returns the player name whose turn it
        is to play the game. If game has not yet
        started, returns None.
        """
        return self._turn

    def make_move(self, playername, coordinates, direction):
        """
        Takes in the player's name, the coordinates of
        the marble the player wants to push, and the
        direction the player wants to push the marble,
        either 'L','R','F', or 'B'. Returns True and
        updates the game state if the move is valid,
        returns False otherwise.
        """

        # Stores the name of the first player to make
        # a move.
        if self._turn is None:
            self._turn = playername

        # On subsequent moves, ensures that the
        # player making a move is obeying the turn order.
        if self._turn != playername:
            return False

        # If game is already over, return False
        if self._winner is not None:
            return False

        # If coordinates are invalid, return False
        for num in coordinates:
            if num < 0 or num > 6:
                return False

        # Retrieves current player object from player
        # list. Stores an integer 0 if the current
        # player is the first object in the list, and
        # a 1 otherwise.
        if self._players[0].get_name() == playername:
            current_player = self._players[0]
            other_player = self._players[1]
            curr = 0
        elif self._players[1].get_name() == playername:
            current_player = self._players[1]
            other_player = self._players[0]
            curr = 1
        else:
            return False    # Invalid playername

        # If marble being moved is not player's marble, or if
        # space is empty:
        if self.get_marble(coordinates) != current_player.get_color():
            return False

        # Confirms whether or not there are legal moves left for
        # the current player. If no moves are left, winner becomes
        # other player's name and move returns False.
        temp_no_go = self._no_go_move   # saves a copy of no-go move
        can_move = False
        for row in range(7):
            for column in range(7):
                cell = self._board[row][column]
                if cell == current_player.get_color():
                    test_left = self.move_left((row,column),current_player)
                    test_right = self.move_right((row,column),current_player)
                    test_forward = self.move_forward((row, column), current_player)
                    test_backward = self.move_backward((row, column), current_player)
                    if test_left or test_right or test_forward or test_backward:
                        # If a move is possible in any direction, loop terminates
                        can_move = True
                        break
        self._no_go_move = temp_no_go   # restores no-go move
        # No legal moves are possible for current player, set winner equal
        # to opponent's name.
        if not can_move:
            self._winner = other_player.get_name()
            return False

        # Attempts to move marble in direction specified. If
        # movement fails due to pushing own marble off of edge
        # or if there is no space for movement, return False.
        # If move undoes last move by opponent, return False
        # Else, updates board and player/board marble counts.
        if direction == 'L':
            temp = self.move_left(coordinates,current_player)
        elif direction == 'R':
            temp = self.move_right(coordinates,current_player)
        elif direction == 'F':
            temp = self.move_forward(coordinates,current_player)
        elif direction == 'B':
            temp = self.move_backward(coordinates,current_player)
        else:   #Direction instruction is invalid
            return False

        if temp:    # If the move is successful.
            if self._captured_marble is not None:   # A marble has been captured
                self.update_marbles(self._captured_marble, current_player)
            self._board = self._temp_board  # Move is real, update real board state.
        if not temp:    # If the move is not successful.
            return False

        # All False checks complete. The method now checks for a
        # winner, updates the turn to be the other player's name,
        # and returns True.

        # Obtains the number of red marbles and opponent's marbles
        # captured by the current player. If the player has captured
        # at least 7 red stones or all 8 of the opponent's marbles,
        # the current player's name is stored as the winner.
        opponent_marbles = current_player.get_opponent_marbles()
        player_red = current_player.get_red()
        if opponent_marbles >= 8 or player_red >= 7:
            self._winner = playername

        # Updates the turn. If current player is first player in
        # the player list, sets turn to be other player's name, and
        # vice versa.
        if curr == 0:
            self._turn = self._players[1].get_name()
        else:
            self._turn = self._players[0].get_name()

        return True

    def move_left(self, coor_tup, player):
        """
        Takes in coordinates as a tuple and
        current player object. Makes a temporary
        board that is a copy of self._board, and
        pushes marble at coordinate left on the
        temporary board. If a marble will be pushed
         off of the edge, save its color under the
         _captured_marble data member. Returns
        False if player will push own marble off of board,
        move is impossible, or move results in duplicating
        board state created by opponent last round.
        Updates the no-go move, if applicable, and
        returns True.
        """
        # Makes a copy of the board
        self._temp_board = copy.deepcopy(self._board)
        self._captured_marble = None    # Assume no marble is captured to begin
        row = coor_tup[0]
        column = coor_tup[1]
        min = 0
        # Inverse bool tracks if a no-go move will
        # need to be created at the end of the move.
        inverse_bool = True

        # If cell to be moved is not at the right edge and
        # value to right of cell is not blank, move is
        # impossible and method returns False.
        if column != 6:
            val = self._temp_board[row][column + 1]
            if val != 'X':
                return False

        # Finds next blank cell in row to the left (if it exists).
        for num in range(column,-1,-1):
            if self._temp_board[row][num] == 'X':
                min = num
                break

        # If blank cell exists to the left, no-go move will
        # not be needed.
        if min != 0:
            inverse_bool = False

        # Piece will be pushed off of edge of board
        if min == 0:
            leftmost = self._temp_board[row][min]
            if leftmost == player.get_color():  # If player is about to push
                # own marble off of edge, return False
                return False
            elif leftmost != 'X':
                # If marbles is pushed off of board, no-go
                # move will not be needed.
                inverse_bool = False
                self._captured_marble = leftmost

        # If move undoes opponent's previous, return False
        if self._no_go_move is not None \
                and coor_tup[0] == self._no_go_move[0] \
                and coor_tup[1] == self._no_go_move[1] \
                and self._no_go_move[2] == 'L':
            return False

        # Move is successful. Updates board,updates
        # no_go_move, and returns True
        for num in range(min,column):
            self._temp_board[row][num] = self._temp_board[row][num+1]
        self._temp_board[row][column] = 'X'

        # Updates no-go move to be the inverse
        # of move that was just performed. Clears out
        # current no-go move if no inverse move is
        # required.
        if inverse_bool is True:
            self._no_go_move = (row,min,'R')
        else:
            self._no_go_move = None

        return True

    def move_right(self, coor_tup, player):
        """
        Takes in coordinates as a tuple and
        current player object. Makes a temporary
        board that is a copy of self._board, and
        pushes marble at coordinate right on the
        temporary board. If a marble will be pushed
         off of the edge, save its color under the
         _captured_marble data member. Returns
        False if player will push own marble off of board,
        move is impossible, or move results in duplicating
        board state created by opponent last round.
        Updates the no-go move, if applicable, and
        returns True.
        """
        # Makes a copy of the board
        self._temp_board = copy.deepcopy(self._board)
        self._captured_marble = None  # Assume no marble is captured to begin
        row = coor_tup[0]
        column = coor_tup[1]
        max = 6
        # Inverse bool tracks if a no-go move will
        # need to be created at the end of the move.
        inverse_bool = True

        # If cell to be moved is not at the left edge and
        # value to left of cell is not blank, move is
        # impossible and method returns False.
        if column != 0:
            val = self._temp_board[row][column - 1]
            if val != 'X':
                return False

        # Finds next blank cell in row to the right (if it exists).
        for num in range(column,7):
            if self._temp_board[row][num] == 'X':
                max = num
                break

        # If blank cell exists to the right, no-go move will
        # not be needed.
        if max != 6:
            inverse_bool = False

        # Piece will be pushed off of edge of board
        if max == 6:
            rightmost = self._temp_board[row][max]
            if rightmost == player.get_color():  # If player is about to push
                # own marble off of edge, return False
                return False
            elif rightmost != 'X':
                # If marbles is pushed off of board, no-go
                # move will not be needed.
                inverse_bool = False
                self._captured_marble = rightmost

        # If move undoes opponent's previous, return False
        if self._no_go_move is not None \
                and coor_tup[0] == self._no_go_move[0] \
                and coor_tup[1] == self._no_go_move[1] \
                and self._no_go_move[2] == 'R':
            return False

        # Move is successful. Updates board and returns True
        for num in range(max,column,-1):
            self._temp_board[row][num] = self._temp_board[row][num - 1]
        self._temp_board[row][column] = 'X'

        # Updates no-go move to be the inverse
        # of move that was just performed. Clears out
        # current no-go move if no inverse move is
        # required.
        if inverse_bool is True:
            self._no_go_move = (row,max,'L')
        else:
            self._no_go_move = None

        return True

    def move_forward(self, coor_tup, player):
        """
        Takes in coordinates as a tuple and
        current player object. Makes a temporary
        board that is a copy of self._board, and
        pushes marble at coordinate forward on the
        temporary board. If a marble will be pushed
         off of the edge, save its color under the
         _captured_marble data member. Returns
        False if player will push own marble off of board,
        move is impossible, or move results in duplicating
        board state created by opponent last round.
        Updates the no-go move, if applicable, and
        returns True.
        """
        # Makes a copy of the board
        self._temp_board = copy.deepcopy(self._board)
        self._captured_marble = None  # Assume no marble is captured to begin
        row = coor_tup[0]
        column = coor_tup[1]
        min = 0
        # Inverse bool tracks if a no-go move will
        # need to be created at the end of the move.
        inverse_bool = True

        # If cell to be moved is not at the bottom edge and
        # value in cell below is not blank, move is
        # impossible and method returns False.
        if row != 6:
            val = self._temp_board[row + 1][column]
            if val != 'X':
                return False

        # Finds next blank cell above in column (if it exists).
        for num in range(row,-1,-1):
            if self._temp_board[num][column] == 'X':
                min = num
                break

        # If blank cell exists above, no-go move will
        # not be needed.
        if min != 0:
            inverse_bool = False

        # Piece will be pushed off of edge of board
        if min == 0:
            topmost = self._temp_board[min][column]
            if topmost == player.get_color():  # If player is about to push
                # own marble off of edge, return False
                return False
            elif topmost != 'X':
                # If marbles is pushed off of board, no-go
                # move will not be needed.
                inverse_bool = False
                self._captured_marble = topmost

        # If move undoes opponent's previous, return False
        if self._no_go_move is not None \
                and coor_tup[0] == self._no_go_move[0] \
                and coor_tup[1] == self._no_go_move[1] \
                and self._no_go_move[2] == 'F':
            return False

        # Move is successful. Updates board and returns True
        for num in range(min,row):
            self._temp_board[num][column] = self._temp_board[num+1][column]
        self._temp_board[row][column] = 'X'

        # Updates no-go move to be the inverse
        # of move that was just performed. Clears out
        # current no-go move if no inverse move is
        # required.
        if inverse_bool is True:
            self._no_go_move = (min,column,'B')
        else:
            self._no_go_move = None

        return True

    def move_backward(self, coor_tup, player):
        """
        Takes in coordinates as a tuple and
        current player object. Makes a temporary
        board that is a copy of self._board, and
        pushes marble at coordinate backward on the
        temporary board. If a marble will be pushed
         off of the edge, save its color under the
         _captured_marble data member. Returns
        False if player will push own marble off of board,
        move is impossible, or move results in duplicating
        board state created by opponent last round.
        Updates the no-go move, if applicable, and
        returns True.
        """
        # Makes a copy of the board
        self._temp_board = copy.deepcopy(self._board)
        self._captured_marble = None  # Assume no marble is captured to begin
        row = coor_tup[0]
        column = coor_tup[1]
        max = 6
        # Inverse bool tracks if a no-go move will
        # need to be created at the end of the move.
        inverse_bool = True

        # If cell to be moved is not at the top edge and
        # value in cell above is not blank, move is
        # impossible and method returns False.
        if row != 0:
            val = self._temp_board[row - 1][column]
            if val != 'X':
                return False

        # Finds next blank cell below in column (if it exists).
        for num in range(row,7):
            if self._temp_board[num][column] == 'X':
                max = num
                break

        # If blank cell exists below, no-go move will
        # not be needed.
        if max != 6:
            inverse_bool = False

        # Piece will be pushed off of edge of board
        if max == 6:
            bottommost = self._temp_board[max][column]
            if bottommost == player.get_color():  # If player is about to push
                # own marble off of edge, return False
                return False
            elif bottommost != 'X':
                # If marbles is pushed off of board, no-go
                # move will not be needed.
                inverse_bool = False
                self._captured_marble = bottommost

        # If move undoes opponent's previous, return False
        if self._no_go_move is not None \
                and coor_tup[0] == self._no_go_move[0] \
                and coor_tup[1] == self._no_go_move[1] \
                and self._no_go_move[2] == 'B':
            return False

        # Move is successful. Updates board and returns True
        for num in range(max,row,-1):
            self._temp_board[num][column] = self._temp_board[num-1][column]
        self._temp_board[row][column] = 'X'

        # Updates no-go move to be the inverse
        # of move that was just performed. Clears out
        # current no-go move if no inverse move is
        # required.
        if inverse_bool is True:
            self._no_go_move = (max,column,'F')
        else:
            self._no_go_move = None
        return True

    def update_marbles(self,cell_captured,player):
        """
        Takes in as input the color of the captured
        marble as well as the player who captured
        the marble. Updates player's marble
        count and board's marble count.
        """
        # Captured marble is red.
        # Updates number of red marbles in
        # player's inventory and the board.
        if cell_captured == 'R':
            player.add_red()
            self._red -= 1
        else:
            # Captured marbles is either
            # white or black. Updates
            # number of opponent marbles in
            # the player's inventory and
            # the number of white/black
            # marbles on the board.
            player.add_opponent_marbles()
            if cell_captured == 'W':
                self._white -= 1
            else:
                self._black -= 1

    def get_winner(self):
        """
        Returns the name of the winning player.
        If no player has won, return None.
        """
        return self._winner

    def get_captured(self, player_name):
        """
        Takes in name of player and returns the
        number of red marbles captured by player.
        """
        for player in self._players:
            if player.get_name() == player_name:
                return player.get_red()

    def get_marble(self, corr_tup):
        """
        Takes in tuple consisting of row and
        column and returns the marble at that
        location on the board. Returns 'X'
        if no marble is found at that location.
        """
        row = corr_tup[0]
        column = corr_tup[1]

        return self._board[row][column]

    def get_marble_count(self):
        """
        Returns the number of White, Black, and
        Red marbles as a tuple in the order (W,B,R).
        """
        return (self._white,self._black,self._red)

    def get_player(self, name):
        """
        Returns player object.
        """
        for player in self._players:
            if player.get_name() == name:
                return player


if __name__ == '__main__':
    game = KubaGame(('PlayerA', 'W'), ('PlayerB', 'B'))
    print(game.get_marble_count())  # returns (8,8,13))
    print(game.get_captured('PlayerA'))  # returns 0
    game.make_move('PlayerA', (6, 5), 'F')
    print(game.get_current_turn())  # returns 'PlayerB' because PlayerA has just played.
    print(game.get_winner())  # returns None
    print(game.make_move('PlayerA', (6, 5), 'L'))  # Cannot make this move, returns False
    print(game.get_marble((5, 5)))  # returns 'W'
    print(game.get_current_turn()) # returns 'PlayerB' because PlayerA is the last player to play.