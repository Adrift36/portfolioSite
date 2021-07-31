from os import name
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
db = SQLAlchemy(app)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return 'project ' + str(self.id)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/projects', methods=['GET', 'POST'])
def projects():
    if request.method == 'POST':
        project_title = request.form['title']
        project_content = request.form['content']
        project_date = request.form['date']
        new_project = Project(title=project_title, content=project_content, date=project_date)
        db.session.add(new_project)
        db.session.commit()
        return redirect('/projects')
    else:
        all_projects = Project.query.order_by(Project.date).all()
        return render_template('projects.html', projects=all_projects)

@app.route('/projects/delete/<int:id>')
def delete(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return redirect('/projects')

@app.route('/projects/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    project = Project.query.get_or_404(id)
    if request.method == 'POST':
        project.title = request.form['title']
        project.date = request.form['date']
        project.content = request.form['content']
        db.session.commit()
        return redirect('/projects')
    else:
        return render_template('edit.html', project=project)


@app.route('/home/<string:name>')
def hello(name):
    return f'Hello {name}'

if __name__ == '__main__':
    app.run(debug=True) 