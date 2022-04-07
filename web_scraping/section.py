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
  term: term this Section is part of i.e. 1 = whole semester, A = 1st 8 weeks,
        B = last 8 weeks, N/A means no value provided
        src: https://registrar.illinois.edu/academic-calendars/academic-calendars-archive/fall-2021-academic-calendar/
  '''

  # Initialize Section object given the section name, path to the section's xml file,
  # and its Course
  def __init__(self, name, section_path, course_str):
    self.course = course_str
    self.name = name
    self.init_location(section_path)

  # check if two Sections are the same
  # modifying Riya's version (below) copy pasted here due to problems with git pull
  # def __eq__(self, other):
  #  return (self.course == other.course) and (self.name == other.name)
  def __eq__(self, other):
    return self.course == other.get_course() and\
      self.name == other.get_name() and\
      self.section_type == other.get_type() and\
      self.location == other.get_location() and\
      self.days == other.get_days() and\
      self.start == other.get_start() and\
      self.end == other.get_end()
  
  # Initialize location, section type, meeting days, and start and end time
  # from Section XML file
  def init_location(self, section_path):
    try:
      soup = BeautifulSoup(requests.get(section_path).text, "lxml-xml")
    except:
      raise ValueError("timeout")
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
    
    term = soup.findAll("partOfTerm")
    if(len(term)):
      self.term = term[0].string
    else:
      self.term = "N/A"
  
  # Determine if there's an overlap in days between two sections
  # Fixing bug in Section has_time_conflict
  # Example: one course has WF, other MW. Before this change, 
  # this days overlap would not be detected
  def days_overlap(days, days1):
    if days == days1:
      return True
    for day in days:
      if day in days1:
        return True
    return False

  # Get whether two sections have a time conflict
  # If one starts between the other's start and end times, there's a time conflict
  # A section cannot have a time conflict with itself
  def has_time_conflict(self, other_section):
    if (self != other_section and Section.days_overlap(self.get_days(), other_section.get_days())):
      
      if self.start >= other_section.start and self.start <= other_section.end:
        return True
      if other_section.start >= self.start and other_section.start <= self.end:
        return True
    return False  
  
  # Determine whether two sections are linked
  # If two sections belong to the same course and have the same first letter, they're linked
  def linked(self, other_section):
    return ((self.course == other_section.course) and 
    (self.name[0] == other_section.get_name()[0]))
  
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
  
  # Get term: "1", "A", "B", or "N/A"
  def get_term(self):
    return self.term
  
  # Hash function for section (for dictionary used in distance matrix module)
  def __hash__(self):
      return (hash((self.name, self.section_type, self.location,
       self.start.strftime("%H:%M"), self.end.strftime("%H:%M"), self.days, self.course)))
