# Distance-Optimized Schedule Generator


## 1. Summary of Presentation Introduction

Every semester, many students have trouble creating a schedule that minimizes the travel
distance. With our Distance Optimized Schedule Generator, Illinis will be able to build
an optimal, time-saving schedule that minimizes the distance between their classes.


## 2. Technical Architecture

![Alt text](tech_architecture.png?raw=true "Title")

## 3. Reproducible Installation Instructions

### Dependencies
* Python3 3.6.8
* beautifulsoup4 (4.10.0)
* bs4 (0.0.1)
* lxml (4.8.0)
* requests (2.27.1)
* urllib3 (1.26.8)

### Usage

The manage.py file can be used to control the Django server. To run the server you can use

```
python manage.py runserver
```
To run the front end, simply use

```
npm start
```

from within the virtual environment <sup>*</sup>

And simply running

```
python manage.py
```
will give you a list of commands 'manage.py' can run

### Testing

We will be using Django to write unit tests for our code. Since there is no module for writing unit tests for HTML and CSS, the front-end components of the project can be 'tested' by running 

```
python manage.py runserver
```

and opening the generated link in any browser.

### Note
Django requires you to set up a virtiual env to run it. Please look the 'Virtual Environment Setup' section below for a setup assistance.

### Virtual Environment Setup
We are using pipenv to create our virtual environment. 
If you do not have pipenv you can install it using

```
pip install pipenv
```

or

```
pip3 install pipenv
```
#

The given Pipfile defines the version of python and any dependencies being used and can be used to create the virtual environment using 

```
pipenv shell
```

### Note
Make sure you run ```pipenv shell``` in the same directory as the Pipfile

</br>

## 4. Group members + Roles

### Irina

* Wrote the Section, Course, and Linked Section class within web_scraping to parse data from courses.illinois.edu
* Wrote and Optimized functions to determine whether sections are linked, have atime conflict, etc.
* Worked on design doc to ensure backend communicates/interlinks smoothly
* Tested data extracted using BeautifulSoup

### Nalin

* Developed the old version of the frontend using UI mockups
* Hosted Web server using Django 
* Worked on integration allowing user input to be processed and passed into the relevant backend components
* Wrote relevant CRUD operations to accept user input and display the schedule (as an interactive google maps iframe + table)


### Riya
* Used Google Maps Distance Matrix API to retrieve relevant information regarding course's locations
* Parsed the JSON matrix into sensible data structure (edit)
* Wrote and optimized function to calculate score for each schedule option
* Helped improve frontend design 
* Worked on design doc to ensure backend communicates/interlinks smoothly
* Redesigned the frontend of the project using React and Tailwind CSS framework.

### Sanya
* Used Google Maps Static Map API to generate image used to display schedule
* Created Schedule Class to generate a schedule with linked sections split by the day 
* Wrote the test suite for the Schedule and MapsAPI class
* Worked on design doc and README.md

<!-- ![](resized.png?raw=true =200x200 ) -->
