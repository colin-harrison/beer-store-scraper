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

sizeRegex = re.compile(r'\d* ml')
canRegex = re.compile(r'473 ml')
kegRegex = re.compile(r'30000 ml')

rawLinks = linksText.select('.brand-link')
linkRegex = re.compile(r'/beers/\w+(-\w+)*')
nameRegex = re.compile(r'\w+(\s\w+)*')
lagerLinks = []

for i in range(len(rawLinks)):
    rawLinksString = str(rawLinks[i])
    match = linkRegex.search(rawLinksString)
    fullLink = 'http://www.thebeerstore.ca' + match.group(0)
    beerInfo = requests.get(fullLink)
    beerSoup = bs4.BeautifulSoup(beerInfo.text)
    prices = beerSoup.select('.price')
    sizes = beerSoup.select('.size')
    nameElement = beerSoup.select('.page-title')
    


# Get all links for the Ales
linksRequest = requests.get('http://www.thebeerstore.ca/beers/search/beer_type--Ale')
linksText = bs4.BeautifulSoup(linksRequest.text)

rawLinks = linksText.select('.brand-link')
linkRegex = re.compile(r'/beers/\w+(-\w+)*')
aleLinks = []

for i in range(len(rawLinks)):
    rawLinksString = str(rawLinks[i])
    match = linkRegex.search(rawLinksString)
    fullLink = 'http://www.thebeerstore.ca' + match.group(0)
    aleLinks.append(fullLink)

# Get all links for the Malts
linksRequest = requests.get('http://www.thebeerstore.ca/beers/search/beer_type--Malt')
linksText = bs4.BeautifulSoup(linksRequest.text)

rawLinks = linksText.select('.brand-link')
linkRegex = re.compile(r'/beers/\w+(-\w+)*')
maltLinks = []

for i in range(len(rawLinks)):
    rawLinksString = str(rawLinks[i])
    match = linkRegex.search(rawLinksString)
    fullLink = 'http://www.thebeerstore.ca' + match.group(0)
    maltLinks.append(fullLink)

# Get all links for the Stouts
linksRequest = requests.get('http://www.thebeerstore.ca/beers/search/beer_type--Ale')
linksText = bs4.BeautifulSoup(linksRequest.text)

rawLinks = linksText.select('.brand-link')
linkRegex = re.compile(r'/beers/\w+(-\w+)*')
stoutLinks = []

for i in range(len(rawLinks)):
    rawLinksString = str(rawLinks[i])
    match = linkRegex.search(rawLinksString)
    fullLink = 'http://www.thebeerstore.ca' + match.group(0)
    stoutLinks.append(fullLink)

print(len(lagerLinks))
print(len(aleLinks))
print(len(maltLinks))
print(len(stoutLinks))

# Iterate through the sizes and find all of the sizes minus ml
# Convert sizes to integers
# Iterate through both prices and sizes and compile a dictionary
# Where the size is the key and the value is the price

print(sizes)
print(prices)
