import gamelogic
import montecarlo
import random

random.seed("prump")

numberOfGames = 0

board = montecarlo.Board()

initialPhase2 = board.init([])

mc = montecarlo.MonteCarlo(board, initialPhase2, 1, 100)

winners = [0, 0, 0]

while numberOfGames < 100:
    phase1 = gamelogic.game()
    playerCards = [
        phase1[0].cards,
        phase1[1].cards,
        phase1[2].cards]

    initialPhase2 = board.init(playerCards)

    mc.reset(initialPhase2)

    previousState = initialPhase2

    numberOfGames += 1
    while True:
        aimove = mc.get_play()
        previousState = board.next_state(previousState, [aimove, random.choice(
            previousState.player2Cards), random.choice(previousState.player3Cards)])
        mc.update(previousState)
        if len(previousState.money) == 0:
            winners[board.winner(previousState) - 1] += 1
            break
    if numberOfGames % 10 == 0:
        print numberOfGames
        print winners
