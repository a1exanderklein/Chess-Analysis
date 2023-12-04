import pandas as pd
import matplotlib.pyplot as plt
import csv
import time
from analyzer import ChessAnalyzer

# chess_dataframe = pd.read_csv(csvFile, delimiter=",", header= 0)
# print(chess_dataframe.head)

print("Welcome to the Chess Meta Analyzer!")
print("What game mode would you like to analyze?\n(1) Blitz\n(2) Rapid\n(3) Classical\n(4) All Modes")

inputMode = '0'
selectedModes = []
mode = ""
#process user input
while inputMode == '0':
    inputMode = input("Enter your choice: ")
    if inputMode == '1':
        selectedModes = ['Rated Blitz game', 'Rated Blitz tournament']
        print("Gathering Data from Rated Blitz mode...")
        mode = "Blitz mode"
    elif inputMode == '2':
        selectedModes = ['Rated Rapid game', 'Rated Rapid tournament']
        print("Gathering Data from Rated Rapid mode...")
        mode = "Rapid mode"
    elif inputMode == '3':
        selectedModes = ['Rated Classical game','Rated Classical tournament']
        print("Gathering Data from Rated Classical mode...")
        mode = "Classical mode"
    elif inputMode == '4':
        selectedModes = ['Rated Blitz game', 'Rated Blitz tournament','Rated Rapid game', 'Rated Rapid tournament','Rated Classical game','Rated Classical tournament']
        print("Gathering Data from All Modes...")
        mode = "All modes"
    else:
        print("Invalid choice. Please enter a valid number.")

analyzer = ChessAnalyzer(selectedModes=selectedModes)
analyzer.openingAnalyzer()
analyzer.winRateAnalyzer()

# Ask which sorting method they want to use
print("Which sorting method would you like to use?\n(1) Merge Sort\n(2) Quick Sort")
chosenSort = '0'

while chosenSort == '0':
    chosenSort = input("Enter your choice: ")
    if chosenSort == '1':
        start = time.time()
        analyzer.mergeSort(analyzer.winRatios)
        end = time.time()
        print(f"Merge sort from {mode} completed in {end-start} seconds")
    elif chosenSort == '2':
        start = time.time()
        analyzer.quickSort(analyzer.winRatios, 0, len(analyzer.winRatios) - 1)
        end = time.time()
        print(f"Quick sort from {mode} completed in {end-start} seconds")
    else:
         print("Invalid choice. Please enter a valid number.")

analyzer.printer()