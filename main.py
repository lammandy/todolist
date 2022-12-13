#todo when i remove the submission part of todo, doing works.
# https://stackoverflow.com/questions/18290142/multiple-forms-in-a-single-page-using-flask-and-wtforms
# delete for the other two columns, arrow
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
    todo1 = StringField('', validators=[Optional()])
    submit1 = SubmitField('')

class DoingForm(FlaskForm):
    todo2 = StringField('', validators=[Optional()])
    submit2 = SubmitField('')

class DoneForm(FlaskForm):
    todo3 = StringField('', validators=[Optional()])
    submit3 = SubmitField('')

@app.route('/', methods=['GET', 'POST'])
def main():
    todo_form = TodoForm()
    todo_tasks = TodoList.query.all()


    doing_form = DoingForm()
    doing_tasks = DoingList.query.all()

    done_form = DoneForm()
    done_tasks = DoneList.query.all()
    if todo_form.todo1.data and todo_form.is_submitted():
        todo_task = TodoList(
            todo=todo_form.todo1.data)
        db.session.add(todo_task)
        db.session.commit()
        return redirect(url_for('main'))

    if doing_form.todo2.data and doing_form.is_submitted():
        doing_task = DoingList(
            todo=doing_form.todo2.data)
        db.session.add(doing_task)
        db.session.commit()
        return redirect(url_for('main'))

    if done_form.todo3.data and done_form.is_submitted():
        done_task = DoneList(
            todo=done_form.todo3.data)
        db.session.add(done_task)
        db.session.commit()
        return redirect(url_for('main'))
    return render_template(
        'index.html',
        todo_form=todo_form, todo_tasks=todo_tasks,
        doing_form=doing_form, doing_tasks=doing_tasks,
        done_form=done_form, done_tasks=done_tasks)

@app.route('/todo_doing/<int:id>', methods=["GET", "POST"])
def todo_doing(id):
    task = db.get_or_404(TodoList, id)
    db.session.delete(task)
    db.session.commit()
    print(task.todo)
    doing_task = DoingList(
        todo=task.todo)
    db.session.add(doing_task)
    db.session.commit()
    return redirect(url_for('main'))

@app.route('/doing_done/<int:id>', methods=["GET", "POST"])
def doing_done(id):
    task = db.get_or_404(DoingList, id)
    db.session.delete(task)
    db.session.commit()
    print(task.todo)
    done_task = DoneList(
        todo=task.todo)
    db.session.add(done_task)
    db.session.commit()
    return redirect(url_for('main'))


@app.route('/done_doing/<int:id>', methods=["GET", "POST"])
def done_doing(id):
    task = db.get_or_404(DoneList, id)
    db.session.delete(task)
    db.session.commit()
    print(task.todo)
    doing_task = DoingList(
        todo=task.todo)
    db.session.add(doing_task)
    db.session.commit()
    return redirect(url_for('main'))

@app.route('/doing_todo/<int:id>', methods=["GET", "POST"])
def doing_todo(id):
    task = db.get_or_404(DoingList, id)
    db.session.delete(task)
    db.session.commit()
    print(task.todo)
    doing_task = TodoList(
        todo=task.todo)
    db.session.add(doing_task)
    db.session.commit()
    return redirect(url_for('main'))
@app.route('/todo_delete/<int:id>', methods=["GET", "POST"])
def todo_delete(id):
    task = db.get_or_404(TodoList, id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('main'))

@app.route('/doing_delete/<int:id>', methods=["GET", "POST"])
def doing_delete(id):
    task = db.get_or_404(DoingList, id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('main'))

@app.route('/done_delete/<int:id>', methods=["GET", "POST"])
def done_delete(id):
    task = db.get_or_404(DoneList, id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(debug=True)