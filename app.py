import random
import time
import csv

""" 
0 = red
1 = black
"""

"""
notes

seprate stats that use profits and those that only use original pot
"""

def makeBet():
    win = False
    
    greenRoll = random.randint(0, 37)
    colourGuess = random.randint(0, 1)
    
    if (greenRoll == greenNum):
        win = False
    else:
        colourRoll = random.randint(0, 1)
        if (colourGuess == colourRoll):
            win = True
    
    return win

startingPot = int(input("Starting Pot -> "))
startingBet = 0.1
spinMinutes = 3
startTime = time.time()

csvPath = f'stats/pot({startingPot}).csv'

with open(csvPath, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',',
                            quotechar=' ', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Pot', 'Bet', 'Winrate', 'Time', 'Profit'])

while (startingBet < startingPot):
    winTally = 0
    lossTally = 0
    totalProfit = 0
    totalPlayTime = 0

    j = 0
    greenNum = random.randint(0, 37)

    while (j < 10000):
        pot = startingPot
        lossStreak = 0
        profit = 0
        i = 1

        #print(f'{i}: pot({pot}), bet({startingBet}), lossStreak({lossStreak})')

        # Play Roulette
        while ((i < (60 / spinMinutes) or lossStreak > 0) and pot > 0):
            bet = startingBet * (pow(2, lossStreak))
            i += 1
                
            # Stop from betting more than available
            if (bet > pot):
                bet = pot     
                
            if (makeBet()):  
                pot += bet
                bet = startingBet
                lossStreak = 0
                profit = (pot - startingPot)
            else:
                lossStreak += 1
                pot -= bet
                
            #print(f'{i}: pot({round(pot, 2)}), bet({bet}), lossStreak({lossStreak})')
                
        # Print Results
        hours = round((i * spinMinutes) / 60, 3)
        #print(f'Time played: {hours} hours ')
        
        if (pot < startingPot): 
            lossTally += 1
            #print(f'Probability Loss: {round((1 / pow(2, lossStreak)) * 100, 3)}')
        else:
            profit = round(profit, 2)
            #print(f'Profit: ({profit})')
            
            winTally += 1
            totalProfit += profit
            totalPlayTime += hours
            
        j += 1

    totalGamesPlayed = winTally + lossTally
    winRate = round(winTally / (totalGamesPlayed) * 100, 3)
    averageTimePlayed = round((totalPlayTime / winTally), 2)
    averageProfit = round((totalProfit / winTally), 2)
    #print("")
    #print(f'Win Rate: {winRate}%')
    #print(f'Average profit: {averageProfit}')
    #print(f'Average time played: {averageTimePlayed}')

    # Write to CSV
    with open(csvPath, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                                quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([startingPot, startingBet, winRate, averageTimePlayed, averageProfit])
        
    startingBet = startingBet * 2
    totalProfit = 0
    totalPlayTime = 0
    
runTime = round((time.time() - startTime), 3)
print(f'--- {runTime} seconds ---')
