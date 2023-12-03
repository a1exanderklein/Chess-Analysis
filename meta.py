import pandas as pd
import matplotlib.pyplot as plt
import csv

csvFile = 'sep.csv'
# chess_dataframe = pd.read_csv(csvFile, delimiter=",", header= 0)
# print(chess_dataframe.head)

print("Welcome to the Chess Meta Analyzer!")
print("What game mode would you like to analyze?\n(1) Blitz\n(2) Rapid\n(3) Classical\n(4) All Modes")

inputMode = input("Enter your choice: ")
selectedModes = []
#process user input
if inputMode == '1':
    selectedModes = ['Rated Blitz game', 'Rated Blitz tournament']
    print("Gathering Data from Rated Blitz mode...")
elif inputMode == '2':
    selectedModes = ['Rated Rapid game', 'Rated Rapid tournament']
    print("Gathering Data from Rated Rapid mode...")
elif inputMode == '3':
    selectedModes = ['Rated Classical game','Rated Classical tournament']
    print("Gathering Data from Rated Classical mode...")
elif inputMode == '4':
    selectedModes = ['Rated Blitz game', 'Rated Blitz tournament','Rated Rapid game', 'Rated Rapid tournament','Rated Classical game','Rated Classical tournament']
    print("Gathering Data from All Modes...")
else:
    print("Invalid choice. Please enter a valid game mode.")


openingData = [] #list of pairs (Opening, # of Occurrences)
with open(csvFile, newline='') as csvfile:
    #creates csv manager for traversing rows
    csvReader = csv.DictReader(csvfile)
    #iterate through each row in the CSV
    for row in csvReader:
        gameMode = row['Event']
        if any(mode in gameMode for mode in selectedModes):
            result = row['Result']
            openingName = row['Opening']

            # Check if the opening is already in the list
            found = False
            for openingVector in openingData:
                if openingVector[0] == openingName:
                    # Increment occurrences count
                    openingVector[1] += 1
                    # Check if the game result is a win (1-0)
                    if result == '1-0':
                        openingVector[2] += 1
                    found = True
                    break

            # If opening not in list, add with initial counts based on the result
            if not found:
                openingData.append([openingName, 1, 1 if result == '1-0' else 0])

#create separate list for win rates
winRatios = []
for openingStats in openingData:
    name, occurrences, wins = openingStats
    if occurrences > 25:
        success_ratio = wins / occurrences if occurrences > 0 else 0
        winRatios.append([name, success_ratio])

#display result
for opening_ratio in winRatios:
    print(f"Opening: {opening_ratio[0]}, Success Ratio: {opening_ratio[1]}")