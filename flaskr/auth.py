from flask import (Blueprint, request, g, render_template, flash, redirect, url_for, session)
from rethinkdb import RethinkDB
r = RethinkDB()
from werkzeug.security import generate_password_hash, check_password_hash
import functools


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Route for registering an account. Checks if an account with
# the specified username exists, if not creates the new account
# and redirects to the login page.
@auth_bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = g.get_conn()
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            cursor_arr = r.db('todolist').table('users').filter(r.row["username"] == username).coerce_to('array').run(conn)
            if len(cursor_arr) > 0:
                error = 'Username already exists.'
        if error is None:
            try:
                new_user = {
                    'username': username,
                    'password': generate_password_hash(password)
                }
                insertion = r.db('todolist').table('users').insert(new_user).run(conn)
            except Exception as e:
                error = str(e)
            else:
                return redirect(url_for("auth.login"))
        flash(error)
    return render_template('auth/register.html')

# Login route. Queries the database using the username and password entered.
# Once the user is logged in their id (primary key for user table) is stored in
# the session and any further requests relating to the user are performed using that.
@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = g.get_conn()
        error = None
        cursor_arr = r.db('todolist').table('users').filter(r.row["username"] == username).coerce_to('array').run(conn)
        if len(cursor_arr) == 0:
            error = 'User does not exist.'
        else:
            user = cursor_arr[0]
            if not check_password_hash(user['password'], password):
                error = 'Incorrect password.'
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('todos_bp.index'))
        flash(error)
    return render_template('auth/login.html')

# Checks whether there is a user logged in and
# stored their id in the session if so.
@auth_bp.before_app_request
def load_logged_in_user():
    conn = g.get_conn()
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = r.db('todolist').table('users').get(user_id).run(conn)

# Clears the session.
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('todos_bp.index'))

# Ensures that a user is prompted to log in
# before accessing any todos page. 
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view