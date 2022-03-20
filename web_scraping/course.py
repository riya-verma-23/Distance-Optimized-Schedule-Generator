from bs4 import BeautifulSoup
from section import Section
import re
import requests
import itertools as it

class Course:
  '''
  Creates a Course object
  
  Member variables:
  page: the Course's xml file as a string
  sections: dictionary of the sections, where the key is section name
  subject: i.e. MATH
  num: i.e. 241
  '''
  
  # Get course page using semester, year, and already init subject and number
  def get_page(self, semester, year):
    path = "https://courses.illinois.edu/cisapp/explorer/schedule/" + year + "/" + semester.lower() + "/" + self.subject + "/" + self.num + ".xml"
    response = requests.get(path)
    self.page = response.text
    if not len(self.page):
      raise ValueError
  
  # Init the sections dictionary using each course's XML file
  def init_sections(self):
    soup = BeautifulSoup(self.page, "lxml-xml")
    self.sections = {}
    for section in soup.findAll("section"):
      section_str = section.string.strip()
      self.sections[section_str] = Section(section_str, section.get('href'), self)

  # equal operator for section objects by Riya. copy pasted due to problems with git pull
  def __eq__(self, other):
    return (self.course == other.course) and (self.name == other.name)

  # Initialize Course object given the semester, year, and course number
  def __init__(self, semester, year, course_num):
    try:
      self.subject = re.findall('\D+', course_num)[0]
      self.num = re.findall('\d+', course_num)[0]
      self.get_page(semester, year)
      self.init_sections()
    # if user forgot subject, number, or class unavailable in given semester, throw exception
    except:
      raise ValueError
  
  # Takes all sections from dictionary and splits it based on type
  # Discussion = [ section A, section B ]
  # Lecture = [ section C, section D ]
  # Lab = [ section E, section F ]
  # returns {'Discussion':Discussion , 'Lecture':Lecture , 'Lab':Lab }

  def split_sections_on_type(self):
    sections_by_type = {}
    
    for section_name in self.sections:
      section = self.sections[section_name]
      section_type = section.get_type()
      
      if section_type in sections_by_type:
        sections_by_type[section_type].append(section)
      else:
        sections_by_type[section_type] = [section]

    return sections_by_type
  
  # check if a list of sections contains a time conflict
  def has_time_conflict(self, section_list):

    # check all pairs (obviously no time conflict not transitive)
    for i in section_list:
      for j in section_list:
        if i != j and i.has_time_conflict(j):
          return True

    return False
  
  # gets list of all possible groups of linked sections 
  # (just the required e.g. lab, discussion, lecture) 
  # ex. {...{section discussion, section lecture, section lab}...}
  # uses has_time_conflict(list) to eliminate some linked section combinations
  def get_linked_sections(self):
    linked_sections = []

    # TODO: optimize
    sections_by_type = self.split_sections_on_type()
    sorted_sections = sorted(sections_by_type)
    combos = it.product(*(sections_by_type[section_name] for section_name in sorted_sections))

    for combo in combos:
      if not self.has_time_conflict(combo):
        linked_sections.append(self.LinkedSection(combo))
    
    return linked_sections
    
  class LinkedSection:
    
    '''
    Encapsulates a list of linked sections
    '''

    def __init__(self, sections):
        # linked sections
        self.sections = sections

    # Add a section to this group of linked sections
    def add_section(self, section):
      self.sections.append(section)

    # returns section at index i (can be called with [])
    def __getitem__(self, index):
      return self.sections[index]
  
  # Get section with given name
  def get_section(self, section_name):
    try:
      return self.sections[section_name]
    except:
      print("not a section")
      raise ValueError

  # Get course subject
  def get_subject(self):
    return self.subject
  
  # Get course number
  def get_number(self):
    return self.num
