# comp0034_flask_basics
COMP0034 starter code for week 5

This repository contains the activities and starter code for week 5.

A repository showing completed examples of the activities can be found at TBC.

### Setup
After forking or cloning the repository you will need to:
1. Add a venv to the project
2. Open requirements.txt and install the required packages
3. Go to settings/preferences | Project Structure and click on the templates folder then select Templates from the ‘Mark as: ‘ line of options
4. You may need to change the templating language to Jinja2. In the project preferences/settings | Languages and Frameworks | Template Languages and then select Jinja2 in the dropdown and press OK
5. Check Flask is set in Settings/Preferences | Languages & Frameworks | Flask. Tick 'Flask integration' and Apply.


### Activity 1: Create the Flask app structure
1. Create a new Python Package called 'app' in the project structure
2. Use the Refactor > Move directory option to move the static and templates directories into the 'app' package
3. Create a basic MVC structure
    1. Move models.py (model) to the ‘app’ package
    2. Index.html (view) has already been created in the ‘templates’ folder.
    3. Create a python package within the ‘app’ package called ‘main’. Move routes.py (controller) to ‘main’.
4. Edit config.py and create your own SECRET_KEY. To do this open a Python Console (bottom of PyCharm window) and enter:
    ```python
    import secrets
    secrets.token_urlsafe(16)
    ```
    You can then copy and paste the resulting key into config.py.
5. Create the Flask app using the factory pattern. Open `app/__init__.py` and add the following:
    ```python
   from flask import Flask
   from flask_sqlalchemy import SQLAlchemy
   from my_app.config import DevConfig


   # The SQLAlchemy object is defined globally
   db = SQLAlchemy()

   def create_app(config_class=DevConfig):
       """
        Creates an application instance to run
        :return: A Flask object
        """
       app = Flask(__name__)

       # Configure app wth the settings from config.py
       app.config.from_object(config_class)
   
       # Allow the app to access to the database
       db.init_app(app)
       # Import the models and then create the database with the tables
       from my_app.app import Teacher, Student, Course, Grade
       with app.app_context():
           db.create_all()
   
       # Default route to be moved later in the lecture
       @app.route('/')
       def index():
           return "Hello, World!"

       return app
   ```
6. Edit app.py to call the create_app() function to run your Flask app.
    ```python
   from my_app.app import create_app
   
   app = create_app()
   app.app_context().push()
    ```
   
   The line `app.app_context().push()` allows you to use `current_app` later in the code and is required to allow the app to access the global SQLAlchemy database see https://flask.palletsprojects.com/en/1.1.x/appcontext/ for more detail.
7. Right click on app.py in PyCharm and select the option to run as a Flask app.

### Activity 2: Create Jinja2 templates
1. Create `layout.html` in the templates folder.
    1. Open index.html and 'save as' to create layout.html
    2. Edit layout.html so that the `<title>` can be set for each page using a Jinja2 expression
        ```jinja2
        {#  Allows each page title to be set using a variable named 'title' #}
        {% block title %}{{ title }}{% endblock %}
        ```
    3. Edit layout.html so that within the main div there is a Jinja2 statement for the main content e.g.
        ```jinja2
       {# Child pages add page specific content here #}
       {% block content %}
       {% endblock %}
        ```
    4. Update the reference to the static css file with a Jinja2 reference:
    ```jinja2
    <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.css') }}">
    ```
2. Create a new HTML file called index.html in the templates folder and delete the provided HTML code. Add Jinja2 code to:
    1. Inherit (extends) `layout.html` e.g. `{% extends "layout.html" %}`
    2. Provide the page title ‘home’ in the title block e.g. `{% block title %} Home {% endblock %}`
    3. Add a new Jinja2 variable name to create a tag that would be result in `<h1>Hello, name</h1>` e.g. `<h1>Hello, {{ name }}</h1>`
3. Edit the default route in `app\__init__py` so that it renders index.html using the Flask function `render_template()`
    ```python
    from flask import render_template

   @app.route('/')
   def index():
       return render_template('index.html')
    ```  
4. Stop the Flask app and re-run it.
  
### Activity 3 Create a blueprint for the `main` package
1. Delete the route for index from the `create_app()` function in `app\__init__py`.
2. Edit `routes.py` in main with the following:
   ```python
   from flask import Blueprint

   bp_main = Blueprint('main', __name__)
   
   @bp_main.route('/')
   def index():
       return render_template('index.html') 
   ```
   This creates a Blueprint named 'main'. 
3. Import and register the blueprint from the factory using `app.register_blueprint()`. Place the new code at the end of the `create_app()` function before returning the app.
    ```python
   # Register Blueprints
   from my_app.app import bp_main
       app.register_blueprint(bp_main)
   ```
4. Stop and restart the Flask app.

### Activity 4: Enable flash messaging
1. Add the following code to the start of the main div in the base template.
    ```jinja2
    {# Displays flashed messages on a page #}
    {% with messages = get_flashed_messages() %}
        {% if messages %}
            <ul>
            {% for message in messages %}      
                <li>{{ message }}</li>
            {% endfor %}
            </ul>
        {% endif %}
    {% endwith %}
    ```

