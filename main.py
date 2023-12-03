# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def gnomesort(arr, size):
    i = 0
    while i < size:
        if i == 0:
            i = i + 1
        if arr[i] >= arr[i - 1]:
            i = i + 1
        else:
            temp = arr[i]
            arr[i] = arr[i - 1]
            arr[i - 1] = temp
            i = i -1
    return arr


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    newArr = [4, 2, 6, 1, 3, 7, 5,]
    myArr = gnomesort(newArr, len(newArr))
    for i in myArr:
        print(i, end=" ")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
