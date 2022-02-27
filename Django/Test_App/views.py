from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# Request -> Response


def hello_world(request):
    # return HttpResponse('Howdy World')
    return render(request, 'hello_world.html', {'fav_proff': 'Micheal Nowak'})
