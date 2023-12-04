import csv

class ChessAnalyzer:
    def __init__(self, selectedModes=None):
        self.csvFile = 'sep.csv'
        self.selectedModes = selectedModes if selectedModes is not None else []
        self.mode = ""
        self.eloData = []
        self.openingData = []
        self.playerData = {}
        self.winRatios = []
        self.winRatios2 = []
        self.playerOpeningUsage = {}

    def printer(self):
        for opening_ratio in self.winRatios:
            print(f"Opening: {opening_ratio[0]}, Success Ratio: {opening_ratio[1]}")

    def eloAnalyzer(self):
        with open(self.csvFile, newline='') as csvfile:
            #creates csv manager for traversing rows
            csvReader = csv.DictReader(csvfile)
            #iterate through each row in the CSV
            for row in csvReader:
                gameMode = row['Event']
                whitePlayerName = row['White']
                blackPlayerName = row['Black']
                whitePlayerElo = row['WhiteElo']
                blackPlayerElo = row['BlackElo']
                whiteRatingDiff = row['WhiteRatingDiff']
                opening = row['Opening']
                result = row['Result']

                whitePlayerElo = int(whitePlayerElo) if whitePlayerElo.isdigit() else None
                blackPlayerElo = int(blackPlayerElo) if blackPlayerElo.isdigit() else None

                # Append data to eloData list
                self.eloData.append([opening, whitePlayerElo, blackPlayerElo, whiteRatingDiff, result])
                

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
                if occurrences > 25: #only if it occurs over 25 to eliminate noise of 100% success rates in few games
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
                    # Update occurrences
                    self.playerData[playerName]['Occurrences'] += 1
                    # Check if game result is a win (1-0) and update wins
                    if result == '1-0':
                        self.playerData[playerName]['Wins'] += 1



    def getPlayerOpeningUsage(self, name):
        if name not in self.playerData:
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
        print(f"{name}: {playerStats['ELO']} ELO, {playerStats['Wins']} Wins\n{name}'s top 3 Openings:")
        for i in range(3):
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
        if len(arr) > 1:
            middle = len(arr)//2
            left = arr[0:middle]
            right = arr[middle:len(arr)]
            self.mergeSort(left)
            self.mergeSort(right)
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

    # def openingPrinter(self, num):
    #     self.winRatios.reverse()
    #     for index, pair in enumerate(self.winRatios[:num], start=1):
    #         print(f"{index}. {pair[0]} | Success Ratio: {round(pair[1] * 100, 2)}%")
    #     print()

    def openingPrinter(self, num):
        self.winRatios.reverse()
        for index, pair in enumerate(self.winRatios[:num], start=1):
            opening_name = pair[0]
            success_ratio = round(pair[1] * 100, 2)
            print(f"{index}. {opening_name.ljust(50)} | Success Ratio: {success_ratio}%")
        print()