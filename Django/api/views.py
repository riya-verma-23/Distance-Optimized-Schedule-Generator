from django.shortcuts import render
from django.http import HttpResponse, QueryDict
from rest_framework.views import APIView
from django.views.generic import ListView
from rest_framework.response import Response
from django.views.generic.edit import CreateView
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view


import sys
import os
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
from course import Course as CourseConstructor
from schedule_class import Schedule
from distances import Distance
from mapsAPI import MapsAPI
import datetime
from collections import OrderedDict

# Create your views here.

year = ''
semester = ''
courses = OrderedDict()
schedule_dict = OrderedDict()
schedule_dict_obj = OrderedDict()
map_links = []

class Course(APIView):

    def post(self, request):
        global courses
        for c in request.data:
            c = c.replace(' ', '')
            courses[c] = ''
        print('courses', courses)
        return Response(status.HTTP_200_OK)
        

@csrf_exempt
@api_view(['GET'])
def get_course_obj(request):
    global courses
    global schedule_dict
    global schedule_dict_obj
    course_obj = []
    for course_key in courses:
        c = CourseConstructor(semester.lower(), year, course_key.upper())
        course_obj.append(c)
    print(course_obj)
    best_schedule = Distance.best_schedule(course_obj)
    
    for i in range(len(best_schedule)):
        if i > 5: break
        schedule_dict_obj[i] = best_schedule[i]
        print("best score: ", best_schedule[i].get_score())
        for ls in best_schedule[i].get_linked_sections():
            for s in ls:
                courses[s.get_course()] += s.get_name() + ' '

        print(courses)
        schedule = []
        for key, value in courses.items():
            schedule.append(value)
            courses[key] = ''
        schedule_dict[i] = schedule
    
    print(schedule_dict)

    return Response(schedule_dict)
    
@csrf_exempt
@api_view(['GET'])
def get_daily_schedule(request, id):
    global map_links
    map_links = MapsAPI.map_API_schedule(schedule_dict_obj[id])
    print(map_links)
    week_schedule = Schedule.split_sections_on_day(schedule_dict_obj[id])
    print('ws', week_schedule)
    ws = []
    for ds in week_schedule:
        day_schedule = []
        for s in ds:
            day_schedule.append(s.get_course() + ' Section ' + s.get_name())
        ws.append(day_schedule)
    return Response([ws, map_links])

class YearSem(APIView):
    def post(self, request):
        global year
        year = request.data.get('year')
        global semester
        semester = request.data.get('semester')
        return Response(status.HTTP_200_OK)