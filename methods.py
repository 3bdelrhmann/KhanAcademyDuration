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

    TOPIC_HEADER_ATTR  = 'data-test-id'
    TOPIC_HEADER_VAL   = 'lesson-card-link'

    LESSON_TITLE_CLASS = 'div[data-test-id="lesson-card"] ._14hvi6g8'

    def __init__(self,link):
        self.link    = link
        
    def load_webpage(self,page_link):
        req     = requests.get(page_link)
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


    def is_curriculm(self):
        """
            Count Branches and units,
            Titles of Branches and units,
            Units Links
        """
        page_content = self.load_webpage(self.link)
        branches = page_content.find_all(attrs={self.BRANCH_HEADER_ATTR:self.BRANCH_HEADER_VAL},href=True)
        units    = page_content.find_all(attrs={self.UNIT_HEADER_ATTR:self.UNIT_HEADER_VAL},href=True)

        self.branches_len   = len(branches)
        self.brances_titles = []
        self.units_len    = len(units)
        self.units_titles = [unit.get_text() for unit in units]
        self.units_links  = [link['href'] for link in units]

        for branche in branches:
            for title in branche.contents:
                self.brances_titles.append(title.get_text())
        
    def count_topics(self,unit_link):
        load_unit = self.load_webpage(unit_link)
        get_topics  = load_unit.select(self.LESSON_TITLE_CLASS)
        get_lessons = load_unit.find_all(attrs={self.TOPIC_HEADER_ATTR:self.TOPIC_HEADER_VAL})

        self.topics_titles = [ topic.get_text() for topic in get_topics ]
        self.lessons_titles = [ lesson.get_text() for lesson in get_lessons ]
        
    def count_units_and_branches(self):
        pass

    def count_units(self):
        pass

obj = Main('https://www.khanacademy.org/math/high-school-math/')
obj.count_topics('https://www.khanacademy.org/math/high-school-math/math1/x89d82521517266d4:algebra-foundation')
print(obj.topics_titles)
print(obj.lessons_titles)