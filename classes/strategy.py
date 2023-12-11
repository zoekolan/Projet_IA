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

    def max_value(self, _board_state, alpha, beta):
        if logic.is_game_over(self.player_opponent, _board_state)!= None:
            return self.utility( _board_state), None
        value = -math.inf
        action = None
        for a in logic.get_possible_moves(_board_state) :
            new_board = self.result(self.player, _board_state, a)
            v2, a2 = self.min_value(new_board, alpha, beta)
            if v2 > value :
                value = v2
                action = a
                alpha = max(alpha, value)
            if value >= beta:
                return value, action
        return value, action

    def min_value(self, _board_state, alpha, beta):
        if logic.is_game_over(self.player, _board_state) != None:
            return self.utility( _board_state), None
        value = math.inf
        action = None
        for a in logic.get_possible_moves(_board_state):
            new_board = self.result(self.player_opponent, _board_state, a)
            v2, a2 = self.max_value(new_board, alpha, beta)
            if v2 < value :
                value = v2
                action = a
                beta = min(beta, value)
            if value <= alpha:
                return value, action
        return value, action

    def start(self):
        return self.max_value(self.root_state, -math.inf, math.inf)[1]

class MiniMaxEval(PlayerStrat):
    # Build here the class implementing the MiniMax strategy
    def __init__(self, _board_state, player):
        super().__init__(_board_state, player)
        self.player = player
        self.player_opponent = 3 - player
        self.depth = 0

    def generate_hex_weights(self, n):
        weights = [[0 for _ in range(n)] for _ in range(n)]

        # Poids pour les bords
        border_weight = 50
        for i in range(n):
            for j in range(n):
                if i == 0 or i == n - 1 or j == 0 or j == n - 1:
                    weights[i][j] = border_weight

        # Poids pour le centre
        center_weight = 100
        if n % 2 != 0:
            weights[n // 2][n // 2] = center_weight
        else:
            weights[n // 2 - 1][n // 2 - 1] = center_weight
            weights[n // 2][n // 2] = center_weight

        # Poids pour les positions adjacentes au centre
        adjacent_center_weight = 80
        for i in range(n):
            for j in range(n):
                if (
                    (i, j) != (n // 2, n // 2)
                    and abs(i - n // 2) <= 1
                    and abs(j - n // 2) <= 1
                ):
                    weights[i][j] = adjacent_center_weight

        return weights

    def utility(self, _board_state):
        """Return le poids total du board - on cherhce à maximiser ce poids."""
        weights = self.generate_hex_weights(len(_board_state))
        myweight = 0
        opponentweight = 0

        for coord in logic.get_player_tiles(_board_state, self.player):
            myweight += weights[coord[0]][coord[1]]

        for coord in logic.get_player_tiles(_board_state, self.player_opponent):
            opponentweight += weights[coord[0]][coord[1]]

        return myweight - opponentweight

    def result(self, player, _board_state, move):
        """Place a marker for current player on square."""
        new_board = _board_state.copy()
        new_board[move] = player
        return new_board

    def max_value(self, _board_state, alpha, beta):
        if logic.is_game_over(self.player, _board_state)!= None:
            return 10000, None
        if self.depth >= 5:
            return self.utility(_board_state), None

        value = -math.inf
        action = None
        for a in logic.get_possible_moves(_board_state) :
            new_board = self.result(self.player, _board_state, a)
            v2, a2 = self.min_value(new_board, alpha, beta)
            if v2 > value :
                value = v2
                action = a
                alpha = max(alpha, value)
            if value >= beta:
                return value, action
        self.depth += 1
        return value, action

    def min_value(self, _board_state, alpha, beta):
        if logic.is_game_over(self.player_opponent, _board_state)!= None:
            return -10000, None
        if self.depth >= 5:
            return self.utility(_board_state), None

        value = math.inf
        action = None
        for a in logic.get_possible_moves(_board_state):
            new_board = self.result(self.player_opponent, _board_state, a)
            v2, a2 = self.max_value(new_board, alpha, beta)
            if v2 < value :
                value = v2
                action = a
                beta = min(beta, value)
            if value <= alpha:
                return value, action
        self.depth += 1
        return value, action

    def start(self):
        return self.max_value(self.root_state, -math.inf, math.inf)[1]

class MiniMaxCross(PlayerStrat):
    # Build here the class implementing the MiniMax strategy
    def __init__(self, _board_state, player):
        super().__init__(_board_state, player)
        self.player = player
        self.player_opponent = 3 - player
        self.depth = 0

    def generate_hex_weights_with_cross(self, n):
        weights = [[0 for _ in range(n)] for _ in range(n)]

        # Poids pour les bords
        border_weight = 50
        for i in range(n):
            for j in range(n):
                if i == 0 or i == n - 1 or j == 0 or j == n - 1:
                    weights[i][j] = border_weight

        # Poids pour le centre
        center_weight = 100
        if n % 2 != 0:
            weights[n // 2][n // 2] = center_weight
        else:
            weights[n // 2 - 1][n // 2 - 1] = center_weight
            weights[n // 2][n // 2] = center_weight

        # Poids pour la croix centrale
        cross_weight = 80
        for i in range(n):
            weights[i][n // 2] = cross_weight
            weights[n // 2][i] = cross_weight

        return weights

    def utility(self, _board_state):
        """Return le poids total du board - on cherhce à maximiser ce poids."""
        weights = self.generate_hex_weights_with_cross(len(_board_state))
        myweight = 0
        opponentweight = 0

        for coord in logic.get_player_tiles(_board_state, self.player):
            myweight += weights[coord[0]][coord[1]]

        for coord in logic.get_player_tiles(_board_state, self.player_opponent):
            opponentweight += weights[coord[0]][coord[1]]

        return myweight - opponentweight

    def result(self, player, _board_state, move):
        """Place a marker for current player on square."""
        new_board = _board_state.copy()
        new_board[move] = player
        return new_board

    def max_value(self, _board_state, alpha, beta):
        if logic.is_game_over(self.player, _board_state)!= None:
            return 10000, None
        if self.depth >= 5:
            return self.utility(_board_state), None

        value = -math.inf
        action = None
        for a in logic.get_possible_moves(_board_state) :
            new_board = self.result(self.player, _board_state, a)
            v2, a2 = self.min_value(new_board, alpha, beta)
            if v2 > value :
                value = v2
                action = a
                alpha = max(alpha, value)
            if value >= beta:
                return value, action
        self.depth += 1
        return value, action

    def min_value(self, _board_state, alpha, beta):
        if logic.is_game_over(self.player_opponent, _board_state)!= None:
            return -10000, None
        if self.depth >= 5:
            return self.utility(_board_state), None

        value = math.inf
        action = None
        for a in logic.get_possible_moves(_board_state):
            new_board = self.result(self.player_opponent, _board_state, a)
            v2, a2 = self.max_value(new_board, alpha, beta)
            if v2 < value :
                value = v2
                action = a
                beta = min(beta, value)
            if value <= alpha:
                return value, action
        self.depth += 1
        return value, action

    def start(self):
        return self.max_value(self.root_state, -math.inf, math.inf)[1]

str2strat = { #: dict[str, PlayerStrat]
        "human": None,
        "random": Random,
        "minimax": MiniMax,
        "minimaxeval": MiniMaxEval,
        "minimaxcross": MiniMaxCross,
    }
