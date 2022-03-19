class Schedule:
    def __init__(self, score_, linked_sections_):
        self.score = score_
        self.linked_sections = linked_sections_
    
def getScore():
    return self.score


def split_sections_on_day(schedule):
    schedule = [[]]
    result = []
    for course in linked_sections:
        for section in course:
            if "M" in section.list(get_days())
                schedule[0].append(tuple((section, get_start())))
            if "T" in section.list(get_days())
                schedule[1].append(tuple((section, get_start())))
            if "W" in section.list(get_days())
                schedule[2].append(tuple((section, get_start())))
            if "R" in section.list(get_days())
                schedule[3].append(tuple((section, get_start())))
            if "F" in section.list(get_days())
                schedule[4].append(tuple((section, get_start())))


# [[(225Lecture, 9:00AM), (446, 8:00AM)]]
    for day in schedule:
        day.sort(key=lambda a: a[1])
    
    for day in schedule:
       only_sections = [ section[0] for section in day ]
       result.append(only_sections)

def unique_days():
    list(set(this.schedule))