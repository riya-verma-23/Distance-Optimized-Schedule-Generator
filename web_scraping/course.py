import section

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
     
    
  class LinkedSection:
    # linked sections
    self.sections = []
      
    # returns section at index i (can be called with [])
    def __getitem__(self, index):
      return sections[index]
