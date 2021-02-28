from flask import Flask, render_template, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolist.id'), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id}: {self.description}, list: {self.list_id}, status: {self.completed}>'


class TodoList(db.Model):
    __tablename__ = 'todolist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    todos = db.relationship('Todo', backref='list', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<TodoList {self.id}: {self.name}>'


# create all tables
db.create_all()

# insert some data when starting
default_list = TodoList(name='default')
todo = Todo(description='complete sqlalchemy demo')
default_list.todos.append(todo)
db.session.add(default_list)
db.session.commit()


@app.route('/lists', methods=['POST'])
def create_list():
    body = request.get_json()
    name = body.get('name', '')
    if not name:
        abort(400)

    todolist = TodoList(name=name)
    try:
        db.session.add(todolist)
        db.session.commit()
    except:
        abort(500)
    return jsonify({'success': True, 'id': todolist.id})


@app.route('/lists/<int:list_id>', methods=['DELETE'])
def delete_list(list_id: int):
    if list_id == 1:
        abort(403)

    todolist = TodoList.query.get_or_404(list_id)

    try:
        db.session.delete(todolist)
        db.session.commit()
    except:
        abort(500)
    return jsonify({'success': True, 'id': list_id})


@app.route('/todos', methods=['POST'])
def create_todo():
    body = request.get_json()
    description = body.get('description', '')
    if not description:
        abort(400)

    list_id = body.get('list_id', 1)
    todolist = TodoList.query.get_or_404(list_id)
    todo = Todo(description=description)
    todolist.todos.append(todo)

    try:
        db.session.commit()
    except:
        abort(500)
    return jsonify({'success': True, 'todo_id': todo.id})


@app.route('/todos/<int:todo_id>', methods=['PUT'])
def change_todo_status(todo_id: int):
    todo = Todo.query.get_or_404(todo_id)
    todo.completed = not todo.completed

    try:
        db.session.commit()
    except:
        abort(500)
    return jsonify({'success': True, 'todo_id': todo_id})


@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id: int):
    todo = Todo.query.get_or_404(todo_id)

    try:
        db.session.delete(todo)
        db.session.commit()
    except:
        abort(500)
    return jsonify({'success': True, 'todo_id': todo_id})


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad Request'
    }), 400


@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        'success': False,
        'error': 403,
        'message': 'Forbidden'
    }), 403


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Not Found'
    }), 404


@app.errorhandler(500)
def server_error(error):
    db.session.rollback()
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal Server Error'
    }), 500


@app.route('/')
def index():
    lists = TodoList.query.all()
    todos = Todo.query.all()
    return render_template('index.html', lists=lists, todos=todos)


if __name__ == '__main__':
    app.run()
