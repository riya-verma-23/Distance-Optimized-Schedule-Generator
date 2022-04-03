import sys
# var relativePath = Path.GetRelativePath(
#     @"course-project-tyk-b/web_scraping",
#     @"/Users/sanyasharma/Documents/UIUC/222/course-project-tyk-b/web_scraping");
# sys.path.insert(1, relativePath)
sys.path.insert(1, "/Users/sanyasharma/Documents/UIUC/222/course-project-tyk-b/web_scraping")

from course import Course
from section import Section
# class maintaining the Schedule 
class Schedule:
    '''
    Creates a Schedule object
  
    Member variables:
    score : distance-time optimized score
    linked sections : specific list sections to take
    schedule: outputted class schedule to take
    '''

# Initialize Schedule object given the score and linked_sections
    def __init__(self, linked_sections):
        self.score = -9
        self.linked_sections = linked_sections
            
    # get score to compare schedule's for optimized distance and time    
    def get_score(self):
        return self.score

    # set score to compare schedule's for optimized distance and time    
    def set_score(self, score):
        self.score = score

    # get linked_sections list for given course 
    def get_linked_sections(self):
        return self.linked_sections

    # set linked_sections list for given course 
    def set_linked_sections(self, linked_section):
        self.linked_sections = linked_section

    # set course and linked_section for given schedule
    def set_course(self, course):
        self.course = course
        self.linked_sections = course.get_linked_sections()

    # returns a 2d list for daily schedule (which sections on each day)
    # each day's list consists of sections on that day 
    # the sections are sorted ascendingly using start_time
    def split_sections_on_day(self):
        schedule_result = [[], [], [], [], []]
        result = []
        # for course in courses:
        #     for section in linked_section:
        for linked_section in self.linked_sections:
            for section in linked_section:
                if "M" in section.get_days():
                    schedule_result[0].append(tuple((section.get_name(), section.get_start())))
                if "T" in section.get_days():
                    schedule_result[1].append(tuple((section.get_name(), section.get_start())))
                if "W" in section.get_days():
                    schedule_result[2].append(tuple((section.get_name(), section.get_start())))
                if "R" in section.get_days():
                    schedule_result[3].append(tuple((section.get_name(), section.get_start())))
                if "F" in section.get_days():
                    schedule_result[4].append(tuple((section.get_name(), section.get_start())))

        for day in schedule_result:
            day.sort(key=lambda a: a[1])
        
        for day in schedule_result:
            only_sections = [ section[0] for section in day ]
            remove_duplicates = []
            for section in only_sections:
                if section not in remove_duplicates:
                    remove_duplicates.append(section)
            result.append(remove_duplicates)
        
        return result

    # returns the days that need to be calculated
    # removes all the day where there are repeats in the schedule
    def unique_days(self):
        unique_schedule = []
        for day in self.schedule:
            if day not in unique_schedule:
                unique_schedule.append(day)

    # returns list of days the section occurs during 
    def get_days_as_list(days):
        return [ day for day in days]

    def has_time_conflict(self):
        for i in range(0, len(self.linked_sections)):
            for j in range(0, len(self.linked_sections)):
                if (self.linked_sections[i].has_time_conflict(self.linked_sections[j])):
                    return True
        return False           

math241 = Course("spring", "2022", "MATH241" )
cs222 = Course("spring", "2022", "CS222" )

# create CS225 course object and input its linked sections into Schedule
cs225 = Course("spring", "2022", "CS225" )
# schedule = Schedule(cs225.get_linked_sections())
# print(schedule.split_sections_on_day())

# to-do - rename github folder to schedule + read.me + relative path + test.py
# write and test getters and setters for score and linkedsections
# write comments 
# PR message to write how to test