import imp
import os
import sys

from django.shortcuts import render
from numpy import size

sys.path.append(os.path.join(os.path.dirname(
    sys.path[0]), 'web_scraping'))
sys.path.append(os.path.join(os.path.dirname(
    sys.path[0]), 'schedule'))
sys.path.append(os.path.join(os.path.dirname(
    sys.path[0]), 'distances_optimize'))
sys.path.append(os.path.join(os.path.dirname(
    sys.path[0]), 'maps'))

from section import Section
from course import Course
from schedule import Schedule
from distances import Distance
from mapsAPI import generateMapAPITwo

# Create your views here.

# frontend_components is a dictionary of parameters that have to be
# displayed on the homepage that should be recived from the backend

# Restrict API key
# frontend_components = {
#     'class_1': 'CS 225',
#     'class_2': 'CS 222',
#     'class_3': 'CS 233',
#     'class_4': 'MATH 257',
#     'class_5': 'ANTH 103',
#     'section_1_1': 'AL2',
#     'section_1_2': 'AL3',
#     'section_2_1': 'DC2',
#     'section_2_2': 'CL8',
#     'section_3_1': 'M8',
#     'section_3_2': 'GR8',
#     'section_4_1': 'R2',
#     'section_4_2': 'D2',
#     'section_5_1': 'C3',
#     'section_5_2': 'P0',
# }


# Maps api requires locations list
# Course.py no input validation needed

def homepage(request):
    semester = None
    year = None
    classes = []
    maps_link = None
    sections = []

    if request.method == "POST":
        # print(request.POST)  # Printing out the user input from the Front End
        if 'sem' in request.POST:
            request.session['semester'] = request.POST['sem']
            request.session['year'] = request.POST['year']

        if 'sub' in request.POST:
            course_no = request.POST['sub']+request.POST['course_no']
            if 'classes' in request.session:
                if course_no not in request.session['classes']:
                    request.session['classes'].insert(0, course_no)
                    request.session.modified = True
            else:
                request.session['classes'] = [course_no]
                request.session.modified = True

    if 'classes' in request.session:
        classes = request.session['classes']

    if 'semester' in request.session:
        semester = request.session['semester']

    if 'year' in request.session:
        year = request.session['year']
    
    if 'sections' in request.session:
        sections = request.session['sections']
    
    if 'maps_link' in request.session:
        maps_link = request.session['maps_link']

    context = {
        'semester': semester, 'year': year,
        'maps_link': maps_link, 'classes': classes,
        'sections': sections}

    return render(request, 'homepage.html', context)


def reset_session(request):
    try:
        del request.session['classes']
        del request.session['semester']
        del request.session['year']
        del request.session['sections']
        del request.session['maps_link']
    except KeyError:
        pass
    return homepage(request)


def generate_schedule(request):
    if 'classes' in request.session:
        course_list=[]
        for course in request.session['classes']:
            course_list.append(Course(request.session['semester'], request.session['year'], course))
            print(course_list[size(course_list)-1])

        schedules=Distance.best_schedule(course_list) #Bug with CS 440, Math 416 + Input Validation (Fall 2021?)
                                                      #Index out of bounds at line 188 or sections not found(ln 145)
        best_schedule=schedules[0]
        section_list=[]
        location_list=[]
        for course in best_schedule.get_linked_sections():
            #print(course[0].get_course()+" "+course[0].get_name()+" "+course[0].get_location())
            section_list.append(course[0].get_name())
        
        for course in best_schedule.get_linked_sections():
            location_list.append(course[0].get_location())
        
        request.session['sections']=section_list
        request.session['maps_link']=generateMapAPITwo(location_list)
        #print(request.session['maps_link'])
        
    return homepage(request)
