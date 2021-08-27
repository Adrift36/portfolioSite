from os import name
from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import requests

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Asettergh23@localhost/Projects'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Project(db.Model):
    __tablename__ = 'Projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.Text, nullable=False)

    def __init__(self, title, content, date):
        self.title = title
        self.content = content
        self.date = date


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


@app.route('/contact')
def contact():
    if request.method == 'POST':
        ##contact.title = request.form['title']
        ##contact.date = request.form['date']
        ##project.content = request.form['content']
        ##db.session.commit()
        return redirect('/contact')
    else:
        return render_template('contact.html')


@app.route('/c4/<string:gameSequence>')
def bestmove(gameSequence): #temporary solution while I figure out minimax algorithms

    #headers to make the request look genuine
	headers = {
		'authority': 'connect4.gamesolver.org',
		'sec-ch-ua': '^\\^',
		'accept': 'application/json, text/javascript, */*; q=0.01',
		'x-requested-with': 'XMLHttpRequest',
		'sec-ch-ua-mobile': '?0',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
		'sec-fetch-site': 'same-origin',
		'sec-fetch-mode': 'cors',
		'sec-fetch-dest': 'empty',
		'referer': f'https://connect4.gamesolver.org/?pos={gameSequence[:-1]}',
		'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
	#	'cookie': '',
	}

    #game state parameter
	params = (
		('pos', gameSequence),
	)

    #make the request
	response = requests.get('https://connect4.gamesolver.org/solve', headers=headers, params=params)

    #intepret the response to decide the best move for the robot
	ratings = [-100 if x==100 else x for x in response.json()['score']]
	max_value = max(ratings)
	max_index = ratings.index(max_value)

	return jsonify({'index': max_index})


if __name__ == '__main__':
    app.run()