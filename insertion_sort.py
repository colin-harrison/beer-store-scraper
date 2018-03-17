#! python3
# insertion_sort.py - this module defines a simple implementation
# of insertion sort.

def sort(beerList):
    for i in range(len(beerList)):
        for j in range(i):
            if beerList[j-1][6] > beerList[j][6]:
                temp = beerList[j-1][6]
                beerList[j-1][6] = beerList[j][6]
                beerList[j][6] = temp
            else:
                break
    return beerList
