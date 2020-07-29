import requests
from bs4 import BeautifulSoup

class Main:

    CURRICULUM   = 'CURRICULUM' 
    BRANCH       = 'BRANCH'
    UNIT         = 'UNIT'
    BRANCH_CLASS = '._yb3e51j' 
    BRANCHES_UNITS_CLASS = '._7hv5v4c ._xmja1e8'
    
    def __init__(self,link):
        self.link = link

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
        
    def count_units_and_branches(self):
        pass

    def count_branches(self):
        pass
    
    def count_units(self):
        pass

