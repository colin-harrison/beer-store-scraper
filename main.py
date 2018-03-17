#! python3
# This program scrapes thebeerstore.ca for a list of url's to every beer
# they sell. The beers are categorized into Ale, Lager, Malt & Stout.

import requests, bs4, re, openpyxl, lxml, beer_store_scraper, threading
from openpyxl import Workbook

beerTypes = ['Lager', 'Ale', 'Malt', 'Stout']
threads = []
for i, beerType in enumerate(beerTypes):
    newThread = threading.Thread(target=beer_store_scraper.scrape, args=(beerTypes[i]))
    threads.append(newThread)
    newThread.start()

for currentThread in threads:
    currentThread.join()

# Each thread now finished. All scraping has been completed

#lagerList = beer_store_scraper.scrape('Lager')
#aleList = beer_store_scraper.scrape('Ale')
#maltList = beer_store_scraper.scrape('Malt')
#stoutList = beer_store_scraper.scrape('Stout')
beerLists = [lagerList, aleList, maltList, stoutList]

# Create 4 worksheets
wb = Workbook()
ws = wb.active
ws.title = 'Lagers'
wb.create_sheet(title='Ales')
wb.create_sheet(title='Malts')
wb.create_sheet(title='Stouts')

bold11Font = Font(size=11, bold=True)
mL_per_drink = 17.7441 # ml

for counter, beerList in enumerate(beerLists):
    row = 4
    
    # Set headers and change active sheet
    ws = wb[beerTypes[counter]]
    ws['B3'] = 'Beer'
    ws['C3'] = 'Sold as'
    ws['D3'] = 'Quantity'
    ws['E3'] = 'Volume (ml)'
    ws['F3'] = 'ABV'
    ws['G3'] = 'Price'
    ws['G3'].number_format = '$#.##'
    ws['H3'] = 'Price per Drink'
    ws['H3'].number_format = '$#.##'
    ws.column_dimensions['B'].width = 27
    ws.column_dimensions['C'].width = 20
    ws.column_dimensions['H'].width = 12
    
    for i in range(len(beerList)):
        nameIndex = 'B' + str(row)
        sizeIndex = 'C' + str(row)
        quantityIndex = 'D' + str(row)
        volIndex = 'E' + str(row)
        abvIndex = 'F' + str(row)
        priceIndex = 'G' + str(row)
        costPerDrinkIndex = 'H' + str(row)
        row += 1

        # Import list into Excel
        ws[nameIndex] = beerList[i][0]
        ws[sizeIndex] = beerList[i][1]
        ws[quantityIndex] = int(beerList[i][2])
        ws[volIndex] = float(beerList[i][3])
        ws[abvIndex] = beerList[i][4]
        ws[priceIndex] = float(beerList[i][5])
        
        # Get price per drink (17.7441 mL alcohol)
        alcoholVol = float(beerList[i][2]) * float(beerList[i][3]) * float(beerList[i][4])
        dollars_per_mL = float(beerList[i][5]) / alcoholVol
        costPerDrink = dollars_per_mL * mL_per_drink
        ws[costPerDrinkIndex] = round(costPerDrink,2)

wb.save('beer_store_catalog.xlsx')
