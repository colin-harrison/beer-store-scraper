import requests, re, bs4, lxml

def scrape(beerType):

    # Get all links for the type of beer
    url = 'http://www.thebeerstore.ca/beers/search/beer_type--' + beerType
    linksRequest = requests.get(url)
    linksText = bs4.BeautifulSoup(linksRequest.text, "lxml")
    rawLinks = linksText.select('.brand-link')

    # Regular expression declarations
    sizeRegex = re.compile(r'\d+.*ml')
    volumeRegex = re.compile(r'\d+\sml')
    quantityRegex = re.compile(r'\d+')
    priceRegex = re.compile(r'\d+\.\d{2}')
    linkRegex = re.compile(r'/beers/\w+(-\%\w+(-\w+)*)?(-\w+)*')
    nameRegex = re.compile(r'>.*<')
    ABVRegex = re.compile(r'\d+\.\d')
    beerList = []

    for i in range(len(rawLinks)):
        # Get the webpage of this specifc link
        rawLinksString = str(rawLinks[i])
        match = linkRegex.search(rawLinksString)
        fullLink = 'http://www.thebeerstore.ca' + match.group(0)
        beerInfo = requests.get(fullLink)
        beerSoup = bs4.BeautifulSoup(beerInfo.text, "lxml")

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
            beerList.append([name, size, quantity, volume[:-3], ABV, price]) # remove ' ml'

    return beerList
