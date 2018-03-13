#! python3
# This program scrapes thebeerstore.ca for a list of url's to every beer
# they sell. The beers are categorized into Ale, Lager, Malt & Stout.

import requests, bs4, re

# Refactor all of this into one function
# So don't write same code four times, write one function
# And call it four times
# The parameter should be the type of beer e.g. 'Ale'
# Then use the parameter to plug into linksRequest at the end of beer_type--

# Get all links for the Lagers
linksRequest = requests.get('http://www.thebeerstore.ca/beers/search/beer_type--Lager')
linksText = bs4.BeautifulSoup(linksRequest.text)
rawLinks = linksText.select('.brand-link')

#sizeRegex = re.compile(r'\d* ml')
#canRegex = re.compile(r'473 ml')
#kegRegex = re.compile(r'30000 ml')

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
        lagerList.append([name, size, quantity, volume, ABV, price])
        print([name, size, quantity, volume, ABV, price])

# TODO: Write lagerList to an Excel Spreadsheet
