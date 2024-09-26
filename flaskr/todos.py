import json
from flask import (g, jsonify, request, Blueprint, render_template, redirect, session)
from rethinkdb import RethinkDB
r = RethinkDB()
from .auth import login_required

todos_bp = Blueprint('todos_bp', __name__,
                     template_folder='templates',
                     static_folder='static', static_url_path='/')

# Gets all the todos for the current user from the database.
@todos_bp.route("/todos", methods=['GET'])
@login_required
def get_todos():
    conn = g.get_conn()
    user_id = session['user_id']
    selection = list(r.db('todolist').table('todos')
                     .filter(r.row['user_id'] == user_id)
                     .order_by('completed', r.desc('created_at'))
                     .run(conn))
    return json.dumps(selection)

# Adds a new todo for the current user to the database.
@todos_bp.route("/todos", methods=['POST'])
@login_required
def new_todo():
    conn = g.get_conn()
    user_id = session['user_id']
    new_todo = {'title': request.json.get('title'),
                'completed': False,
                'user_id': user_id}
    inserted = r.db('todolist').table('todos').insert(new_todo).run(conn)
    return jsonify(id=inserted['generated_keys'][0])

# Gets a specific todo based on id.
@todos_bp.route("/todos/<string:todo_id>", methods=['GET'])
@login_required
def get_todo(todo_id):
    conn = g.get_conn()
    user_id = session['user_id']
    todo = list(r.db('todolist').table('todos').filter((r.row['user_id'] == user_id) & (r.row['id'] == todo_id)).run(conn))
    return jsonify(todo[0])

# Patches a user's todo (used for toggling completed).
@todos_bp.route("/todos/<string:todo_id>", methods=['PATCH'])
@login_required
def patch_todo(todo_id):
    conn = g.get_conn()
    user_id = session['user_id']
    result = r.db('todolist').table('todos').filter((r.row['user_id'] == user_id) & (r.row['id'] == todo_id)).update(request.json).run(conn)
    return jsonify(result)

# Deletes a user's todo from the database.
@todos_bp.route("/todos/<string:todo_id>", methods=['DELETE'])
@login_required
def delete_todo(todo_id):
    conn = g.get_conn()
    user_id = session['user_id']
    #return jsonify(r.db('todolist').table('todos').get(todo_id).delete().run(conn))
    result = r.db('todolist').table('todos').filter((r.row['user_id'] == user_id) & (r.row['id'] == todo_id)).delete().run(conn)
    return jsonify(result)

# Renders the base template for the main page.
@todos_bp.route("/")
@login_required
def index():
    return render_template('base.html')