#! python3
# This program scrapes thebeerstore.ca for a list of url's to every beer
# they sell. The beers are categorized into Ale, Lager, Malt & Stout.

import requests, bs4, re, openpyxl
from openpyxl import Workbook

# Refactor all of this into one function
# So don't write same code four times, write one function
# And call it four times
# The parameter should be the type of beer e.g. 'Ale'
# Then use the parameter to plug into linksRequest at the end of beer_type--

# Get all links for the Lagers
linksRequest = requests.get('http://www.thebeerstore.ca/beers/search/beer_type--Lager')
linksText = bs4.BeautifulSoup(linksRequest.text)
rawLinks = linksText.select('.brand-link')

sizeRegex = re.compile(r'\d+.*ml')
volumeRegex = re.compile(r'\d+\sml')
quantityRegex = re.compile(r'\d+')
priceRegex = re.compile(r'\d+\.\d{2}')
linkRegex = re.compile(r'/beers/\w+(-\w+)*')
nameRegex = re.compile(r'>.*<')
ABVRegex = re.compile(r'\d+\.\d')
lagerLinks = []
lagerList = [] 

# Program only works for lagers as of now.
# After refactoring it will run through all 4 types.

for i in range(len(rawLinks)):
    # Get the webpage of this specifc link
    rawLinksString = str(rawLinks[i])
    match = linkRegex.search(rawLinksString)
    fullLink = 'http://www.thebeerstore.ca' + match.group(0)
    beerInfo = requests.get(fullLink)
    beerSoup = bs4.BeautifulSoup(beerInfo.text)

    # Get prices and sizes of the beer
    prices = beerSoup.select('.price')
    sizes = beerSoup.select('.size')

    # Get the name of the beer
    names = beerSoup.select('.page-title')
    nameMatch = nameRegex.search(str(names[0]))
    name = nameMatch.group(0)[1:-1]

    # Get the ABV of the beer
    abvContent = beerSoup.select('dd')
    abvMatch = ABVRegex.search(str(abvContent))
    ABV = float(abvMatch.group(0)) / 100

    # Iterate through each size option to get the price, size, vol, and quantity of each
    for j in range(len(prices)):
        price = priceRegex.search(str(prices[j])).group(0)
        volume = volumeRegex.search(str(sizes[j])).group(0)
        quantity = quantityRegex.search(str(sizes[j])).group(0)
        size = sizeRegex.search(str(sizes[j])).group(0)
        lagerList.append([name, size, quantity, volume[:-3], ABV, price]) # remove ' ml'
        #print([name, size, quantity, volume, ABV, price])

wb = Workbook()
ws = wb.active
ws.title = 'Lagers'

# Set headers
ws['B3'] = 'Beer'
ws['C3'] = 'Sold as'
ws['D3'] = 'Quantity'
ws['E3'] = 'Volume (ml)'
ws['F3'] = 'ABV'
ws['G3'] = 'Price'
ws['H3'] = 'Price per Drink'
ws.column_dimensions['B'].width = 24
ws.column_dimensions['C'].width = 20
ws.column_dimensions['H'].width = 12

row = 4
mL_per_drink = 17.7441 # ml

for i in range(len(lagerList)):
    nameIndex = 'B' + str(row)
    sizeIndex = 'C' + str(row)
    quantityIndex = 'D' + str(row)
    volIndex = 'E' + str(row)
    abvIndex = 'F' + str(row)
    priceIndex = 'G' + str(row)
    costPerDrinkIndex = 'H' + str(row)
    row += 1

    # Import list into Excel
    ws[nameIndex] = lagerList[i][0]
    ws[sizeIndex] = lagerList[i][1]
    ws[quantityIndex] = int(lagerList[i][2])
    ws[volIndex] = float(lagerList[i][3])
    ws[abvIndex] = lagerList[i][4]
    ws[priceIndex] = float(lagerList[i][5])
    
    # Get price per drink (17.7441 mL alcohol)
    alcoholVol = float(lagerList[i][2]) * float(lagerList[i][3]) * float(lagerList[i][4])
    dollars_per_mL = float(lagerList[i][5]) / alcoholVol
    costPerDrink = dollars_per_mL * mL_per_drink
    ws[costPerDrinkIndex] = round(costPerDrink,2)
    

wb.save('beer_store_catalog.xlsx')
