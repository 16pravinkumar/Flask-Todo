from flask import Flask, render_template, request,redirect,flash

from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

# used for generating unique IDs
import uuid
from sqlalchemy.dialects.postgresql import UUID  # PostgreSQL-specific
from flask import jsonify

app =   Flask(__name__)

#? DB Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = '4f9d3bc842b68a53b947123ffa6c1d4a'

#? Init DB
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} {self.title}"
    
# Todo : To create a particular todo element
@app.route('/',methods=['GET','POST'])
def index():
    
    if(request.method == 'POST'):
        title = request.form.get('title')
        desc = request.form.get('desc')
    
        if title and desc:
            todo = Todo(title=title,desc=desc)
            db.session.add(todo)
            db.session.commit()
            flash('Data saved successfully!','success')
            return redirect('/') 
        else :
            return "Please enter both title and description"

    allTodo = Todo.query.all()
        
    # Start building the query
    query = Todo.query

    search_query = request.args.get('search', '').lower()
    if search_query:
        query = query.filter(
            (Todo.title.ilike(f"%{search_query}%")) |
            (Todo.desc.ilike(f"%{search_query}%")) |
            (Todo.created_date.ilike(f"%{search_query}%"))
        )

    # Apply sorting
    sort_by = request.args.get('sort_by')
    match sort_by:
        case 'by_title':
            query = query.order_by(Todo.title.asc())
        case 'by_desc':
            query = query.order_by(Todo.desc.asc())
        case 'by_date' | 'by_created_date':
            query = query.order_by(Todo.created_date.desc())
        case _:
            pass  

    allTodo = query.all()

    return render_template('index.html',allTodo=allTodo,update=False)

# Todo : To delete a particular todo element
@app.route('/delete/<string:sno>', methods=['DELETE'])
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
        flash('Data deleted successfully!','success')
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Todo not found'}), 404

# Todo : To update a particular todo element
@app.route('/update/<string:sno>', methods=['GET','POST'])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    allTodo = Todo.query.all()
    print("ALL",allTodo)

    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        flash('Data updated successfully!','success')
        return redirect('/')
    return render_template('index.html',todo=todo, allTodo=allTodo, update=True)

# Todo : To read a entire todo data
@app.route('/show')
def showData():
    allTodo = Todo.query.all()
    print(allTodo)
    return render_template('index.html',allTodo=allTodo, update=False)




# ? 
if __name__ == '__main__':
    app.run(debug=True)
    
    
    
    
    
    
    
    
 
    
    
    
    
    
    
    
    
    
    
    
  