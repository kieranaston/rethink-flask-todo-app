# Flask and RethinkDB Todo List

A simple todo list with the following features:

* User account creation and login
* Listing a user's todos
* Adding todos
* Deleting todos
* Marking todos as complete/incomplete

## How I worked on this project

I worked on this project with the goal of familiarizing myself with Flask and RethinkDB, as well as getting some more experience with frontend work. I referenced various articles, documentation, and demo projects to get an idea of how I wanted to structure my web app and what features I wanted it to have. To establish my workflow I began by asking myself a number of important questions:
* How do I want to structure my project? I want it to be modular, but I also need to consider that my project is small and should be simple and easy to navigate
* How am I going to manage database connections? I need a robust method that can be easily used throughout the rest of my project
* How will I initialize the Flask application and connect it to the database?
* What sort of views and routes do I need?
* What logic should be performed in the frontend and what should be done in the backend?
* How can I use styling to make my project look nice?

### Choosing a file structure

One thing I found when looking at small todo list projects was that often modularity was not a big focus. This makes a lot of sense, since most of the time these projects are so small that it makes more sense to adopt a more basic file structure. After going over a number of demo Flask web apps it seemed to me that the most effective way to achieve some degree of modularity while maintaining a simple file structure was with Flask blueprints.

[This](https://realpython.com/flask-blueprint/)[^3] article outlines a completely modular setup with blueprints. When considering the scale of my project and the components I wanted to include I found it would be better to implement blueprints with a more simple file structure that could be made more modular if needed. I ended up adopting the project layout detailed [here](https://flask.palletsprojects.com/en/2.3.x/tutorial/layout/)[^4], leaving the files for database logic, logic related to the todos, and logic related to user authentication in the root project folder `todo-app/flaskr/`, and using separate folders for different pages within my `todo-app/flaskr/templates/` directory.

### Managing database connections

To manage database connections I followed [this](https://fjebaker.github.io/notes/python/flask/rethink-db-with-flask.html)[^2] instantiation of RethinkDB with Flask. It ensures that only one database connection is active at all times by checking for a connection at the beginning of a request and only establishing one if needed. It does this by assigning custom functions to Flask's `app.before_request()` and `app.teardown_appcontext()`.

With this a connection can be accessed anywhere in my project with `g.get_conn`.

One thing I added to the database management was a database initialization function, `init_db()`, that checks if the database and tables exist and creates them if not. The intialization function gets registered as a terminal command so that the database can be easily initialized before running the flask application with `flask --app flaskr init-db`.

### Initializing the app and connecting to the database

I made use of the application factory [here](https://flask.palletsprojects.com/en/2.3.x/tutorial/factory/)[^1] in `todo-app/flaskr/__init__.py`, which initializes the Flask app with a config if specified and registers blueprints for managing the database, user authentication, and interacting with todos.

### Views % Routes



[^1]: Baker, F. (2021). Using RethinkDB with Flask. notes. https://fjebaker.github.io/notes/python/flask/rethink-db-with-flask.html
[^2]: Baker, F. (2021). Using RethinkDB with Flask. notes. https://fjebaker.github.io/notes/python/flask/rethink-db-with-flask.html
[^3]: Garcia, M. (2021, February 6). Use a flask blueprint to architect your applications. Real Python. https://realpython.com/flask-blueprint/
[^4]: Project layout. Project Layout - Flask Documentation (2.3.x). (2010). https://flask.palletsprojects.com/en/2.3.x/tutorial/layout/
