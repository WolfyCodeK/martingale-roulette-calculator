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
    writer.writerow(['Pot', 'Bet', 'Winrate', 'Time(hours)', 'Profit'])

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
                
        # Print Results
        hours = round((i * spinMinutes) / 60, 3)
        
        if (pot < startingPot): 
            lossTally += 1
        else:
            profit = round(profit, 2)
            
            winTally += 1
            totalProfit += profit
            totalPlayTime += hours
            
        j += 1

    totalGamesPlayed = winTally + lossTally
    winRate = round(winTally / (totalGamesPlayed) * 100, 3)
    averageTimePlayed = round((totalPlayTime / winTally), 2)
    averageProfit = round((totalProfit / winTally), 2)

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
