from django.shortcuts import render
# Create your views here.

# frontend_components is a dictionary of parameters that have to be
# displayed on the homepage that should be recived from the backend

# Restrict API key
# frontend_components = {
#     'maps_link': 'https://www.google.com/maps/embed/v1/directions?origin=place_id:ChIJf5sYMRrXDIgRv9cFI6s4og8&destination=place_id:ChIJqXmEqmvXDIgRMJY1DdQBn04&key=AIzaSyC5EWe12L9MWFK0Um6aRdVkZd6eMETlNnY',
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

maps_link = 'https://www.google.com/maps/embed/v1/directions?origin=place_id:ChIJf5sYMRrXDIgRv9cFI6s4og8&destination=place_id:ChIJqXmEqmvXDIgRMJY1DdQBn04&key=AIzaSyC5EWe12L9MWFK0Um6aRdVkZd6eMETlNnY'
sections = ['AL2', 'AL3', 'DC2', 'CL8', 'M8']


# Maps api requires locations list

def homepage(request):
    classes = []
    if request.method == "POST":
        # print(request.POST)  # Printing out the user input from the Front End
        course_no = request.POST['sub']+' '+request.POST['course_no']
        if 'classes' in request.session:
            if course_no not in request.session['classes']:
                request.session['classes'].insert(0, course_no)
                request.session.modified = True
        else:
            request.session['classes'] = [course_no]
            request.session.modified = True

    if 'classes' in request.session:
        classes = request.session['classes']

    context = {
        'maps_link': maps_link, 'classes': classes,
        'sections': sections}

    return render(request, 'homepage.html', context)


def reset_session(request):
    try:
        del request.session['classes']
    except KeyError:
        pass
    return homepage(request)
