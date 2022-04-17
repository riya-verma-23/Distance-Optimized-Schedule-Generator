import sys
sys.path.insert(0, "web_scraping")
from course import Course
from section import Section

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

    # get linked_sections list for given schedule 
    def get_linked_sections(self):
        return self.linked_sections

    # set linked_sections list for given schedule 
    def set_linked_sections(self, linked_section):
        self.linked_sections = linked_section

    # set course and linked_section for given schedule
    def set_course(self, course):
        self.course = course
        self.linked_sections = course.get_linked_sections()

    # returns a 2d list for daily schedule (which sections on each day)
    # each day's list consists of section objects on that day 
    # the sections are sorted ascendingly using start_time
    def split_sections_on_day(self):
        schedule_result = [[], [], [], [], []]
        result = []
        for linked_section in self.linked_sections:
            for section in linked_section:
                if "M" in section.get_days():
                    schedule_result[0].append(tuple((section, section.get_start())))
                if "T" in section.get_days():
                    schedule_result[1].append(tuple((section, section.get_start())))
                if "W" in section.get_days():
                    schedule_result[2].append(tuple((section, section.get_start())))
                if "R" in section.get_days():
                    schedule_result[3].append(tuple((section, section.get_start())))
                if "F" in section.get_days():
                    schedule_result[4].append(tuple((section, section.get_start())))

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

    # returns a 2d list for daily schedule (which sections on each day)
    # each day's list consists of sections names on that day 
    # the sections are sorted ascendingly using start_time
    def split_sections_on_day_str(self):
        schedule_result = [[], [], [], [], []]
        result = []
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

    # returns the days whose distances need to be calculated
    # removes all the day where there are repeats in the schedule
    def unique_days(self):
        unique_schedule = []
        for day in self.schedule:
            if day not in unique_schedule:
                unique_schedule.append(day)

    # returns list of days the section occurs during 
    def get_days_as_list(days):
        return [ day for day in days]

    # returns whether there is a time conflict between two schedules
    def has_time_conflict(self):
        for i in range(0, len(self.linked_sections)):
            for j in range(0, len(self.linked_sections)):
                if (self.linked_sections[i].has_time_conflict(self.linked_sections[j])):
                    return True
        return False

    # returns locations of all classes in the schedule
    def return_locations(self):
        result = []
        schedule = self.split_sections_on_day()
        for day in schedule:
            locations = []
            for section in day:
                if section.get_location() not in locations:
                    locations.append(section.get_location())
            result.append(locations)
        return result

cs225 = Course("spring", "2022", "CS225" )
# cs233 = Course("spring", "2022", "CS233")
aas283 = Course("spring", "2022", "AAS283" )
stat200 = Course("spring", "2021", "STAT200" )
schedule =  Schedule(cs225.get_linked_sections())
# print(schedule.has_time_conflict())
# print(schedule.has_time_conflict())
# print(schedule.return_locations())