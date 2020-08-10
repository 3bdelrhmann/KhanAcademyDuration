import requests
from bs4 import BeautifulSoup
import json
class Main():

    CURRICULUM   = 'CURRICULUM' 
    BRANCH       = 'BRANCH'
    UNIT         = 'UNIT'
    TOPIC        = 'TOPIC'
    
    BRANCH_TITLE_ATTR  = 'data-test-id'
    BRANCH_TITLE_VAL   = 'unit-header'

    UNIT_TITLE_ATTR  = 'data-test-id'
    UNIT_TITLE_VAL   = 'lesson-link'

    TOPIC_HEADER_ATTR  = 'data-test-id'
    TOPIC_HEADER_VAL   = 'lesson-card-link'

    LESSON_TITLE_SELECTOR = 'div[data-test-id="lesson-card"] ._14hvi6g8'
    LESSON_LINK_SELECTOR  = 'div[data-test-id="lesson-card"] ._stw1dyg > a:first-child'

    LESSON_LENGTH_ATTR = 'data-test-id'
    LESSON_LENGTH_VAL  = 'video-time-hidden'

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
        load_page = self.load_webpage(link)
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
        branches = page_content.find_all(attrs={self.BRANCH_TITLE_ATTR:self.BRANCH_TITLE_VAL},href=True)
        units    = page_content.find_all(attrs={self.UNIT_TITLE_ATTR:self.UNIT_TITLE_VAL},href=True)

        self.branches_len   = len(branches)
        self.brances_titles = []
        self.units_len    = len(units)
        self.units_titles = [unit.get_text() for unit in units]
        self.units_links  = [link['href'] for link in units]

        for branche in branches:
            for title in branche.contents:
                self.brances_titles.append(title.get_text())
    
    def is_branch(self,branch_link):
        """
            units and topics len and titles
        """
        # NOTICE : I doesn't made a one method to get units titles in general
        # and call these method in is_curriculm method and is_branch method
        # because the selector in branch web page and in curriculm web page is Different
        load_branch = self.load_webpage(branch_link)
        # see deffrence between curriculum page VS branch page
    #   units       = page_content.find_all(attrs={self.UNIT_TITLE_ATTR:self.UNIT_TITLE_VAL},href=True)
        get_units   = load_branch.find_all(attrs={self.BRANCH_TITLE_ATTR:self.BRANCH_TITLE_VAL})
        self.units_titles = []
        self.total_units  = len(get_units)
        
        for unit in get_units:
            for unit_title in unit.contents:
                self.units_titles.append(unit_title.get_text())
        
    def is_unit(self,unit_link):
        load_unit  = self.load_webpage(unit_link)
        get_topics = load_unit.find_all(attrs={self.TOPIC_HEADER_ATTR:self.TOPIC_HEADER_VAL})
        
        get_lessons       = load_unit.select(self.LESSON_TITLE_SELECTOR)
        get_lessons_link  = load_unit.select(self.LESSON_LINK_SELECTOR)
        
        self.topics_titles  = [ topic.get_text() for topic in get_topics ]
        self.lessons_titles = [ lesson.get_text() for lesson in get_lessons ]
        self.lessons_links  = [ lesson['href'] for lesson in get_lessons_link ] 
        self.total_lessons  = len(get_lessons)

        
    def lesson_length(self,lesson_link):
        load_lesson_page = self.load_webpage(lesson_link)
        get_length     = load_lesson_page.find(attrs={self.LESSON_LENGTH_ATTR:self.LESSON_LENGTH_VAL})
        total_duration = get_length.get_text() # <span class="sr-only" data-test-id="video-time-hidden">Current time:<!-- -->0:00<!-- -->Total duration:<!-- -->7:18</span>
        duration    = 'duration:' # for explaination these step loop on the upper comment
        position    = total_duration.find(duration) + len(duration) # + len(duration) to clean the result from "duration:"
        
        return total_duration[position:] 

obj    = Main('https://www.khanacademy.org/math/high-school-math/')
