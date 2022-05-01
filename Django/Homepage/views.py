import imp
import os
import sys

from django.shortcuts import render
from numpy import size
from django.contrib import messages

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
from schedule_class import Schedule
from distances import Distance
from mapsAPI import MapsAPI

# Create your views here.


def homepage(request):
    semester = None
    year = None
    classes = []
    map_links = []
    sections = []

    if request.method == "POST":
        print(request.POST)  # Printing out the user input from the Front End
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
    
    if 'map_links' in request.session:
        map_links = request.session['map_links']

    context = {
        'semester': semester, 'year': year,
        'map_links': map_links, 'classes': classes,
        'sections': sections}

    return render(request, 'homepage.html', context)


def reset_session(request):
    try:
        del request.session['classes']
        del request.session['semester']
        del request.session['year']
        del request.session['sections']
        del request.session['map_links']
    except KeyError:
        pass
    return homepage(request)


def generate_schedule(request):
    if 'classes' in request.session:
        course_list=[]
        for course in request.session['classes']:
            #try catch here for bad course num ValueError
            try:
                course_list.append(Course(request.session['semester'], request.session['year'], course))
                print(course_list[size(course_list)-1])
            except ValueError:
                messages.error(request,"Invalid Course. Please Reset and try again.")
                return homepage(request)
            except:
                messages.error(request,"Unknown Error")
                return homepage(request)

        try:
            schedules=Distance.best_schedule(course_list)
            best_schedule=schedules[0]
            section_list=[]
            for course in best_schedule.get_linked_sections():
                linked_sections=''
                for linked_section in course:
                    linked_sections+=linked_section.get_name()+' '

                section_list.append(linked_sections)
            
            
            request.session['sections']=section_list
            request.session['map_links']=MapsAPI.map_API_schedule(best_schedule)
        except:
            messages.error(request,"No Schedule Found")
            return homepage(request)
        
        
    return homepage(request)