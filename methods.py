import requests
from bs4 import BeautifulSoup
import json


class Main():

    CURRICULUM = 'CURRICULUM'
    BRANCH = 'BRANCH'
    UNIT = 'UNIT'
    TOPIC = 'TOPIC'
    LESSON = 'LESSON'
    KHAKACADEMY_URL = 'https://www.khanacademy.org'

    BRANCH_TITLE_ATTR = 'data-test-id'
    BRANCH_TITLE_VAL = 'unit-header'

    UNIT_TITLE_ATTR = 'data-test-id'
    UNIT_TITLE_VAL = 'lesson-link'
    UNIT_TITLE_unitPage = '[data-test-id="unit-block-title"]'

    TOPIC_HEADER_ATTR = 'data-test-id'
    TOPIC_HEADER_VAL = 'lesson-card-link'

    LESSON_TITLE_SELECTOR = 'div[data-test-id="lesson-card"] ._14hvi6g8'
    LESSON_LINK_SELECTOR = 'div[data-test-id="lesson-card"] ._stw1dyg > a:first-child'

    LESSON_LENGTH_ATTR = 'data-test-id'
    LESSON_LENGTH_VAL = 'video-time-hidden'

    # return True
    CURRIUCULUM_PAGE_SIGNATURE_1 = '[data-slug="table-of-contents"]'
    # return False
    CURRIUCULUM_PAGE_SIGNATURE_2 = '[data-position-slug="subject-challenge"]'
    LESSON_PAGE_SIGNATURE = '[data-test-id="tutorial-page"]'
    BRANCH_PAGE_SIGNATURE = '[data-position-slug="subject-challenge"]'
    UNIT_PAGE_SIGNATURE = '[aria-labelledby="topic-progress-sidebar-title"]'

    _total_lessons = 0
    _branches_len = 0
    _units_len = 0

    _brances_titles = []
    _units_titles = []
    _units_links = []

    _topics_titles = []
    _lessons_titles = []
    _lessons_links = []

    def __init__(self, link):
        self.link = link

    def loadPageContent(self, page_link):
        if self.KHAKACADEMY_URL not in page_link:
            page_link = self.KHAKACADEMY_URL + page_link
        req = requests.get(page_link)
        content = BeautifulSoup(req.text, 'html.parser')
        return content

    def determinePage(self):
        """
            Determine web page is 
        """
        load_page = self.loadPageContent(self.link)
        if load_page.select(self.CURRIUCULUM_PAGE_SIGNATURE_1) \
                and bool(load_page.select(self.CURRIUCULUM_PAGE_SIGNATURE_2)) == False:
            return self.CURRICULUM

        elif load_page.select(self.LESSON_PAGE_SIGNATURE):
            return self.LESSON
        elif load_page.select(self.BRANCH_PAGE_SIGNATURE):
            return self.BRANCH
        elif load_page.select(self.UNIT_PAGE_SIGNATURE):
            return self.UNIT
        else:
            return None

    def curriculm(self):
        """
            Count Branches and units,
            Titles of Branches and units,
            Units Links
        """
        page_content = self.loadPageContent(self.link)
        branches = page_content.find_all(
            attrs={self.BRANCH_TITLE_ATTR: self.BRANCH_TITLE_VAL}, href=True)
        units = page_content.find_all(
            attrs={self.UNIT_TITLE_ATTR: self.UNIT_TITLE_VAL}, href=True)

        self._branches_len = len(branches)
        self._brances_titles = []
        self._units_len = len(units)
        self._units_links = [link['href'] for link in units]

        for branche in branches:
            for title in branche.contents:
                self._brances_titles.append(title.get_text())

    def branch(self):
        """
            units and topics len and titles
        """
        # NOTICE : I doesn't made a one method to get units titles in general
        # and call these method in is_curriculm method and is_branch method
        # because the selector in branch web page and in curriculm web page is Different
        load_branch = self.loadPageContent(self.link)
        # see deffrence between curriculum page VS branch page
        #   units       = page_content.find_all(attrs={self.UNIT_TITLE_ATTR:self.UNIT_TITLE_VAL},href=True)
        get_units = load_branch.find_all(
            attrs={self.BRANCH_TITLE_ATTR: self.BRANCH_TITLE_VAL})
        get_lessons = load_branch.select(self.LESSON_TITLE_SELECTOR)
        get_lessons_len = len(get_lessons)
        units = load_branch.find_all(
            attrs={self.UNIT_TITLE_ATTR: self.UNIT_TITLE_VAL}, href=True)

        self._units_titles = []
        self._total_units = len(get_units)
        self._units_links = [link['href'] for link in units]

        for unit in get_units:
            for unit_title in unit.contents:
                self._units_titles.append(unit_title.get_text())

    def is_unit(self, unit_link):

        load_unit = self.loadPageContent(unit_link)
        get_topics = load_unit.find_all(
            attrs={self.TOPIC_HEADER_ATTR: self.TOPIC_HEADER_VAL})

        unit_name = load_unit.select_one(self.UNIT_TITLE_unitPage)
        get_lessons = load_unit.select(self.LESSON_TITLE_SELECTOR)
        get_lessons_len = len(get_lessons)

        self._total_lessons = self._total_lessons + get_lessons_len
        self._units_titles.append({unit_name.text: get_lessons_len})

        # get_lessons_link  = load_unit.select(self.LESSON_LINK_SELECTOR)
        # self._topics_titles  = [ topic.get_text() for topic in get_topics ]
        # self._lessons_titles = [ lesson.get_text() for lesson in get_lessons ]
        # self._lessons_links  = [ lesson['href'] for lesson in get_lessons_link ]

    def lesson_length(self, lesson_link):
        load_lesson_page = self.loadPageContent(lesson_link)
        get_length = load_lesson_page.find(
            attrs={self.LESSON_LENGTH_ATTR: self.LESSON_LENGTH_VAL})
        # <span class="sr-only" data-test-id="video-time-hidden">Current time:<!-- -->0:00<!-- -->Total duration:<!-- -->7:18</span>
        total_duration = get_length.get_text()
        duration = 'duration:'  # for explaination these step loo on the upper comment
        # + len(duration) to clean the result from "duration:"
        position = total_duration.find(duration) + len(duration)

        return total_duration[position:]

    ''' 
        Getters Methods
    '''

    def getUnitsLinks(self):
        return self._units_links

    def getUnitsTitles(self):
        return self._units_titles

    def getUnitsLength(self):
        return self._units_len

    def getTotalLessons(self):
        return self._total_lessons

    def getBranchTitles(self):
        return self._brances_titles

    def getTopicTitles(self):
        return self._topics_titles

    def getBrancheLength(self):
        return self._branches_len
