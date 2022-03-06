from bs4 import BeautifulSoup
import re
import requests

class Section:
  '''
  Creates a Section object
  
  Member variables:
  course: the course the Section belongs to
  name: the name of the section (i.e. ADB)
  section_type: i.e. Lecture, Discussion
  location: i.e. Altgeld Hall
  days: days the Section meets. i.e. MWF, TR
  start: datetime object representing start time
  end: datetime object representing end time
  '''
  
  # Initialize Section object given the section name, path to the section's xml file,
  # and its Course
  def __init__(self, name, section_path, course):
    self.course = course.subject + course.num
    self.name = name
    self.get_location(section_path)
  
  # Initialize location, section type, meeting days, and start and end time
  # from Section XML file
  def init_location(self, section_path):
    soup = BeautifulSoup(requests.get(section_path).text, "lxml-xml")
    self.section_type = soup.findAll("type")[0].string

    loc = soup.findAll("buildingName")
    if(len(loc)):
      self.location = loc[0].string
    else:
      self.location = "N/A"
    self.days = soup.findAll("daysOfTheWeek")[0].string
    self.start = datetime.datetime.strptime(soup.findAll("start")[0].string, '%I:%M %p')
    self.end = datetime.datetime.strptime(soup.findAll("end")[0].string, '%I:%M %p')
  
  # Get whether two sections have a time conflict
  # If one starts between the other's start and end times, there's a time conflict
  def has_time_conflict(self, other_section):
    if self.days == other_section.days:
      if self.start >= other_section.start and self.start <= other_section.end:
        return True
      if other_section.start >= self.start and other_section.start <= self.end:
        return True
    return False  
  
  # Determine whether two sections are linked
  # If two sections belong to the same course and have the same first letter, they're linked
  def linked(self, other_section):
    return (self.course == other_section.course) and (self.name[0] == other_section.name[0])

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
  def get_sections(self):
    soup = BeautifulSoup(self.page, "lxml-xml")
    self.sections = {}
    for section in soup.findAll("section"):
      self.sections[section.string] = Section(section.string, section.get('href'), self)

  # Initialize Course object given the semester, year, and course number
  def __init__(self, semester, year, course_num):
    try:
      self.subject = re.findall('\D+', course_num)[0]
      self.num = re.findall('\d+', course_num)[0]
      self.get_page(semester, year)
      self.get_sections()
    # if user forgot subject, number, or class unavailable in given semester, throw exception
    except:
      raise ValueError
