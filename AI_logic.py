from __future__ import division
import numpy as np


cards = range(1, 31)


money = 18


def money_spend1(remaining_cards, state, money):
    if len(state) == 1:
        return 0
    state = np.sort(state)
    average = np.sum(state) / 3.0

    if len(state) == 3:
        d1 = state[1] - state[0]
        d2 = state[2] - state[1]
        avg_difference = (d1 + d2) / 2
        k = avg_difference / 15
    else:
        d1 = state[1] - state[0]
        k = d1 / 30

    i = 1

    for item in remaining_cards:
        if item >= average:
            break
        i += 1

    if len(remaining_cards) != 0:
        money_percentage = ((i - 1) / len(remaining_cards))
    else:
        money_percentage = 1

    money_spent = np.ceil(np.floor(money * money_percentage) * k)

    return money_spent


def money_spend2(remaining_cards, state, money):
    if len(state) == 1:
        return 0
    state = np.sort(state)
    product_of_cards = np.prod(state)
    average = np.floor(product_of_cards**(1. / 3.))

    if len(state) == 3:
        d1 = state[1] - state[0]
        d2 = state[2] - state[1]
        avg_difference = (d1 + d2) / 2
        k = avg_difference / 15
    else:
        d1 = state[1] - state[0]
        k = d1 / 30

    i = 1

    for item in remaining_cards:
        if item >= average:
            break
        i += 1

    if len(remaining_cards) != 0:
        money_percentage = ((i - 1) / len(remaining_cards))
    else:
        money_percentage = 1

    money_spent = np.ceil(np.floor(money * money_percentage) * k)

    return money_spent


def money_spend3(remaining_cards, state, money):
    return 0
