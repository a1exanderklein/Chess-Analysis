import time
from analyzer import ChessAnalyzer

notExited = True
print("\033[34m\033[1mWelcome to the Chess Meta Analyzer!\033[0m")

print("What game mode would you like to analyze?\n(1) Blitz\n(2) Rapid\n(3) Classical\n(4) All Modes")
inputMode = '0'
selectedModes = []
mode = ""
#process user input
selectedInput = False
while selectedInput == False:
    inputMode = input("Enter your choice: ")
    print()
    if inputMode == '1':
        selectedModes = ['Rated Blitz game', 'Rated Blitz tournament']
        selectedInput = True
        mode = "Blitz Mode"
    elif inputMode == '2':
        selectedModes = ['Rated Rapid game', 'Rated Rapid tournament']
        mode = "Rapid Mode"
        selectedInput = True
    elif inputMode == '3':
        selectedModes = ['Rated Classical game','Rated Classical tournament']
        mode = "Classical Mode"
        selectedInput = True
    elif inputMode == '4':
        selectedModes = ['Rated Blitz game', 'Rated Blitz tournament','Rated Rapid game', 'Rated Rapid tournament','Rated Classical game','Rated Classical tournament']
        mode = "All Modes"
        selectedInput = True
    else:
        print("Invalid choice. Please enter a valid number.")

print(f"Gathering Data from {mode}...\n")
analyzer = ChessAnalyzer(selectedModes=selectedModes)

while notExited:
    print("What data would you like to analyze?\n(1) Opening data\n(2) Player data\n(3) Highest Ranked Games\n(4) Exit")
    inputQuery = input("Enter your Choice: ")
    print()
    if inputQuery == '1': #Opening Data
        print("Sorting Opening data (Comparing Merge & Quick Sort)...\n")
        analyzer.openingAnalyzer()
        start = time.time()
        analyzer.mergeSort(analyzer.winRatios)
        end = time.time()
        print(f"Merge sort completed in {round((end-start), 3)} seconds")
        start = time.time()
        analyzer.quickSort(analyzer.winRatios2, 0, len(analyzer.winRatios2)-1)
        end = time.time()
        print(f"Quick sort completed in {round((end-start), 3)} seconds")
        print()

        analyzer.printer()
        print("How many of the most successful openings would you like to see?")
        numOpenings = input("Enter a numeric value: ")
        analyzer.openingPrinter(int(numOpenings))

    elif inputQuery == '2': #Player data
        print("Sorting Player data...\n")
        analyzer.playerAnalyzer()
        name = input ("Enter name of player: ")
        analyzer.getPlayerOpeningUsage(name)
        print()

    elif inputQuery == '3': #ELO Data
        print("Sorting ELO data (Comparing Merge & Quick Sort)...\n")
        analyzer.eloAnalyzer()

        start = time.time()
        analyzer.mergeSort(analyzer.eloData2)
        end = time.time()
        print(f"Merge sort completed in {round((end-start), 3)} seconds")
        start = time.time()
        analyzer.quickSort(analyzer.eloData, 0, len(analyzer.eloData) - 1)
        end = time.time()
        print(f"Quick sort completed in {round((end-start), 3)} seconds")
        print()

        print("How many of the highest ranked matches would you like to see?")
        numMatches = input("Enter a numeric value: ")
        analyzer.eloPrinter(int(numMatches))
    
    elif inputQuery == '4': #Exit Program
        notExited = False
        print("Bye!")
    else:
        print("Invalid choice. Please enter a valid number.")
    analyzer.wipe()