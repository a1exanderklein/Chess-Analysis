import pandas as pd
import matplotlib.pyplot as plt
import csv
import time
from analyzer import ChessAnalyzer

# chess_dataframe = pd.read_csv(csvFile, delimiter=",", header= 0)
# print(chess_dataframe.head)

notExited = True
print("Welcome to the Chess Meta Analyzer!")
while notExited:
    print("What game mode would you like to analyze?\n(1) Blitz\n(2) Rapid\n(3) Classical\n(4) All Modes")

    inputMode = '0'
    selectedModes = []
    mode = ""
    #process user input
    selectedInput = False
    while selectedInput == False:
        inputMode = input("Enter your choice: ")
        if inputMode == '1':
            selectedModes = ['Rated Blitz game', 'Rated Blitz tournament']
            selectedInput = True
            mode = "Blitz mode"
        elif inputMode == '2':
            selectedModes = ['Rated Rapid game', 'Rated Rapid tournament']
            mode = "Rapid mode"
            selectedInput = True
        elif inputMode == '3':
            selectedModes = ['Rated Classical game','Rated Classical tournament']
            mode = "Classical mode"
            selectedInput = True
        elif inputMode == '4':
            selectedModes = ['Rated Blitz game', 'Rated Blitz tournament','Rated Rapid game', 'Rated Rapid tournament','Rated Classical game','Rated Classical tournament']
            mode = "All"
            selectedInput = True
        else:
            print("Invalid choice. Please enter a valid number.")


    analyzer = ChessAnalyzer(selectedModes=selectedModes)

    selectedQuery = False
    print("What data would you like to analyze?\n(1) Opening win rate data\n(2) Player win rate data\n(3) Exit Analyzer")
    while selectedQuery == False:
        inputQuery = input("Enter your Choice: ")
        if inputQuery == '1':
            print(f"Gathering Data from {mode} mode...\n")
            selectedQuery = True
            analyzer.openingAnalyzer()
            print("How many of the most successful openings would you like to see?")
            numOpenings = input("Enter a numeric value: ")
            print(f"Sorting Opening data for the {numOpenings} most successful openings...\n")

            start = time.time()
            analyzer.mergeSort(analyzer.winRatios)
            end = time.time()
            print(f"Merge sort completed in {end-start} seconds")

            analyzer.openingPrinter(int(numOpenings))

        elif inputQuery == '2':
            print(f"Gathering Data from {mode} mode...\n")
            print("Sorting Player data...\n")
            selectedQuery = True
            analyzer.playerAnalyzer()
        elif inputQuery == '3':
            notExited = False
            selectedQuery = True
            print("Bye!")
        else:
            print("Invalid choice. Please enter a valid number.")

    # Ask which sorting method they want to use
    # print("Which sorting method would you like to use?\n(1) Merge Sort\n(2) Quick Sort")
    # chosenSort = '0'

    # while chosenSort == '0':
    #     chosenSort = input("Enter your choice: ")
    #     if chosenSort == '1':
    #         start = time.time()
    #         analyzer.mergeSort(analyzer.winRatios)
    #         end = time.time()
    #         print(f"Merge sort from {mode} completed in {end-start} seconds")
    #     elif chosenSort == '2':
    #         start = time.time()
    #         analyzer.quickSort(analyzer.winRatios, 0, len(analyzer.winRatios) - 1)
    #         end = time.time()
    #         print(f"Quick sort from {mode} completed in {end-start} seconds")
    #     else:
    #          print("Invalid choice. Please enter a valid number.")

    # analyzer.printer()