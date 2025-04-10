# Flask and RethinkDB Todo List

A simple todo list with the following features:

* User account creation and login
* Listing a user's todos
* Adding todos
* Deleting todos
* Marking todos as complete/incomplete

## Table of Contents
- [Flask and RethinkDB Todo List](#flask-and-rethinkdb-todo-list)
  - [Table of Contents](#table-of-contents)
  - [How to install/use](#how-to-installuse)
  - [How to navigate this project](#how-to-navigate-this-project)
  - [Things I would like to add in the future](#things-i-would-like-to-add-in-the-future)
  - [References](#references)

## How to install/use

First you can navigate to [this](https://rethinkdb.com/docs/install/) page to install RethinkDB to your system. Then, you can install the RethinkDB Python drivers globally or within your virtual environment using `sudo pip install rethinkdb`.

To make sure it is working, run the command `rethinkdb`. If you then go to: http://localhost:8080/ you should see the dashboard for RethinkDB.

To test the Python drivers run the following commands:
```
$ python
>>> from rethinkdb import RethinkDB
>>> r = RethinkDB()
>>> r.connect('localhost', 28015).repl()
```

What you get back should be similar to `<rethinkdb.net.DefaultConnection object at 0x100f6cc80>` if everything is working properly.

Install the packages from the requirements file: `pip install -r requirements.txt`

Navigate the the directory containing the project folder `flaskr`, and run the following command: `flask --app flaskr init-db`.

This should initialize your RethinkDB database.

Then, you should be good to run the app: `flask --app flaskr run` or `flask --app flaskr run --debug` if you are going to be making changes. You should see something similar to the following:

```
 * Serving Flask app 'flaskr'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

## How to navigate this project

Within `flaskr/` are the app factory `__init__.py`, the database management functions `db.py`, as well as the todo and user authentication logic `todos.py` and `auth.py`, respectively. `flaskr/static/` includes static files such as the styling `style.css` and supporting JavaScript `todo.js`. `flaskr/templates/` includes the HTML files with `layout.html` being a template for flashing error messages, `base.html` being the main page, and `flaskr/templates/auth` including the login and register pages.

THe file structure:

```
├── flaskr
│   ├── static
│   │   ├── style.css
│   │   └── todo.js
│   ├── templates
│   │   ├── auth
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── base.html
│   │   └── layout.html
│   ├── __init__.py
│   ├── auth.py
│   ├── db.py
│   └── todos.py
├── README.md
└── requirements.txt
```

## Things I would like to add in the future

In the future I would like to add unit testing to this project, as well as some more advanced features such as subtasks and reminders/forcing users to complete their tasks.

I would also like to add displayed timestamps for the todos to the page.

## References

1. [Application Setup - Flask Documentation (2.3.x)](https://flask.palletsprojects.com/en/2.3.x/tutorial/factory/)
2. [Using RethinkDB with Flask](https://fjebaker.github.io/notes/python/flask/rethink-db-with-flask.html)
3. [Blueprints and Views - Flask Documentation](https://flask.palletsprojects.com/en/2.3.x/tutorial/views/)
4. [Use a Flask Blueprint to Architect Your Applications](https://realpython.com/flask-blueprint/)
5. [RethinkDB Example Flask Backbone Todo](https://github.com/rethinkdb/rethinkdb-example-flask-backbone-todo)
6. [Project Layout - Flask Documentation](https://flask.palletsprojects.com/en/2.3.x/tutorial/layout/)