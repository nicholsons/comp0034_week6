# Create a new Flask app project and modify the file and folder structure
The following gives instructions for using Flask and indicates where you should find instructions for other IDEs.

## Create a new project with a basic Flask app
In PyCharm Project you simply create a new Flask project and this will install Flask and any dependencies and create the basic folder structure and app.py.

For other IDEs follow the [installation instructions](https://flask.palletsprojects.com/en/1.1.x/installation/#install-flask) in the Flask documentation.

## Add a README.md
Create a new file called README.md.

You will need to use markdown to edit the file.

For now you can copy the following into README.md:

## Create a requirements.txt
Open the Terminal in PyCharm (or open a command line and navigate to your venv).

Enter `pip freeze > requirements.txt`

This will generate a requirements.txt file with the package dependencies for the project. Note: if you add more dependency packages to your project you will need to either add these to requirements.txt or run the command again and replace the existing file.

```markdown
# Flask app structure
A minimal app to demonstrate how to structure and configure a Flask app.
```

## Add a .gitignore file
If you are using PyCharm and have installed and enabled the .ignore plug in then you should be able to select File | New | .ignore file | .gitignore

Find and select the JetBrains (if using PyCharm) and the Python templates and create the .ignore.

## Create a new python package for the app
In PyCharm this is File | New | Package. You can call it `my_app` or any name you wish.

If you create a directory from a command line then inside the directory you need to create a blank python file called `__init__.py` (in Pycharm this is created when you select the Python Package option for the new file).

## Move the static and template folders and app.py into the python package you just created
If you are working in an IDE then you should use refactoring to move files so that any references to them in other files are updated. 
In PyCharm you can use Refactor | Move (though dragging to another folder within PyCharm refactors by default).

## Create setup.py and MANIFEST.in
Read [Making the project installable](https://flask.palletsprojects.com/en/1.1.x/tutorial/install/) and then create a `setup.py` and `MANIFEST.in` for your project.

The might look like this:
```python
# setup.py

from setuptools import find_packages, setup

setup(
    name='my_app',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
```
```text
# MANIFEST.in

graft my_app/static
graft my_app/templates
global-exclude *.pyc
```

## Check your structure
You should now have something like this:
```
/yourapplication
    /my_app
        __init__.py
        app.py
        /static
            ... css will go here
        /templates
            ... html files will go here
    /venv
    .gitignore
    README.md
    setup.py
```

You will need to copy in the `dash_app` directory and sub-directories and the `data` directory from the [week 5 GitHub repository](https://github.com/nicholsons/comp0034_week5) into your Flask app.

We will add further files to this structure by the end of this week's activities.

See [Flask structure recommendations](https://flask.palletsprojects.com/en/1.1.x/patterns/packages/) for more guidance.
