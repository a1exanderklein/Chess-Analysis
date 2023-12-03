import pandas as pd
import matplotlib.pyplot as plt
import csv

csvFile = 'sep.csv'
# chess_dataframe = pd.read_csv(csvFile, delimiter=",", header= 0)
# print(chess_dataframe.head)

print("Welcome to the Chess Meta Analyzer!")
print("What game mode would you like to analyze?\n-Rated Blitz\n-Rated Rapid\n-Rated Classical\n-Blitz\n-Rapid\n-Classical\n-All Modes")

inputMode = input("Enter your choice: ")
selected = ""
#process user input
if inputMode.lower() == 'rated blitz':
    selected = ""
    print("Analyzing Rated Blitz mode...")
elif inputMode.lower() == 'rated rapid':
    print("Analyzing Rated Rapid mode...")
elif inputMode.lower() == 'rated classical':
    print("Analyzing Rated Classical mode...")
elif inputMode.lower() == 'blitz':
    print("Analyzing Blitz mode...")
elif inputMode.lower() == 'rapid':
    print("Analyzing Rapid mode...")
elif inputMode.lower() == 'classical':
    print("Analyzing Classical mode...")
elif inputMode.lower() == 'all modes':
    print("Analyzing All Modes...")
else:
    print("Invalid choice. Please enter a valid game mode.")


openingOccurrences = [] #list of pairs (Opening, # of Occurrences)
with open(csvFile, newline='') as csvfile:
    #creates csv manager for traversing rows
    csvReader = csv.DictReader(csvfile)
    #iterate through each row in the CSV
    for row in csvReader:
        openingName = row['Opening']
        #check if opening already in list
        found = False
        for openingPair in openingOccurrences:
            if openingPair[0] == openingName:
                #increment occurrence count
                openingPair[1] += 1
                found = True
                break
        #if opening not in list, add with occurrence count of 1
        if not found:
            openingOccurrences.append([openingName, 1])

for openingPair in openingOccurrences:
    print(f"Opening: {openingPair[0]}, Occurrences: {openingPair[1]}")
