# Configure the Flask app
You may need to refer to the [Flask Configuration documentation](https://flask.palletsprojects.com/en/1.1.x/config/) during this activity.

## Why do you need to care about configuration?
To date we haven't needed to configure the Flask object, however as you start to develop your app you will need to configure the app to work support different functionality, some of which require Flask config parameters.

You will also start to consider working with Flask in different environments. In COMP0035 we considered 3 environments that code may be used in:

- Development environment (dev): where the developer creates the code e.g. your machine
- Testing environment (test): where the testing takes place, this usually mimics the production environment but is likely to have test data and will be configured to provide detailed logging and error reporting. For your coursework this maybe a continuous testing environment that you have configured on GitHub using GitHub Actions.
- Production environment (prod): where the code is deployed and used in the wild. For this coursework you are asked not to deploy the application for ethical reasons (you would need to gain UCL Ethics approval first). If there were no ethics consideration then you could deploy to a free tier of services such as Heroku or AWS.

Complex apps or large organisations may have other environments, however for the purposes of this course the dev, test and prod will be sufficient.

How you configure each environment will vary from a number of perspectives e.g. consider how the database might be different. You may use a SQLite database for development as you have greater control, then you may have a locally hosted Oracle database for testing, and then for production a database that is perhaps split across multiple data centres globally. The location and access details for each of these will be different so you will need to configure Flask differently.

## Where the Flask config values are loaded
Flask provides a `config` attribute for the Flask object that you can use to create a config object to  which holds the loaded configuration values. 
This is the place where Flask itself puts certain configuration values and also where extensions can put their configuration values. 
But this is also where you can have your own configuration.

## Methods for providing config values
The config attribute is a subclass of a dictionary and can be modified just like any dictionary:
```python
from flask import Flask

app = Flask(__name__)
app.config['TESTING'] = True

# Or provide multiple config parameters using this format
app.config.update(
    TESTING=True,
    SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/'
)
```
This method becomes unwieldy however when you want to provide different config values for different environments. 
There are two methods that can be used, either to use a config class (`from_object`) or from environment variables (`from envvar`).
```python
from flask import Flask

app = Flask(__name__)
app.config.from_object('yourapplication.default_settings')
app.config.from_envvar('YOURAPPLICATION_SETTINGS')
```
As you should now be familiar with Python classes then for this course we will focus on creating a config class.

If you intend to create and deploy your own Flask apps after this course however you should investigate the use of enviornment variables. 

We will still use some environment variables within our config class where not doing so would lead to us putting secret information into a file that will be visible to others on GitHub (i.e. a security risk).

## Create a config class
Create a python file called config.py and create classes within it that reflect the following class diagram:
![Config class diagram](config_class_diag.png)

Your code might look something like this (this is from the Flask documentation):

```python
"""Flask config class."""

class Config(object):
    pass

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    pass

class TestingConfig(Config):
    pass

```

## Adding the config variables

This section covers from of the variables that you will need to set for your coursework. There may be others that you need to add later depending on your application.

Try to add the following to your `config.py`, using appropriate values for each environment.

1. `ENV` What environment the app is running in. 

Flask and extensions may enable behaviors based on the environment, such as enabling debug mode. 

The [Flask documentation](https://flask.palletsprojects.com/en/1.1.x/config/#environment-and-debug-features) recommends that you set this in environment variables rather than in Flask config as it may not behave as expected. For this exercise however we will place it in config.

Do not enable development when deploying in production.

Options: development, testing, production

2. `DEBUG` Whether debug mode is enabled. 

When using flask run to start the development server, an interactive debugger will be shown for unhandled exceptions, and the server will be reloaded when code changes. 

This is enabled when ENV is 'development' and is overridden by the FLASK_DEBUG environment variable.

When set to True, exceptions thrown by the app will print to console automatically and app crashes will result in a helpful error screen.

Do not enable debug mode when deploying in production.

Default: True if ENV is 'development', or False otherwise.

3. `TESTING` Enable testing mode. 

Exceptions are propagated rather than handled by the the app’s error handlers. Extensions may also change their behavior to facilitate easier testing. You should enable this in your own tests.

4. `SECRET_KEY`
A secret key that will be used for securely signing the session cookie and can be used for any other security related needs by extensions or your application. It should be a long random string of bytes, although unicode is accepted too. For example, copy the output of this to your config:

You can generate a random key in several ways. Try one of the following to generate a 16 digit key and copy the resulting text into your `config.py`. You can change the length to any number you wish.

```python
# For python 3.6 and later
import secrets

print(secrets.token_urlsafe(16))
```

```python
import os

print(os.urandom(16))
```

**Do not reveal the secret key when posting questions or committing code to GitHub!**

5. `SQLALCHEMY_DATABASE_URI`,  `SQLALCHEMY_TRACK_MODIFICATIONS` 

These are [additional configurationn keys used by the Flask-SQLAlchemy package](https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/#configuration-keys) which we will use to work with a SQL database.

`SQLALCHEMY_TRACK_MODIFICATIONS = False` needs to be set to avoid warnings. If you want to undersrtand why [read this stack overflow post](https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications/33790196#33790196).

`SQLALCHEMY_DATABASE_URI` defines the URI that should be used for the connection (i.e. the path to connect to the database). 

You are likely to have different databases for different environments. For example, if using an SQL database you might use: 

- a local SQLite database for development
- an in memory database for testing (ie one that is created in memory for the tests but not saved to disk)
- a MySQL (or other database server) for production

Example of syntax for these three scenarios:

```python
# A SQLite database in the 'data' directory of the project
import pathlib

DATA_PATH = pathlib.Path(__file__).parent.joinpath("data")
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATA_PATH.join('mydatabase.sqlite')

# An in memory SQLite database
SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# A MySQL database on a server
SQLALCHEMY_DATABASE_URI = 'mysql://username:password@server/db'
```

You may also want to set `SQLALCHEMY_ECHO` for dev and test as this prints database-related actions to console for debugging purposes.

For this activity set the database to the same for all environments and set it to `data/example.sqlite`.