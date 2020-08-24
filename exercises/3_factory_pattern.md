# Apply the Factory pattern to a Flask app

In this activity we will cover an architectural pattern used in Flask apps:

- [Application Factory](https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/)

## Application Factory

To date we have seen the application object created in `app.py` where are also defined the routes.

If we move the creation of the Flask object into a function, you we can then create multiple instances of this app later.

The advantages of this approach are:

- Testing. You can have instances of the application with different settings to test every case.
- Multiple instances. Imagine you want to run different versions of the same application. You can have multiple instances of the same application running in the same application process which can be handy.

For this course (COMP0034), the main purpose is to support testing. It is also a convenient way to configure and enable a number of the Flask extensions that we will be using in the project such as Flask-Login, Flask-SQLAlchemy and Flask-WTF.

To use this approach you will define a function called `create_app`. For this example we are going to create it in the `__init__.py` for `my_app`.

### Create a new function in `my_app/__init__.py`
We are going to create the function and inside the function create an instance of the Flask app and configure it using the config.py created in the previous activity.

We will the name of our config class to the method and the method will return a Flask app object.

Your Python code might look something like this:

```python
from flask import Flask


def create_app(config_classname):
    """
    Initialise the Flask application.
    :type config_classname: Specifies the configuration class
    :rtype: Returns a configured Flask object
    """
    app = Flask(__name__)
    app.config.from_object(config_classname)

    return app
```

We now need to call the function to create the app. For now we will do this in app.py with the following code:

```python

from my_app import create_app, config

app = create_app(config.Config)


@app.route('/')
def index():
    return 'This is the home page for my_app'


if __name__ == '__main__':
    app.route()

```

Run app.py and check that you can access [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

### Create global instance of the SQLAlchemy object and initialise for our Flask app
You may need to refer to the [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.SQLAlchemy) and [Flask contexts]((https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/)) documentation for this part of the activity.

The `SQLAlchemy` class is used to control the SQLAlchemy integration to one or more Flask applications.

We will first create the the object globally and then initialise it within the Flask app (i.e. in `create_app`).

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    # Existing code here

    # Initialise 
    db.init_app(app)

    return app
```

Stop and restart the app to check it still runs.

### Initialise Flask-Login and Flask-WTF CSRF protection
This is a pattern we will repeat for several other objects that we will use: Flask-Login and Flask-WTF (and you may come across others for your app).

Create and initialise the following by placing the code into the correct place in `my_apps\__init__.py`. The hyperlinks should direct you to the configuration information for the modules.

- [Flask Login](https://flask-login.readthedocs.io/en/latest/#configuring-your-application)
- [Flask-WTF CSRF Protection](https://flask-wtf.readthedocs.io/en/stable/csrf.html#setup)

Stop and restart the Flask app. You won't see any visual changes but the code should still run and allow you to access [http://127.0.0.1:5000/](http://127.0.0.1:5000/). 

### Initialise your Dash app
You can incorporate your dash app usinge the same approach i.e. by adding the following into the `create_app` function:

```python
    with app.app_context():
        # Import Dash application
        from dash_app.dash import init_dashboard
        app = init_dashboard(app)
```

First however we need to modify the way in which the Dash app is created. We need to wrap the Dash app creation and app.layout into an `init_dashboard` function, and wrap the callbacks into an ``init_callbacks` function.

```python
def init_dashboard(server):
    app = dash.Dash(__name__)
    app.layout = html.Div([
        # ... Layout stuff
    ])

    # Initialize callbacks after our app is loaded
    # Pass dash_app as a parameter
    init_callbacks(dash_app)

    return dash_app.server

def init_callbacks(dash_app):
    @app.callback(
    # Callback input/output
    ....
    )
    def update_graph(rows):
        # Callback logic
        ...
```

You can read more about this approach to using [Dash with Flask here](https://hackersandslackers.com/plotly-dash-with-flask/).

If you look at `dash_app/dash.py` you will see that the code has been amended for you.

Stop and restart the Flask app and then navigate to http://127.0.0.1:5000/dashapp/ and you should see the covid dashboard created in week 4.