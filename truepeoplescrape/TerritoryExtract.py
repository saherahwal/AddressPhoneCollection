from html.parser import HTMLParser
import os
from Address import GeocodedAddress


class MyHTMLParser(HTMLParser):
    """
        HTML parser to be used by TerritoryExtract module
        Helper module to parse through HTML table of individuals on territory in Alba HTML export
    """

    inTable = False
    inHeader = False
    inRow = False
    headers = []
    rows = []
    current_row = []  
    
    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.inTable = True
        elif tag == 'thead':
            self.inHeader = True
        elif tag == 'tr':
            self.inRow = True
            

    def handle_endtag(self, tag):
        if tag == 'table':
            self.inTable = False            
        elif tag == 'thead':
            self.inHeader = False
        elif tag == 'tr':
            self.inRow = False
            if (self.current_row[0] != 'ID'):
                self.rows.append(self.current_row)
            self.current_row = []

    def handle_data(self, data):
        if self.inTable:            
            if self.inHeader:
                self.headers.append(data)
            if self.inRow:
                self.current_row.append(data)

    def retrieve_result(self):
        return ( self.headers, self.rows)
    

class TerritoryExtract(object):
    """
        TerritoryExtract

        Given folder location with Alba HTML exports
        this module retrieves names and addesses by means
        of simple HTML parser from the territory HTML table
    """

    def __init__(self, inputFolder):
        self.inputFolder = inputFolder       


    def getHtmlFiles(self):
        """
            retrieve html files only
        """
        files = os.listdir(self.inputFolder)
        htmlFiles = []
        for f in files:
            if ".html" in f:
                htmlFiles.append(f)
        return htmlFiles

    def ParseTable(self, htmlFile):
        """
            parses the HTML table
        """
        absFile = self.inputFolder + "\\" + htmlFile
        content = open( absFile, 'rb').read().decode('utf-8')
        parser = MyHTMLParser()
        parser.feed(content)
        return parser.retrieve_result()

    def GetAddressList(self, headers, rows):
        """
            retrieves the address list given rows of parsed HTML Alba table
        """
        # TODO: use headers for better design and modularity
        address_list = []
        for row in rows:
            address_list += [(row[4], row[6])]

        return address_list


#
# Testing territory extract to be run from the commandline
#
if __name__ == "__main__":

    addresses = []
    tExtract = TerritoryExtract("C:\\Users\\sahwal\\Source\\Repos\\AddressPhoneCollection\\albaFiles")
    
    #
    # Go over html Alba files and append GeocodedAddress list
    #
    htmlFiles = tExtract.getHtmlFiles()
    print (htmlFiles)
    for f in htmlFiles:
        parseResult = tExtract.ParseTable(f)
        addressList = tExtract.GetAddressList(parseResult[0], parseResult[1])        
        for elt in addressList:
            addresses += [GeocodedAddress(elt[0], elt[1])]

    for address in addresses:
        print(address)

    
    
    
        
    
