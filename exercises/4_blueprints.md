# Apply a Blueprint to a Flask app

In this activity we will cover another pattern used in Flask apps:

- [Blueprints](https://flask.palletsprojects.com/en/1.1.x/blueprints/)

## Blueprints
> "Flask uses a concept of blueprints for making application components and supporting common patterns within an application or across applications. Blueprints can greatly simplify how large applications work and provide a central means for Flask extensions to register operations on applications. A Blueprint object works similarly to a Flask application object, but it is not actually an application. Rather it is a blueprint of how to construct or extend an application."

The concept of Blueprints was discussed in activity <TBC - lecturer presentation> and summarised as:

A Flask blueprint is a way to organize a flask application into smaller and re-usable components

A blueprint defines a collection of views, templates and static assets.

If you write your blueprint in a separate Python package, then you have a component that encapsulates the elements related to a specific feature of the application.

Unlike a Flask application, a Blueprint cannot be run on its own, it can only be registered on an app.

For example, imagine you wanted to create your app, and also expose the data in the database as an API for others. Both components could re-use an authentication package. You could create a blueprint for each of these components (main app, API, authentication) within your app.

To use a Blueprint within our example application we will carry out the following:

1. Use the flask Blueprint class to create the blueprint
2. Import and register the blueprint in the application factory
3. Define routes to associate views with the Blueprint

### 1. Use the flask Blueprint class to create the blueprint
In practice you are likely to have several modules that together form your Flask app. We are going to create only one module in this example, called 'community' which we will use to provide the user community features for our web app. In a later week we will also add a module for authentication.

Create a new Python package called 'community' in your `my_app` directory. Your folder structure should contain the following (some file ommited for brevity):

```
/yourapplication
    /my_app
        __init__.py
        app.py
        /community
            __init__.py
        /static
        /templates
```

If you are likely to have several modules that each have different templates, you may also want to add sub-directories to the templates folder for each module e.g. `templates/community`. Another structure you may encounter is to define the [templates and static folders within each module](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure). You may need to consider one of these for coursework 2, however for this practice example we will keep all the templates in the same directory.

A simple way to define a blueprint might look like the following (see the [Blueprint API documentation](https://flask.palletsprojects.com/en/1.1.x/api/#flask.Blueprint) for all the parameters you can define:

```python
from flask import Blueprint

community_bp = Blueprint('community_bp', __name__, url_prefix='community')

```

This creates a blueprint called community_bp and defines one route (or view) called index within that Blueprint. 
`url_prefix` is optional. This provides a path to prepend to all of the blueprint’s URLs, to make them distinct from the rest of the app’s routes.

Where you place this code is up to you, however we will stick to a pattern whereby we place the routes for a module in an appropriately named python file within that module. 
In this example create it in `my_app/community/routes.py`. You do not have to call the file `community.py`, other appropriate names would be `views.py` or `routes.py`. You should should choose a naming convention for your project and then stick to it.

### 2. Import and register the blueprint in the application factory

We now return to the `my_app/__init__.py` file and the `create_app()` method.

After creating the Flask app we need to register the blueprint before we return the Flask app object e.g.:

```python
from my_app.community.community import community_bp
app.register_blueprint(community_bp)
```

### 3. Define a route to associate a view with the Blueprint
Define a route called `index` as the main route for this blueprint e.g.
```python
from flask import Blueprint

community_bp = Blueprint('community_bp', __name__, url_prefix='/community')

@community_bp.route('/')
def index():
    return "This is the community section of the web app"
```

You now have a route called index() in my_app and in the community module. This second index route is bound to the blueprint using the prefix `@community_bp` i.e. `@community_bp.route('/')`

Stop and restart the app and then navigate to: http://127.0.0.1:5000/community/

You should see a page displaying `This is the community section of the web app`.

## Repeat the steps to create a blueprint for the main site
Create a blueprint for the main site and move the current index route out of app.py and into this.
