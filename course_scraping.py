from bs4 import BeautifulSoup
import re
import requests

class Section:

  def __init__(self, name, section_path, course):
    self.course = course.subject + course.num
    self.name = name
    self.get_location(section_path)
    
  def get_location(self, section_path):
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
    
  def has_time_conflict(self, other_section):
    if self.days == other_section.days:
      if self.start >= other_section.start and self.start <= other_section.end:
        return True
      if other_section.start >= self.start and other_section.start <= self.end:
        return True
    return False  
    
  def linked(self, other_section):
    return (self.course == other_section.course) and (self.name[0] == other_section.name[0])

class Course:

  def get_page(self, semester, year):
    path = "https://courses.illinois.edu/cisapp/explorer/schedule/" + year + "/" + semester.lower() + "/" + self.subject + "/" + self.num + ".xml"
    response = requests.get(path)
    self.page = response.text
    if not len(self.page):
      raise ValueError
  
  def get_sections(self):
    soup = BeautifulSoup(self.page, "lxml-xml")
    self.sections = {}
    for section in soup.findAll("section"):
      self.sections[section.string] = Section(section.string, section.get('href'), self)


  def __init__(self, semester, year, course_num):
    try:
      self.subject = re.findall('\D+', course_num)[0]
      self.num = re.findall('\d+', course_num)[0]
      self.get_page(semester, year)
      self.get_sections()
    except:
      print("bad course number")