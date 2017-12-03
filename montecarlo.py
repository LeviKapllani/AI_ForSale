from __future__ import division
import numpy as np
import random
import datetime
import copy
from random import choice
from math import log, sqrt

random.seed("seeed")


class State():
    def __init__(self, player1Cards, player2Cards, player3Cards, money, playersMoney):
        self.player1Cards = player1Cards
        self.player2Cards = player2Cards
        self.player3Cards = player3Cards
        self.money = money
        self.playersMoney = playersMoney

    def __hash__(self):
        return hash((str(self.player1Cards), str(self.player2Cards), str(self.player3Cards)))
        # return hash((str(self.player1Cards), str(self.player2Cards), str(self.player3Cards), str(self.money), str(self.playersMoney)))


class Board():
    # Returns a representation of the starting state of the game.
    def init(self, playerCards):
        if len(playerCards) == 0:
            cards = range(1, 31)
            random.shuffle(cards)
            player1Cards = cards[0:10]
            player2Cards = cards[10:20]
            player3Cards = cards[20:30]
        else:
            player1Cards = playerCards[0]
            player2Cards = playerCards[1]
            player3Cards = playerCards[2]

        playersMoney = [[], [], []]
        money = [0, 0, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8,
                 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15]

        currentPlayer = random.choice([1, 2, 3])
        # new("State",{'player1Cards':player1Cards, "player2Cards":player2Cards, "player3Cards": player3Cards, "money": money, "playersMoney":playersMoney})
        return State(player1Cards, player2Cards, player3Cards, money, playersMoney)

    def next_state(self, state, play):
        # Takes the game state, and the move to be applied.
        # Returns the new game state.

        random.shuffle(state.money)
        roundMoney = sorted(state.money[:3])

        moves = [[0, play[0]], [1, play[1]], [2, play[2]]]

        sortedMoves = sorted(moves, key=lambda x: x[1], reverse=True)

        state.playersMoney[sortedMoves[0][0]].append(roundMoney[2])
        state.playersMoney[sortedMoves[1][0]].append(roundMoney[1])
        state.playersMoney[sortedMoves[2][0]].append(roundMoney[0])

        state.playersMoney[0].sort()
        state.playersMoney[1].sort()
        state.playersMoney[2].sort()

        state.player1Cards.remove(moves[0][1])
        state.player2Cards.remove(moves[1][1])
        state.player3Cards.remove(moves[2][1])

        state.player1Cards.sort()
        state.player2Cards.sort()
        state.player3Cards.sort()

        del state.money[:3]

        state.money.sort()

        return state

    def legal_plays(self, state):
        return [state.player1Cards, state.player2Cards, state.player3Cards]

    def winner(self, state):

        player1Money = sum(state.playersMoney[0])
        player2Money = sum(state.playersMoney[1])
        player3Money = sum(state.playersMoney[2])

        playersTotalMoney = [[1, player1Money], [
            2, player2Money], [3, player3Money]]

        sortedPlayersTotalMoney = sorted(
            playersTotalMoney, key=lambda x: x[1], reverse=True)

        if sortedPlayersTotalMoney[0][1] == sortedPlayersTotalMoney[1][1]:
            if sortedPlayersTotalMoney[0][1] == sortedPlayersTotalMoney[2][1]:
                return 0  # "All tied"
            else:
                # sortedPlayersTotalMoney[0][0] +" and " + sortedPlayersTotalMoney[1][0] + " share the first place."
                return 0
        else:
            return sortedPlayersTotalMoney[0][0]


class MonteCarlo(object):
    def __init__(self, board, initialState, seconds, max_moves):

        self.board = board
        self.calculation_time = datetime.timedelta(seconds=seconds)
        self.states = [initialState]
        self.max_moves = max_moves
        self.plays = {}
        self.wins = {}
        self.gamesWon = 0
        self.gamesPlayed = 0
        self.C = 10.0

    def update(self, state):

        self.states.append(state)

    def reset(self, state):

        self.states = [state]

    def get_play(self):
        # self.max_depth=0
        state = self.states[-1]
        legalMoves = self.board.legal_plays(state)[0]

        if not legalMoves:
            return
        if len(legalMoves) == 1:
            return legalMoves[0]

        games = 0
        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < self.calculation_time:
            self.run_simulation()
            games += 1

        hashedState = hash(state)
        bestMove = legalMoves[0]
        bestMoveWinPercentage = 0
        for move in legalMoves:
            moveWinPercentage = self.wins.get(
                (hashedState, move), 0) / self.plays.get((hashedState, move), 1)
            if moveWinPercentage > bestMoveWinPercentage:
                bestMove = move
                bestMoveWinPercentage = moveWinPercentage

        return bestMove

    def run_simulation(self):
        visited_states = set()
        states_copy = copy.deepcopy(self.states)
        state = states_copy[-1]
        hashedState = hash(state)

        player = 1
        expand = True

        winner = 0

        for t in xrange(100):
            legal = self.board.legal_plays(state)
            play = [0, choice(legal[1]), choice(legal[2])]

            legalPlays = legal[0]
            if(all(self.plays.get((hashedState, legalPlay)) for legalPlay in legalPlays)):
                bestPlayStats = 0
                totalLog = log(
                    sum(self.plays[(hashedState, legalPlay)] for legalPlay in legalPlays))
                for legalPlay in legalPlays:
                    playStats = (self.wins[(hashedState, legalPlay)] / self.plays[(
                        hashedState, legalPlay)]) + self.C * sqrt(totalLog / self.plays[(hashedState, legalPlay)])
                    if playStats > bestPlayStats:
                        bestPlay = legalPlay
            else:
                bestPlay = choice(legalPlays)

            play[0] = bestPlay

            state = self.board.next_state(state, play)
            states_copy.append(state)
            hashedState = hash(state)
            if expand and (hashedState, play[0]) not in self.plays:
                expand = False
                self.plays[(hashedState, play[0])] = 0
                self.wins[(hashedState, play[0])] = 0

            visited_states.add((hashedState, play[0]))

            if len(state.money) == 0:
                winner = self.board.winner(state)
                if winner == 1:
                    self.gamesWon += 1
                self.gamesPlayed += 1
                break

        for hashedState, play in visited_states:
            if (hashedState, play) not in self.plays:
                continue
            self.plays[(hashedState, play)] += 1
            if winner == 1:
                self.wins[(hashedState, play)] += 1


def testing():
    numberOfGames = 0

    a = Board()

    initialState = a.init([])

    mc = MonteCarlo(a, initialState, 1, 100)
    while numberOfGames < 100:

        newState = a.init([])
        mc.reset(newState)
        previousState = newState
        while True:
            aimove = mc.get_play()
            previousState = a.next_state(previousState, [aimove, choice(
                previousState.player2Cards), choice(previousState.player3Cards)])
            mc.update(previousState)
            if len(previousState.money) == 0:
                print a.winner(previousState)
                break

        print mc.gamesPlayed
        if mc.gamesWon > 0:
            break

        numberOfGames += 1


testing()
# print state.money
# nextState = a.next_state(state,[state.player1Cards[0], state.player2Cards[1], state.player3Cards[2]])
# print nextState.money
