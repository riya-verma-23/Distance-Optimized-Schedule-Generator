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
  
  def has_time_conflict(self, section_list):

    # check all pairs (obviously no time conflict not transitive)
    for i in section_list:
      for j in section_list:
        if i != j and i.has_time_conflict(j):
          return True

    return False
  
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
    
    def __init__(self, sections):
        # linked sections
        self.sections = sections

    def add_section(self, section):
      self.sections.append(section)

    # returns section at index i (can be called with [])
    def __getitem__(self, index):
      return self.sections[index]
  
  # Access all instance vars 
  def get_section(self, section_name):
    return self.sections[section_name]

  def get_subject(self):
    return self.subject
  
  def get_number(self):
    return self.num
