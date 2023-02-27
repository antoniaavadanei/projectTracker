from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/project_tracker'
app.config['SECRET_KEY']='q\xae\x89X\x92\xc2\xd9\xc5\xad\xf4\xfd\x06v\xce=\xfcH\xc8 \x8b\x97Vk\xab'

db = SQLAlchemy(app)

class Project(db.Model):
    __tablename__ = 'projects'

    project_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=50))

class Task(db.Model):
    __tablename__ = 'tasks'

    task_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'))
    description = db.Column(db.String(length=50))

    project = db.relationship("Project")

@app.route("/")
def show_projects():
    return render_template("index.html", projects=Project.query.all())

@app.route("/project/<project_id>")
def show_tasks(project_id):
    return render_template("project_tasks.html", project=Project.query.filter_by(project_id=project_id).first(),
                           tasks=Task.query.filter_by(project_id=project_id).all())

@app.route("/add/project", methods=['POST'])
def add_project():
    # add project
    if not request.form['project-title']:
        flash("Enter a title for your new project", "red")
    else:
        project = Project(title=request.form['project-title'])
        db.session.add(project)
        db.session.commit()
        flash("Project added successfully", "green")
    return redirect(url_for('show_projects'))

@app.route("/add/task/<project_id>", methods=['POST'])
def add_task(project_id):
    # add project
    if not request.form['task-description']:
        flash("Enter the description for the new task", "red")
    else:
        task = Task(description=request.form['task-description'],project_id=project_id)
        db.session.add(task)
        db.session.commit()
        flash("Task added successfully", "green")
    return redirect(url_for('show_tasks',project_id=project_id))


app.run(debug=True, host="127.0.0.1", port=3000)
