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