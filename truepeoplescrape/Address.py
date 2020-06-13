class GeocodedAddress:
    """
        Simple class to encapsulate individual address on 
        the territory.
    """
    def __init__(self, name, address ):
        self.address = address
        self.name = name

    def __str__(self):
        return "Name:" + self.name + "," + "Address:" + self.address

    def parseAddress(self):        
        return  self.address.split(',')

    def getAddress(self):
        return self.address
