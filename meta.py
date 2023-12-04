import pandas as pd
import matplotlib.pyplot as plt
import csv
import time

csvFile = 'sep.csv'
# chess_dataframe = pd.read_csv(csvFile, delimiter=",", header= 0)
# print(chess_dataframe.head)

print("Welcome to the Chess Meta Analyzer!")
print("What game mode would you like to analyze?\n(1) Blitz\n(2) Rapid\n(3) Classical\n(4) All Modes")

inputMode = input("Enter your choice: ")
selectedModes = []
mode = ""
#process user input
while inputMode != '1' or inputMode != '2' or inputMode != '3' or inputMode != '4':
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
        print("Invalid choice. Please enter a valid game mode.")


openingData = [] #list of pairs (Opening, # of Occurrences, # of Wins)
with open(csvFile, newline='') as csvfile:
    #creates csv manager for traversing rows
    csvReader = csv.DictReader(csvfile)
    #iterate through each row in the CSV
    for row in csvReader:
        gameMode = row['Event']
        if any(mode in gameMode for mode in selectedModes):
            result = row['Result']
            openingName = row['Opening']
            #do not account for openings with the '?'
            if openingName != "?":
                #check if the opening is already in the list
                found = False
                for openingVector in openingData:
                    if openingVector[0] == openingName:
                        #increment occurrences count
                        openingVector[1] += 1
                        #check if game result is a win (1-0)
                        if result == '1-0':
                            openingVector[2] += 1
                        found = True
                        break

                #if opening not in list, add with initial counts based on the result
                if not found:
                    openingData.append([openingName, 1, 1 if result == '1-0' else 0])

#create separate list for win rates
winRatios = []
for openingStats in openingData:
    name, occurrences, wins = openingStats
    if occurrences > 25:
        successRatio = wins / occurrences if occurrences > 0 else 0
        winRatios.append([name, successRatio])

#display result
# for opening_ratio in winRatios:
#     print(f"Opening: {opening_ratio[0]}, Success Ratio: {opening_ratio[1]}")

#Referenced from DSA Module 6 - Sorting by Amanpreet Kapoor
def quickSort(arr, low, high):
    if low < high:
        pivot  = partition(arr, low, high)
        quickSort(arr, low, pivot - 1)
        quickSort(arr, pivot + 1, high)

def partition(arr, low, high):
    pivot = arr[low][1]
    up = low
    down = high

    while up < down:
        while up < high and arr[up][1] <= pivot:
            up += 1
        while arr[down][1] > pivot:
            down -= 1

        if up < down:
            arr[up], arr[down] = arr[down], arr[up]

    arr[low], arr[down] = arr[down], arr[low]
    return down

def mergeSort(arr):
   
    if len(arr) > 1:
        middle = len(arr)//2
        left = arr[0:middle]
        right = arr[middle:len(arr)]
        mergeSort(left)
        mergeSort(right)
        l = 0
        r = 0
        i = 0
        while l < len(left) and r < len(right):
            if left[l][1] > right[r][1]:
                arr[i] = right[r]
                r = r + 1
                i = i + 1
            else:
                arr[i] = left[l]
                l = l + 1
                i = i + 1
        if l < len(left):
            while l < len(left):
                arr[i] = left[l]
                i = i + 1
                l = l + 1
        if r < len(right):
            while r < len(right):
                arr[i] = right[r]
                i = i + 1
                r = r + 1


# Ask which sorting method they want to use
print("Which sorting method would you like to use?\n(1) Merge Sort\n(2) Quick Sort")
chosenSort = input("Enter your choice: ")

while chosenSort != '1' or chosenSort != '2':
    if chosenSort == '1':
        start = time.time()
        mergeSort(winRatios)
        end = time.time()
        print(f"Merge sort from {mode} completed in {end-start} seconds")
    else if chosenSort == '2':
        start = time.time()
        quickSort(winRatios)
        end = time.time()
        print(f"Quick sort from {mode} completed in {end-start} seconds")

# quickSort(winRatios, 0, len(winRatios) - 1)

for opening_ratio in winRatios:
    print(f"Opening: {opening_ratio[0]}, Success Ratio: {opening_ratio[1]}")