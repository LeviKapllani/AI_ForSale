from __future__ import division
import numpy as np


cards = range(1,31)


money = 16


while len(cards) != 0:

	state=[]
	card1 = input("Please enter a card")
	state = np.append(state,card1)
	card2 = input("Please enter a card")
	state = np.append(state,card2)
	card3 = input("Please enter a card")
	state = np.append(state,card3)

	state = np.sort(state)
	state1 = [1*state[0],2*state[1],3*state[2]]
	average = np.sum(state)/3.0

	remaining_cards = list(filter(lambda card: card not in state,cards ))

	i = 1

	for item in remaining_cards:
		if item >= average:
			break
		i += 1

	if len(remaining_cards) != 0:
		money_percentage = ((i-1)/len(remaining_cards))
	else:
		money_percentage = 1

	money_spent = np.floor(money*money_percentage)

	print money_spent


	money_spent1 = input("Please enter money spent this round")

	money = money - money_spent1

	cards = remaining_cards


