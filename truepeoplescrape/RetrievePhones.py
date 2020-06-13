from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from TerritoryExtract import *


# First we extract names and addresses from territory
addresses_map = {}
addresses = []
tExtract = TerritoryExtract("C:\\Users\\sahwal\\Source\\Repos\\AddressPhoneCollection\\albaFiles")

output_folder = "C:\\Users\\sahwal\\Source\\Repos\\AddressPhoneCollection\\output"

# Go over html Alba files and append GeocodedAddress list
htmlFiles = tExtract.getHtmlFiles()
for f in htmlFiles:
    addresses = []
    parseResult = tExtract.ParseTable(f)
    addressList = tExtract.GetAddressList(parseResult[0], parseResult[1])        
    for elt in addressList:
        addresses += [GeocodedAddress(elt[0], elt[1])]
    
    addresses_map[f] = addresses[:]

# run scrapy spider crawler for each address

process = CrawlerProcess(get_project_settings())

for keyfile,addressList in addresses_map.items():
    # 'truepeoplesearch' is the name of one of the spiders of the project.
    html_file = keyfile.split('.')[0]
    print("html_file:", html_file )
    for address in addressList:
        print("processing address:", address)        
        process.crawl('truepeoplesearch', address=address.getAddress(), output_folder=output_folder, html_file=html_file)

process.start() # the script will block here until the crawling is finished        