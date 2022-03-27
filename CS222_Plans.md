## **CS 222 Schedule Generator Design**

Resources to Potentially Use :[ https://courses.illinois.edu/cisdocs/api](https://courses.illinois.edu/cisdocs/api)


### **Class Section (Irina) (Latest info in web_scraping/README.md)**



* Member Variables
    * Course :the Section belongs to
    * Name : the name of the section (i.e. ADB)
    * Section type : discussion, lecture, recitation
    * Location
    * Days : i.e. MWF, TR
    * Start Time
    * End Time
* Functions
    * init__(name, section_path, course)
    * init_location(section_path): initialize location, section type, meeting days, and start and end time from section xml file
    * has_time_conflict(other_section) —> bool
    * linked(other_section) —> bool : if two sections belong to same course and same first letter
    * get_course()
    * get_name()
    * get_type()
    * get_location()
    * get_days()
    * get_start()
    * get_end()


### **Class Course (Irina)  (Latest info in web_scraping/README.md)**



* Member Variables:
    * subject
    * number
    * page : Course’s xml file as a string
    * sections : dictionary of the sections {key = section name, value : Section }
* **init**(semester, year, course_num)
* get_page(semester, year) : Get course page using semester, year, and already init subject and number
* init_sections() : Initialize the sections dictionary using each course's XML file
* get_section(section_name)
* get_subject()
* get_number()
* split_sections_on_type() —> dictionary (key: type, value: vector)
    * takes all sections from dictionary and splits it based on type
    * Discussion = [ section A, section B ]
    * Lecture = [ section C, section D ]
    * Lab = [ section E, section F ]
    * returns [ [Discussion] , [Lecture] , [Lab] ]
* get_linked_sections( output of split_sections_on_type ) → list of linked sections
    * list of all possible groups of linked sections (just the required e.g. lab, discussion, lecture) ex. {...{section discussion, section lecture, section lab}...}
    * Uses HasTimeConflict() to eliminate some linked section combinations
    * parameter is what helper function split_sections_on_type() returns
* has_time_conflict(section_list) → use Section has_time_conflict() to determine if section list has time conflict
* Operator = needs to be defined between two sections


#### **Class Linked Section (Latest info in web_scraping/README.md)**



* Member Variables:
    * sections = []
* __init__(self, sections)
* __getitem__(self, index) → returns item at index i (similar to operator[] in C++)
* add_section(self, section)


### **Class Schedule (Sanya)**



* Member Variables
    * score : to compare with other schedule - optimized distance and time
    * linked sections : specific set of linked sections to take, 1 linked section for each course
* Functions
    * get_score()
    * init(score, linked sections)
    * split_sections_on_day ( schedule ) →  returns a daily schedule (sections on each day)
        * List with indices with 0-4 being Mon-Fri 
    * unique_days() → returns the days that need to be calculated
        * Given the list of LinkedSections in the schedule, determine which days’ distances need to be calculated


### **Class Distance-Optimizer (using Distance Matrix) (Riya)**



* Member Variables
    * map &lt; (section, section), dist > distances : stores all distances made with the API call to minimize amount of calls
* Functions
    * generate_all_possible_schedules( list of courses) → list of all schedules
        * Takes in list of Linked Sections (using getLinkedList() ) for each course → returns all possible **Schedules**
        * when creating schedule, checks if IsValidSchedule() and calculate_score()
    * find_best_schedule( all schedules )
        * finds the minimum score, get_score()
    * calculate_score( Schedule )
        * Calls split_sections_on_day() and passes daily schedule to calculate_perimeter_for_day(), returning the sum of perimeters for each day (which is Schedule’s score)
    * calculate_perimeter_for_day() : makes a Distance Matrix API call between two sections if it hasn’t made one already
        * Determine the list of tuples, sort() it, you need to call to api and check if map contains it => if not call API => helper called eliminate_called_sections()
        * Calls distance_matrix(origins, destinations) and returns a matrix
    * traverses the matrix returned to sum up distances
    * If distance matrix api call made, then stores the data in a map &lt; (section, section), dist > to be accessed later


### **FrontEnd Files(Nalin):**

**templates/hompage.html & static/css/hompage-style.css:**



* Sections:
    * Title:
        * Font: Montserrat, sans-serif 
        * Color: #e7c519
    * Inputs->Section for obtaining user input:
        * Centered text-box with a submit button
        * Color: #ffac12
    * Schedule-> Section for displaying the distance optimized schedule as a map with an accompanying table to display the course with their sections
        * Font: Montserrat, sans-serif 
        * Colors: #ffce74, #00c3ff63

**Django/Homepage/views.py:**



* Member Variables
    * map &lt; string, string > frontend_components : stores all components that have to be generated by the backend and have to be displayed
* Functions
    * homepage(request)→ rendering the homepage
        * Checks if input has been received, and calls the relevant functions in course and section
        * Renders the homepage.html with the static files (homepage-style.css)**	**


### **External Functions**

is_valid_schedule( linked section set —> schedule) —> bool : checks for time conflicts for linked sections across classes

distance_matrix(origins, destinations) makes the API call

generate_matrix_from_JSON()