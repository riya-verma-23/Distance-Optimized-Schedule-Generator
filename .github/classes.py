class Course: 
    # def __init__(self, subject_, num_, page_, sections_):
    #     self.subject = subject_
    #     self.num = num_
    #     self.page = page_
    #     self.sections = sections_

    def __init__(self, semester_, year_, course_num_): 
        self.semester = semester_
        self.year_ = year_
        self.crn = course_num_

     
    def get_page(semester, year): 
        # return's page from the API
        return "https://courses.illinois.edu/schedule/2022/spring/CS/222"

    def get_sections(self)
        # return list of sections for the course
        return self.sections

class Section:
    def __init__(self, name_, section_path_, course_):
        self.name = name_
        self.path = section_path_
        self.course = course_

    def get_location(section_path):
        # return location scraped from the course listings page
        pass 

    def has_time_conflict(other_section):
        # return bool if time conflict w other_section
        pass 

    def is_linked(other_section):
        # whether linked with another section?
        pass

