# Web Scraping
Course, Section, LinkedSection classes encapsulate functions that get and access section location, time, etc info.

## How To Use

### Dependencies
* Python3 3.6.8
* beautifulsoup4 (4.10.0)
* bs4 (0.0.1)
* lxml (4.8.0)
* requests (2.27.1)
* urllib3 (1.26.8)

### Example
* Get year, semester, SUBJ### from UI
* `course = Course('year', 'semester', 'SUBJ###')`
* `linked_sections = course.get_linked_sections()`
* linked_sections used in other modules

## Course

### Instance variables
* **page**: Course XML file as a string
* **section**: Dictionary of the course's sections, where the key is section name
* **subject**: i.e. MATH
* **num**: i.e. 241
* **semester**: i.e. spring
* **year**: i.e. 2022

### Functions
* **get_page(self, semester, year)**: Init self.page with course XML file as a string
* **init_sections(self)**: Init self.sections dictionary using course XML file and section XML files
* **__init__(self, semester, year, course_num)**: init function for Course objects, uses course XML file and section XML files
* **__eq__(self, other)**: return whether two courses are equal
* **split_sections_on_type(self)**: Return dictionary of sections split by type (key: section type, value: list of sections of that type)
* **has_time_conflict(self, section_list)**: Return whether a list of sections has a time conflict
* **linked(self, section_list)**: Return whether all sections in a list are linked
* **get_linked_sections(self)**: Return a list of LinkedSections each encapsulating a valid combo of three sections of each type
* **get_section(self, section_name)**: Return sections[section_name]
* **get_subject(self)**: Return course subject
* * **get_subject(self)**: Return course section
* * **get_number(self)**: Return course number
* * **get_semester(self)**: Return course semester
* * **get_year(self)**: Return course year

## LinkedSection
Instance Variables
* **sections**: Combination of sections as a list

Functions
* **add_section(self, section)**: Add a section to self.sections
* **__getitem__(self, index)**: Returns section at index i (can be called with [])
* **__len__(self)**: Returns # linked sections (can be called with len(linked_section))
* **__eq__(self, other)**: Check if two LinkedSections are equal

## Section

### Instance variables
* **course**: Course the section belongs to
* **name**: Section name (i.e. ADB)
* **section_type**: i.e. Lecture, Discussion
* **location**: i.e. Altgeld Hall
* **days**: days the Section meets. i.e. MWF, TR or ASYNC for async section
* **start**: datetime object representing start time i.e. 08:00:00 or 00:00:00 for async
* **end**: datetime object representing end time i.e. 08:50:00 or 00:00:00 for async

### Functions
* **__init__(self, name, section_path, course)**: Init function for Section using section XML file
* **__eq__(self, other)**: check if two Sections are the same
* **init_location(self, section_path)**: Initialize location, section type, meeting days, and start and end time from Section XML file
* **has_time_conflict(self, other_section)**: Get whether two sections have a time conflict
* **linked(self, other_section)**: Determine whether two sections are linked
* **get_course(self)**: Get course name this section belongs to 
* **get_name(self)**: Get section name
* **get_type(self)**: Get section type
* **get_location(self)**: Get location
* **get_days(self)**: Get section days
* **get_start(self)**: Get datetime obj representing start time
* **get_end(self)**: Get datetime obj representing end time
