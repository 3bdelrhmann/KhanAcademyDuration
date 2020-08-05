import requests
from bs4 import BeautifulSoup
import json
class Main():

    CURRICULUM   = 'CURRICULUM' 
    BRANCH       = 'BRANCH'
    UNIT         = 'UNIT'
    TOPIC        = 'TOPIC'
    
    BRANCH_HEADER_ATTR  = 'data-test-id'
    BRANCH_HEADER_VAL   = 'unit-header'

    UNIT_HEADER_ATTR  = 'data-test-id'
    UNIT_HEADER_VAL   = 'lesson-link'

    def __init__(self,link):
        self.link    = link
        self.page_content = self.load_webpage()
        
    def load_webpage(self):
        req     = requests.get(self.link)
        content = BeautifulSoup(req.text,'html.parser')
        return content

    def determine_page(self):
        """
            Determine web page is 
        """
        web_page = ''
        result   = self.CURRICULUM
        
        if self.BRANCHES_UNITS_CLASS not in web_page:
            return self.UNIT
        
        if self.BRANCH_CLASS in web_page:
            result = self.BRANCH
        return result


    def count_branches(self):
        """
            Count Branches and units,
            Titles of Branches and units,
            Units Links
        """
        branches = self.page_content.find_all(attrs={self.BRANCH_HEADER_ATTR:self.BRANCH_HEADER_VAL},href=True)
        units    = self.page_content.find_all(attrs={self.UNIT_HEADER_ATTR:self.UNIT_HEADER_VAL},href=True)

        self.branches_len = len(branches)
        self.units_len    = len(units)
        self.units_links  = [link['href'] for link in units]
        
        for branche in branches:
            print(branche)
        

    def count_units_and_branches(self):
        pass

    def count_units(self):
        pass

obj = Main('https://www.khanacademy.org/math/high-school-math/')
obj.count_branches()
