from bs4 import BeautifulSoup, SoupStrainer
from section import Section
import re
import requests
import itertools as it

class Course:
  '''
  Creates a Course object
  
  Instance variables:
  page: the Course's xml file as a string
  sections: dictionary of the sections, where the key is section name
  subject: i.e. MATH
  num: i.e. 241
  semester: i.e. spring
  year: i.e. 2022
  check_linked: whether if two sections are linked should be checked before
                creating linkedsections (not necessary for classes where
                Section names < 3 chars)

  Static variables:
  strainer: SoupStrainer("section") is an object that restricts how much of a page is
            parsed into a BeautifulSoup object, which can make parsing faster
  section_types: dictionary that determines whether two section types are equivalent
                (don't need to be taken together)
                src: https://registrar.illinois.edu/wp-content/uploads/2021/02/Schedule-Type-Descriptions.pdf
  '''
  strainer = SoupStrainer("section")

  # TODO: implement using up-trees (if scraping from registration doesn't pan out)
  section_types = {
    "Discussion":{"Online Discussion", "Discussion", "Discussion/Recitation"},
    "Lecture":{"Lecture-Discussion", "Lecture/Discussion", "Lecture", "Online Lecture-Discussion", 
              "Online Lecture",  "Online Lecture/Discussion"},
    "Lab":{"Laboratory-Discussion", "Laboratory/Discussion", "Online Lab", "Laboratory", "Online Lab"},
  }

  # Get course page using semester, year, and already init subject and number
  def get_page(self):
    path = ("https://courses.illinois.edu/cisapp/explorer/schedule/" + self.year +  "/" + 
    self.semester + "/" + self.subject + "/" + self.num + ".xml")

    try:
      response = requests.get(path)
    except:
      raise ValueError("timeout")
    self.page = response.text
    if not len(self.page):
      raise ValueError("no page found")
  
  # Init the sections dictionary using each course's XML file
  def init_sections(self):
    self.check_linked = True
    soup = BeautifulSoup(self.page, "lxml-xml", parse_only=Course.strainer)
    self.sections = {}
    for section in soup.findAll("section"):
      section_str = section.string.strip()
      self.sections[section_str] = Section(section_str, section.get('href'), self.subject + self.num)
      if len(section_str) < 3:
        self.check_linked = False


  # Initialize Course object given the semester, year, and course number
  def __init__(self, semester, year, course_num):
    try:
      self.subject = re.findall(r'[^\W\d_]+', course_num)[0].upper()
      self.num = re.findall('\d+', course_num)[0].strip()
      self.semester = semester.strip().lower()
      self.year = year.strip()
      self.get_page()
      self.init_sections()
    # if user forgot subject, number, or class unavailable in given semester, throw exception
    except:
      raise ValueError("bad course num")
  
  # Check if two courses are equal
  def __eq__(self, other):
    return (self.subject == other.get_subject() and self.num == other.get_number() and
     self.semester == other.get_semester() and self.year == other.get_year())

  # Get the section category this section longs to
  def get_section_category(self, section_type):
    if "Lecture" in section_type and section_type in Course.section_types["Lecture"]:
      return "Lecture"
    if "Discussion" in section_type and section_type in Course.section_types["Discussion"]:
      return "Discussion"
    if "Lab" in section_type and section_type in Course.section_types["Lab"]:
      return "Lab"
    return section_type

  # Determines if the current section type is in the dictionary
  # if it is, return the section name corresponding to this type
  # otherwise, return empty string
  # Example: MUS132 has types Online Discussion and Discussion/Recitation
  # After discussion/recitation added: key_in_dict('Online Discussion', sections_by_type) -> 'Discussion'
  # Before lecture added: key_in_dict('Lecture', sections_by_type) -> ''
  def key_in_dict(self, section_type, sections_by_type):
    section_cat = self.get_section_category(section_type)
    if section_cat in sections_by_type:
      return section_cat
    return "" 


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
      
      key = self.key_in_dict(section_type,sections_by_type)
      if len(key):
        sections_by_type[key].append(section)
      else:
        sections_by_type[self.get_section_category(section_type)] = [section]

    return sections_by_type
  
  # check if a list of sections contains a time conflict
  def has_time_conflict(self, section_list):

    # check all pairs (obviously no time conflict not transitive)
    for i in section_list:
      for j in section_list:
        if i != j and i.has_time_conflict(j):
          return True

    return False
  
  # check if all sections in list are linked by checking first chars
  # e.g. linked([ADA, AL2]) --> True
  #      linked([ADA, BL1]) --> False
  def linked(self, section_list):
    for i in section_list:
      if (i.get_name()[0] != section_list[0].get_name()[0] or 
          i.get_term() != section_list[0].get_term()):
        return False
    return True

  # Do not link courses that have incompatible section types
  # i.e. Laboratory-Discussion and Lecture-Discussion
  def relink(self, section_ls):
    has_lab_disc = False
    has_lecture_disc = False
    for section in section_ls:
      if section.get_type() in ["Lecture-Discussion", "Lecture/Discussion", "Online Lecture-Discussion", 
                                "Online Lecture/Discussion"]:
        return [section]
    return section_ls

  # gets list of all possible groups of linked sections 
  # (just the required e.g. lab, discussion, lecture) 
  # ex. {...{section discussion, section lecture, section lab}...}
  # uses has_time_conflict(list) to eliminate some linked section combinations
  def get_linked_sections(self):
    linked_sections = []

    sections_by_type = self.split_sections_on_type()
    sorted_sections = sorted(sections_by_type)
    
    # Get all possible combos of each section type
    # 1. Get lists of different section types from sorted sections by type dictionary
    # 2. Cartesian product of of these lists
    #    a. Unpack the lists (pass section_a, section_b, section_c instead of (section_a, section_b ...))
    #    b. Convert each list to a tuple
    #    c. Create lists storing each value in first list, then each value in first list + each value in
    #       second, and so on
    #    d. Return a generator encapsulating the combos (iteration works same as w list) where a0 is in 
    #       the first section type, a1 is in the second, and so on)
    combos = it.product(*(sections_by_type[section_name] for section_name in sorted_sections))
    # 3. Delete combos where sections have time conflicts (i.e. one Lecture section is at the
    #    same time as a discussion section
    for combo in combos:
      # if (not self.has_time_conflict(combo)) and self.linked(combo):
      if not self.has_time_conflict(combo) and ((self.check_linked and self.linked(combo))
          or not (self.check_linked)):
        linked_sections.append(self.LinkedSection(combo))
    
    # if len linked_sections is 0 just return the cartesian product
    # TODO: optimize
    if not len(linked_sections):
      combos = it.product(*(sections_by_type[section_name] for section_name in sorted_sections))
      for combo in combos:
        if not self.has_time_conflict(combo):
          new_combo = self.relink(combo)
          linked_sections.append(self.LinkedSection(new_combo))

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
    
    # returns # linked sections
    def __len__(self):
      return len(self.sections)
    
    # check if two LinkedSections are equal
    def __eq__(self, other):
      
      if len(self.sections) != len(other):
        return False
      
      for i in range(len(self.sections)):
        if self.sections[i] != other[i]:
          return False
      
      return True

    # check two LinkedSections have a time conflict
    def has_time_conflict(self, other):

      # check all pairs (obviously no time conflict not transitive)
      for i in self.sections:
        for j in other:
          if i != j and i.has_time_conflict(j):
            return True

      return False  
  
  # Get section with given name
  def get_section(self, section_name):
    try:
      return self.sections[section_name]
    except:
      raise KeyError("not a section")
  

  # Get course subject
  def get_subject(self):
    return self.subject
  
  # Get course number
  def get_number(self):
    return self.num
  
  # Get semester course belongs to
  def get_semester(self):
    return self.semester
  
  # Get year course belongs to
  def get_year(self):
    return self.year
  
  # Get all Section objs
  def get_sections(self):
    section_ls = []
    for section in self.sections:
      section_ls.append(self.sections[section])
    return section_ls
  
  # Print linked sections. Used in debugging
  def print_linked(self):
    linked = self.get_linked_sections()
    for l in linked:
        for section in l:
            print(section.get_name())
        print('\n')
