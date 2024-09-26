from flask import current_app, g
from rethinkdb import RethinkDB
r = RethinkDB()
import click
import os

# Establishes a database connection.
def _connect_to_database():
    return r.connect(
        host = os.environ.get('RDB_HOST') or 'localhost',
        port = os.environ.get('RDB_PORT') or 28015
    )

# If no current connection, gets a connection and stores it
# in _db_conn.
def get_db_conn():
    if '_db_conn' not in g:
        g._db_conn = _connect_to_database()
    return g._db_conn

# Teardown function for the database connection.
def teardown_db(env):
    conn = g.pop('_db_conn', None)
    if conn is not None:
        current_app.logger.info("Disconnecting from database.")
        conn.close()

# Registers get_db_conn to db.get_conn for easy access to the connection.
def register_db_to_context():
    g.get_conn = get_db_conn

# Registers the teardown function, before_request function, and
# the command for initializing the db.
def init_app_database(app):
    app.teardown_appcontext(teardown_db)
    app.before_request(register_db_to_context)
    app.cli.add_command(init_db_command)

# Initializes the database with the required tables.
def init_db():
    conn = get_db_conn()
    db_name = "todolist"
    db_exists = r.db_list().contains(db_name).run(conn)
    if not db_exists:
        r.db_create(db_name).run(conn)
        r.db(db_name).table_create("todos").run(conn)
        r.db(db_name).table_create("users").run(conn)
        print("Database and tables initialized.")
    else:
        print("Database already exists.")
        todos_tb_exists = r.db(db_name).table_list().contains("todos").run(conn)
        users_tb_exists = r.db(db_name).table_list().contains("users").run(conn)
        if not todos_tb_exists:
            r.db(db_name).table_create("todos").run(conn)
            print("Todos table initialized.")
        if not users_tb_exists:
            r.db(db_name).table_create("users").run(conn)
            print("Users table initialized.")
    conn.close()

# Command for initializing the database.
@click.command('init-db')
def init_db_command():
    init_db()
