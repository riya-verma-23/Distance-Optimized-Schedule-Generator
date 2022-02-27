from django.urls import path
from . import views


# Assigning a Reference to a function to a URL
urlpatterns = [
    path('', views.homepage),
]
