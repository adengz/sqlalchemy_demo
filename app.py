from flask import Flask, render_template
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


db.create_all()
default_list = TodoList(name='default')
todo = Todo(description='complete sqlalchemy demo')
default_list.todos.append(todo)
db.session.add(default_list)
db.session.commit()


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()