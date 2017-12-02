from __future__ import division
import numpy as np
import AI_logic
import random


class Player:
    def __init__(self, money, money_spend):
        self.money = money
        self.cards = []
        self.current_bet = 0
        self.money_spend = money_spend


def game():
    cards = range(1, 31)

    players = [Player(18, AI_logic.money_spend1), Player(
        18, AI_logic.money_spend1), Player(18, AI_logic.money_spend1)]

    starting_player = random.choice([0, 1, 2])
    while len(cards) != 0:

        card1 = random.choice(cards)
        cards.remove(card1)
        card2 = random.choice(cards)
        cards.remove(card2)
        card3 = random.choice(cards)
        cards.remove(card3)

        round = [card1, card2, card3]
        remaining_players = [0, 1, 2]
        next_bet = 1

        for player in players:
            player.current_bet = 0

        i = starting_player
        while len(remaining_players) != 0:
            current_player_id = remaining_players[i]
            current_player = players[current_player_id]

            money_limit = current_player.money_spend(
                cards, round, current_player.money)
            if money_limit >= next_bet:

                if i == len(remaining_players) - 1:
                    i = 0
                else:
                    i += 1
                current_player.current_bet = next_bet
                next_bet += 1

            else:
                money_lost = current_player.current_bet if len(
                    round) == 1 else np.ceil(current_player.current_bet / 2)
                lowest_remaining_card = np.sort(round)[0]
                round.remove(lowest_remaining_card)
                current_player.cards.append(lowest_remaining_card)
                current_player.money -= money_lost
                remaining_players.remove(current_player_id)
                if i == len(remaining_players):
                    i = 0
            players[current_player_id] = current_player
            starting_player = current_player_id

    return players


def test():
    max_games = 1000
    total_games_winners = []
    total_wins_for_player = [0, 0, 0]
    while max_games != 0:

        game_state = game()
        current_game = [np.sum(game_state[0].cards) + game_state[0].money, np.sum(
            game_state[1].cards) + game_state[1].money, np.sum(game_state[2].cards) + game_state[2].money]

        winners_points = np.max(current_game)

        player = 0
        for i in current_game:
            if i == winners_points:
                winner = player
            player += 1

        total_games_winners.append([winner, winners_points])
        total_wins_for_player[winner] += 1
        max_games -= 1

    print total_wins_for_player
