from django.urls import path
from api import views

urlpatterns = [
    path('yearsem/', views.YearSem.as_view()),
    path('sendcourse/', views.Course.as_view()),
    path('getcourselist/', views.get_course_obj),
    path('dailyschedule/<int:id>', views.get_daily_schedule),
]