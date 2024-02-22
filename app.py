from flask import Flask,render_template,request,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(200),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self):
        return '<task %r' % self.id
@app.route('/',methods=["POST","GET"])
def index():
    if request.method=="POST":
        
        task = request.form['content']
        new_task = Todo(content= task)
       
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'An error occur during adding task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=tasks)
@app.route("/about")
def about():
    return 'This is about page'

@app.route("/delete/<int:id>")
def delete(id):
    task_del = Todo.query.get(id)
    try:
        db.session.delete(task_del)
        db.session.commit()
        return redirect("/")
    except:
        return 'An error occur during deleting task'

@app.route("/update_task/<int:id>")
def update_task(id):
    task_update = Todo.query.get(id)
    return render_template("update.html",data=task_update)

@app.route("/update",methods=["POST"])
def update():
    if request.method=="POST":
        task_update = request.form["content"]
        task_id = request.form["id"]
        
        try:
            row = Todo.query.get(task_id)
            row.content = task_update
            db.session.commit()
            return redirect("/")
        except:
            return 'an error occured during update operation'
if __name__=="__main__":
    app.run(debug=True)