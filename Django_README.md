# Django

This project is using Django for hosting  our frontend, for integration between the backend and frontend, and for testing.

## Structure:

Each major component of the frontend is coded as its own application and the admin application called 'Distance_Optimized_Schedule_Generator' synchronizes the working of all the applications. 

The HTML code for each application can be found in the templates folder within that applications directory and is being used by views.py and urls.py for rendering and display

The CSS code for each application can be found in the static folder which is a folder within the main Django directory, within which all the application sub-directories exist. 

## Usage:

The manage.py file can be used to control he Django server. To run the server you can use

```
python manage.py runserver
```


from within the virtual environment <sup>*</sup>

And simply running

```
python manage.py
```
will give you a list of commands 'manage.py' can run

## Testing:

We will be using Django to write unit tests for our code. Since there is no module for writing unit tests for HTML and CSS, the front-end components of the project can be 'tested' by running 

```
python manage.py runserver
```

and opening the generated link in any browser.

### Note: 
Django requires you to set up a virtiual env to run it. Please look at 'Virtual Environment Setup.md' for a setup assistance.
