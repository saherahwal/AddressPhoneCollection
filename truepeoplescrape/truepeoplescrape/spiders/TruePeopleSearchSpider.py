import scrapy

#
# This spider is responsible for scraping phone numbers
# for a given address using truepeoplesearch.com website
# for example an address (11224 Bertrand ave, Granada hills, CA, 91344)
# will return result of at least one person
# This module will follow the retuned links for that address
# and collect all phone numbers
#
class TruePeopleSearchSpider(scrapy.Spider):

    name = "truepeoplesearch"

    def __init__(self, address=None, output_folder=None, html_file=None):
        self.address = address    
        self.output_folder = output_folder  
        self.html_file = html_file          

    def start_requests(self):

        base = "https://www.truepeoplesearch.com/results?"
        urls = []
        
        (street, city, state, zipCpde) = self.parseAddress()

        # construct url address from street,city,state,zip tuple
        url_address = base + "streetaddress=" + street
        url_address += "&citystatezip=" + city + "," + state + "," + zipCpde

        yield scrapy.Request(url=url_address, callback=self.parse)

    def parse(self, response):               

        # get all names associated with the address
        names = response.xpath('//div[@class="h4"]/text()').getall()
        
        # get all the links to follow for phone numbers
        links = response.xpath('//div[contains(@class, "card-summary")]/@data-detail-link').getall()

        # follow each link
        for link in links:
            print("parsing link:", link)
            yield response.follow(url=link, callback = self.parse_individual)
    

    def parse_individual(self, response):
        
        # retrieve name span - could be multiple
        name_span = response.xpath('//span[@class="h2"]/text()').getall()
        
        # retrieve phone numbers
        phone_nums = response.xpath('//a[@data-link-to-more="phone"]/text()').getall()
                
        # file name per .html file name
        file_name = self.html_file + ".csv"
        
        print("---")
        print(self.output_folder)
        print(file_name)
        print("---")
        
        with open( self.output_folder + "\\" + file_name, 'a' ) as f:
            f.write(name_span[1][:-1])
            f.write(',')
            f.write(self.address)
            f.write(',')
            f.write('[')
            for num in phone_nums:
                f.write(num) 
                f.write(',')
            f.write(']')
            f.write('\n')

    def parseAddress(self):        
        return  self.address.split(',')



