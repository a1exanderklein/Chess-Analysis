import csv

class ChessAnalyzer:
    def __init__(self, selectedModes=None):
        self.csvFile = 'sep.csv'
        self.selectedModes = selectedModes if selectedModes is not None else []
        self.mode = ""
        self.eloData = []
        self.eloData2 = []
        self.openingData = []
        self.playerData = {}
        self.winRatios = []
        self.winRatios2 = []
        self.playerOpeningUsage = {}

    def wipe(self):
        self.eloData = []
        self.eloData2 = []
        self.openingData = []
        self.playerData = {}
        self.winRatios = []
        self.winRatios2 = []
        self.playerOpeningUsage = {}

    def printer(self):
        for opening_ratio in self.winRatios:
            print(f"Opening: {opening_ratio[0]}, Success Ratio: {opening_ratio[1]}")

    def eloAnalyzer(self, all):
        with open(self.csvFile, newline='') as csvfile:
            #creates csv manager for traversing rows
            csvReader = csv.DictReader(csvfile)
            #iterate through each row in the CSV
            for row in csvReader:
                gameMode = row['Event']
                # if gameMode in self.selectedModes:
                if all:
                    whitePlayerName = row['White']
                    blackPlayerName = row['Black']
                    whitePlayerElo = row['WhiteElo']
                    blackPlayerElo = row['BlackElo']
                    whiteRatingDiff = row['WhiteRatingDiff']
                    opening = row['Opening']
                    result = row['Result']

                    whitePlayerElo = int(whitePlayerElo) if whitePlayerElo.isdigit() else None
                    blackPlayerElo = int(blackPlayerElo) if blackPlayerElo.isdigit() else None

                    #add list of data to eloData list
                    self.eloData.append([opening, whitePlayerElo, blackPlayerElo, whitePlayerName, blackPlayerName, whiteRatingDiff, result, gameMode])
                else:
                    if gameMode in self.selectedModes:
                        whitePlayerName = row['White']
                        blackPlayerName = row['Black']
                        whitePlayerElo = row['WhiteElo']
                        blackPlayerElo = row['BlackElo']
                        whiteRatingDiff = row['WhiteRatingDiff']
                        opening = row['Opening']
                        result = row['Result']

                        whitePlayerElo = int(whitePlayerElo) if whitePlayerElo.isdigit() else None
                        blackPlayerElo = int(blackPlayerElo) if blackPlayerElo.isdigit() else None

                        #add list of data to eloData list
                        self.eloData.append([opening, whitePlayerElo, blackPlayerElo, whitePlayerName, blackPlayerName, whiteRatingDiff, result, gameMode])
        self.eloData2 = self.eloData

    def openingAnalyzer(self):
        with open(self.csvFile, newline='') as csvfile:
            #creates csv manager for traversing rows
            csvReader = csv.DictReader(csvfile)
            #iterate through each row in the CSV
            for row in csvReader:
                gameMode = row['Event']
                if any(mode in gameMode for mode in self.selectedModes):
                    result = row['Result']
                    openingName = row['Opening']
                    #do not account for openings with the '?'
                    if openingName != "?":
                        #check if the opening is already in the list
                        found = False
                        for openingVector in self.openingData:
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
                            self.openingData.append([openingName, 1, 1 if result == '1-0' else 0])
            for openingStats in self.openingData:
                name, occurrences, wins = openingStats #what is in the lists in the opening data list
                if occurrences > 15: #only if it occurs over 15 to eliminate noise of 100% success rates in few games
                    successRatio = wins / occurrences if occurrences > 0 else 0
                    self.winRatios.append([name, successRatio])
            self.winRatios2 = self.winRatios

    def playerAnalyzer(self):
        with open(self.csvFile, newline='') as csvfile:
            #creates csv manager for traversing rows
            csvReader = csv.DictReader(csvfile)
            #iterate through each row in the CSV
            for row in csvReader:
                gameMode = row['Event']
                if any(mode in gameMode for mode in self.selectedModes):
                    result = row['Result']
                    playerName = row['White']
                    playerELO = row['WhiteElo']
                    #check if the player is already in the list
                        # Initialize player data in dictionary if not already present
                    if playerName not in self.playerData:
                        self.playerData[playerName] = {'ELO': playerELO, 'Occurrences': 0, 'Wins': 0}
                    #increment occurrences
                    self.playerData[playerName]['Occurrences'] += 1
                    #if result is a win (1-0) increment wins
                    if result == '1-0':
                        self.playerData[playerName]['Wins'] += 1
                    #if found elo > current recorded elo
                    if playerELO > self.playerData[playerName]['ELO']:
                        self.playerData[playerName]['ELO'] = playerELO

    def getPlayerOpeningUsage(self, name):
        if name not in self.playerData:
            print("Player Not Found.")
            return
        if name not in self.playerOpeningUsage:
            self.playerOpeningUsage[name] = {}

        with open(self.csvFile, newline='') as csvfile:
            csvReader = csv.DictReader(csvfile)
            for row in csvReader:
                playerName = row['White']
                openingName = row['Opening']
                if playerName == name:
                    if openingName not in self.playerOpeningUsage[name]:
                        self.playerOpeningUsage[name][openingName] = 0
                    self.playerOpeningUsage[name][openingName] += 1
        sorted_openings = sorted(self.playerOpeningUsage[name].items(), key=lambda x: x[1], reverse=True)
        playerStats = self.playerData[name]
        print(f"{name}: {playerStats['ELO']} ELO, {playerStats['Wins']} Wins\n{name}'s top {min(playerStats['Wins'], 3)} Openings:")
        for i in range(min(playerStats['Wins'], 3)):
            print(f"   {sorted_openings[i][0]}: Used {sorted_openings[i][1]} times")

    #Referenced from DSA Module 6 - Sorting by Amanpreet Kapoor
    #Time - Worst O(N^2)
    #Space - O(log n) recursion stack
    def quickSort(self, arr, low, high):
        #check if sortable
        if low < high:
            pivot = self.partition(arr, low, high) #find pivot
            self.quickSort(arr, low, pivot - 1) #call on left
            self.quickSort(arr, pivot + 1, high) #call on right
        return arr

    def partition(self, arr, low, high):
        pivot = arr[low][1] #choose first element of array for pivot
        up = low
        down = high

        while up < down: #continue til they pass eachother
            while up < high and arr[up][1] <= pivot: #while up is not past down & up is not greater than the pivot value
                up += 1 #go right
            while arr[down][1] > pivot: #while down is not less than pivot value
                down -= 1 #go left
            if up < down: #if up still < down, swap
                arr[up], arr[down] = arr[down], arr[up]

        arr[low], arr[down] = arr[down], arr[low] #swap pivot and down
        return down #return pivot index after partition

    #Time - Worst O(n log n)
    #Space - O(n)
    def mergeSort(self, arr):
        #base case, if equal to 1, start combining
        if len(arr) > 1:
            #divide the array in half and recall merge sort
            middle = len(arr)//2
            left = arr[0:middle]
            right = arr[middle:len(arr)]
            self.mergeSort(left)
            self.mergeSort(right)
            #after fully separating the initial array, we begin combination
            #these are the indexes of left, right, and the final array respectively
            l = 0
            r = 0
            i = 0
            #while there is still values left to be sorted in both the right and left array
            while l < len(left) and r < len(right):
                #if left is > add right value and increment the final and right index
                if left[l][1] > right[r][1]:
                    arr[i] = right[r]
                    r = r + 1
                    i = i + 1
                #otherwise insert the left and increment the left and final index
                else:
                    arr[i] = left[l]
                    l = l + 1
                    i = i + 1
            #these if statements check for which array still has values to be inserted
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
        return arr

    def openingPrinter(self, num):
        print(len(self.winRatios))
        self.winRatios.reverse()
        for index, pair in enumerate(self.winRatios[:num], start=1):
            opening = pair[0]
            success = round(pair[1] * 100, 2)
            if (index > 99):
                print(f"{index}. {opening.ljust(63)} | Success Ratio: {success}%")
            elif (index > 9):
                print(f"{index}. {opening.ljust(64)} | Success Ratio: {success}%")
            else:
                print(f"{index}. {opening.ljust(65)} | Success Ratio: {success}%")
        print()

    def eloPrinter(self, num):
        self.eloData.reverse()
        for index, group in enumerate(self.eloData[:num], start=1):
            opening = group[0]
            whitePlayerElo = group[1]
            blackPlayerElo = group[2]
            whitePlayerName = group[3]
            blackPlayerName = group[4]
            whiteRatingDiff = group[5]
            result = group[6]
            print(f"{index}. {whitePlayerName} vs. {blackPlayerName}")
            print(f"      {whitePlayerName} Elo: {whitePlayerElo} | {blackPlayerName} Elo: {blackPlayerElo} | White Differential: {whiteRatingDiff}")
            print(f"      Opening: {opening}")
            print(f"      Result: {result}")
        print()
        