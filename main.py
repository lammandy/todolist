from flask_bootstrap import Bootstrap
from flask import Flask, render_template, redirect, flash, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Optional
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todolist.db"
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)


class TodoList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(50))

class DoingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(50))

class DoneList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(50))

# @app.before_first_request
# def create_tables():
#     db.create_all()

class TodoForm(FlaskForm):
    todo = StringField('', validators=[Optional()])
    submit = SubmitField('')

class DoingForm(FlaskForm):
    todo = StringField('', validators=[Optional()])
    submit = SubmitField('')

class DoneForm(FlaskForm):
    todo = StringField('', validators=[Optional()])

items = []

@app.route('/', methods=['GET', 'POST'])
def main():
    todo_form = TodoForm()
    todo_tasks = TodoList.query.all()
    if todo_form.is_submitted():
        todo_task = TodoList(
            todo=todo_form.todo.data)
        db.session.add(todo_task)
        db.session.commit()
        return redirect(url_for('main'))


    return render_template('index.html', form=todo_form, items=items, tasks=todo_tasks)

@app.route('/delete/<int:id>', methods=["GET", "POST"]) # the href in the index.html
def task_delete(id):
    task = db.get_or_404(TodoList, id)

    if request.method == "POST":
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('main'))


if __name__ == '__main__':
    app.run(debug=True)