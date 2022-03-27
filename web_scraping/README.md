# Web Scraping
Course, Section, LinkedSection classes encapsulate functions that get and access section location, time, etc info.

## How To Use

### Dependencies
### Example

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
