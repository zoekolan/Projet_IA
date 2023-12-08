import copy
import math
import random
from math import log, sqrt, inf
from random import randrange
import numpy as np
from rich.table import Table
from rich.progress import track
from rich.console import Console
from rich.progress import Progress
#import classes.game as game
import classes.logic as logic

# When implementing a new strategy add it to the `str2strat`
# dictionary at the end of the file


class PlayerStrat:
    def __init__(self, _board_state, player):
        self.root_state = _board_state
        self.player = player

    def start(self):
        """
        This function select a tile from the board.

        @returns    (x, y) A tuple of integer corresponding to a valid
                    and free tile on the board.
        """
        raise NotImplementedError

class Node(object):
    """
    This class implements the main object that you will manipulate : nodes.
    Nodes include the state of the game (i.e. the 2D board), children (i.e. other children nodes), a list of
    untried moves, etc...
    """
    def __init__(self, board, move=(None, None),
                 wins=0, visits=0, children=None):
        # Save the #wins:#visited ratio
        self.state = board
        self.move = move
        self.wins = wins
        self.visits = visits
        self.children = children or []
        self.parent = None
        self.untried_moves = logic.get_possible_moves(board)

    def add_child(self, child):
        child.parent = self
        self.children.append(child)


class Random(PlayerStrat):
    # Build here the class for a random player
    def init(self, _board_state, player):
        super().init(_board_state, player)

    def start(self):
        return random.choice(logic.get_possible_moves(self.root_state))

class MiniMax(PlayerStrat):
    # Build here the class implementing the MiniMax strategy
    def __init__(self, _board_state, player):
        super().__init__(_board_state, player)
        print(player)
        self.player = player
        self.player_opponent = 3 - player

    def utility(self, _board_state):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        if logic.is_game_over(self.player, _board_state) == self.player:
            utility = 1
        elif logic.is_game_over(self.player_opponent, _board_state) == self.player_opponent:
            utility = -1

        return utility

    def result(self, player, _board_state, move):
        """Place a marker for current player on square."""
        new_board = _board_state.copy()
        new_board[move] = player
        return new_board

    #def max_value(_board_state, player):
    def max_value(self, _board_state):
        if logic.is_game_over(self.player_opponent, _board_state)!= None:
            #print("game over", logic.is_game_over(self.player, _board_state))
            return self.utility( _board_state), None
        value = -math.inf
        action = None
        actionsPossibles = logic.get_possible_moves(_board_state)
        #print("actions_max", len(actionsPossibles))
        for a in actionsPossibles :
            new_board = self.result(self.player, _board_state, a)
            v2, a2 = self.min_value(new_board)
            #v2, a2 = min_value(_board_state, player)
            #print("Max - v2 et value",v2, value)
            #print("Player dans Max  - ", player)
            #input()
            if v2 > value :
                value = v2
                action = a
        return value, action

    def min_value(self, _board_state):
        #player_op = 1 if player == 2 else 2
        if logic.is_game_over(self.player, _board_state) != None:
            return self.utility( _board_state), None
        value = math.inf
        action = None
        actionsPossibles = logic.get_possible_moves(_board_state)
        #print("actions_min", len(actionsPossibles))
        for a in actionsPossibles:
            new_board = self.result(self.player_opponent, _board_state, a)
            v2, a2 = self.max_value(new_board)
            #print("Min - v2 et value",v2, value)
            #print("Player dans Min  - ", player)
            #input()
            if v2 < value :
                value = v2
                action = a
        return value, action

    def start(self):
        return self.max_value(self.root_state)[1]

str2strat = { #: dict[str, PlayerStrat]
        "human": None,
        "random": Random,
        "minimax": MiniMax,
    }
