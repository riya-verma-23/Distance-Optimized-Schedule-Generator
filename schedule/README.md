# Schedule 

The schedule class contains functions that create schedules given a list of linked sections

### Dependencies
* Python3 3.6.8

### Instance Variables 
* score: distance-time optimized score 
* linked sections: specific linked sections 
* schedule: outputted class schedule given linked sections

### Functions
* init(self, linked_sections): init function for Schedule object
* get_score(self): returns score of the schedule
* set_score(self, score): set score to compare schedule's for optimized distance and time
* get_linked_sections(self): get linked_sections list for given schedule
* split_sections_on_day(self):  returns a 2d list for daily schedule (which sections on each day)
* set_linked_sections(self, linked_section): set linked_sections list for given schedule 
* set_course(self, course): set course and linked_section for given schedule
* unique_days(self): returns the days whose distances need to be calculated
* has_time_conflict(self: returns whether there is a time conflict between two schedules
* return_locations(self): returns locations of all classes in the schedule

## Test Suite
Run `python3 test_schedule.py` to run the unit test cases for the Schedule Class