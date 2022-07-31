from crypt import methods
from email.policy import default
from flask import Flask, redirect, render_template, request, url_for , request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PrimaryKeyConstraint
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(200),nullable=False) #Word
    definition = db.Column(db.String(200),nullable=False) #Def
    examples = db.Column(db.String(200),nullable=False) #Ex
    need_rev = db.Column(db.Integer,default = 0) #Need review or not
    date_created = db.Column(db.DateTime,default=datetime.utcnow)

    def __rep__(self):
        return f'Word {self.id}'


@app.route('/', methods=['POST','GET'])
def index():
    if request.method=='POST':
        word = request.form['word']
        definition = request.form['definition']
        examples = request.form['examples']
        new_task = Todo(word=word,definition=definition,examples=examples)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue adding the word"
    else:
        tasks = Todo.query.filter_by(need_rev=0).all()

        return render_template('index.html',tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting that task"
@app.route('/rev/<int:id>')
def learnt(id):
    learnt_word = Todo.query.get_or_404(id)
    try:
        learnt_word.need_rev = 0
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem adding the word to the learnt group"


@app.route('/forget/<int:id>')
def forget(id):
    forger_word = Todo.query.get_or_404(id)
    try:
        forger_word.need_rev = 1
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem removing the word to the learnt group"


@app.route('/known/<int:id>')
def known(id):
    known_word = Todo.query.get_or_404(id)
    try:
        known_word.need_rev = 2
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem removing the word to the learnt group"
@app.route('/p_known/')
def update():
        tasks = Todo.query.filter_by(need_rev=2).all()
        return render_template('index.html',tasks=tasks)
@app.route('/p_rev/')
def rev():
    return redirect("/")
@app.route('/p_unknown/')
def unkn():
        tasks = Todo.query.filter_by(need_rev=1).all()
        return render_template('index.html',tasks=tasks)
if __name__ == '__main__':
    app.run()
