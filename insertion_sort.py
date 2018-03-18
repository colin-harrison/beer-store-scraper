#! python3
# insertion_sort.py - this module defines a simple implementation
# of insertion sort.

def sort(beerList):
    print('we sorting')
    for i in range(len(beerList)):
        for j in range(i, 0, -1):
            if beerList[j-1][6] > beerList[j][6]:
                temp = beerList[j-1]
                beerList[j-1] = beerList[j]
                beerList[j] = temp
            else:
                break
    return beerList
