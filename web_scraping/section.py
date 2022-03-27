from bs4 import BeautifulSoup
import re
import requests
import datetime


class Section:
  '''
  Creates a Section object
  
  Member variables:
  course: the course the Section belongs to
  name: the name of the section (i.e. ADB)
  section_type: i.e. Lecture, Discussion
  location: i.e. Altgeld Hall
  days: days the Section meets. i.e. MWF, TR or ASYNC for async section
  start: datetime object representing start time i.e. 08:00:00 or 00:00:00 for async
  end: datetime object representing end time i.e. 08:50:00 or 00:00:00 for async
  '''
  # TODO: someone add to readme dependencies, use pipenv
  # TODO: update documentation with new web scraping changes
  # TODO: add semester and year boxes to webpage? or infer from current year
  # TODO: work with Nalin to send relevant data to Section and Course modules
  # TODO: PRs with all modules by next week
  # TODO: resolve git pull, push issue (keep verified)
  # Initialize Section object given the section name, path to the section's xml file,
  # and its Course
  def __init__(self, name, section_path, course):
    self.course = course.subject + course.num
    self.name = name
    self.init_location(section_path)

  # modifying Riya's version (below) copy pasted here due to problems with git pull
  # TODO: update PR during feedback (work in progress don't merge)
  # TODO: nice to have more detail in PR description for reviewers how to run it etc 
  # (how to use LinkedSection etc)
  # def __eq__(self, other):
  #  return (self.course == other.course) and (self.name == other.name)

  # check if two Sections are the same
  def __eq__(self, other):
    # TODO: make this not one line
    return self.course == other.get_course() and self.name == other.get_name() and self.section_type == other.get_type() and self.location == other.get_location() and self.days == other.get_days() and self.start == other.get_start() and self.end == other.get_end()
  
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

    # if there's an entry for days of the week, set days to that
    # otherwise, set to "ASYNC" to mark section as asynchronous  
    days = soup.findAll("daysOfTheWeek")
    if len(days):
      self.days = days[0].string.strip()
    else:
      self.days = "ASYNC"
    
    # if there's an entry for start, end, set start, end to those
    # otherwise, set start and/or end to 00:00 to mark section as asynchronous
    st = soup.findAll("start")
    try:
      self.start = datetime.datetime.strptime(st[0].string, '%I:%M %p')
    except:
      self.start = datetime.datetime.strptime("00:00:00", '%H:%M:%S')

    end = soup.findAll("end")
    try:
      self.end = datetime.datetime.strptime(end[0].string, '%I:%M %p')
    except:
      self.end = datetime.datetime.strptime("00:00:00", '%H:%M:%S')
  
  # Get whether two sections have a time conflict
  # If one starts between the other's start and end times, there's a time conflict
  # A section cannot have a time conflict with itself
  def has_time_conflict(self, other_section):
    if self != other_section and (self.days in other_section.get_days() or other_section.get_days() in self.days):
      if self.start >= other_section.start and self.start <= other_section.end:
        return True
      if other_section.start >= self.start and other_section.start <= self.end:
        return True
    return False  
  
  # Determine whether two sections are linked
  # If two sections belong to the same course and have the same first letter, they're linked
  def linked(self, other_section):
    return (self.course == other_section.course) and (self.name[0] == other_section.get_name()[0])
  
  # Get course name this section belongs to 
  def get_course(self):
    return self.course
  
  # Get section name
  def get_name(self):
    return self.name
  
  # Get section type e.g. "Lecture"
  def get_type(self):
    return self.section_type

  # Get location e.g. "Altgeld Hall"
  def get_location(self):
    return self.location

  # Get days the section meets e.g. "TR"
  def get_days(self):
    return self.days
  
  # Get datetime obj representing start time
  def get_start(self):
    return self.start
  
  # Get datetime obj representing end time
  def get_end(self):
    return self.end
