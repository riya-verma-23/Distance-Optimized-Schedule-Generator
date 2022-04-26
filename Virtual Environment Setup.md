# Virtual Environment Setup

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

#

To install all the dependencies for this project simply run 

```
pipenv update
```

## Note: 
Make sure you run ```pipenv shell``` in the same directory as the Pipfile