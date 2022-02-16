# imports
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# # Create Flask class instance
# def create_app():
app = Flask(__name__)
DATABASE_URI = "sqlite:///todos.db"
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# todo class model
class Todo(db.Model):
    __tablename__ ="Todos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"Todo: {self.title}"




@app.route('/',methods=['GET','POST'])
def todoMain():
    """
    The todos main view for listing all todos with GET method, or add new todo with POST method
    """
    todos = Todo.query.all()
    if request.method == 'GET':
        todoslist = []
        for todo in todos:
            dict={
                'id':todo.id,
                'title': todo.title,
                'content': todo.content
            }
            todoslist.append(dict)

        return jsonify({
            'todos': todoslist
        })

    elif request.method == 'POST':
        notetitle = request.json.get('title')
        notecontent = request.json.get('content')
        newnote = Todo(title=notetitle, content=notecontent)
        db.session.add(newnote)
        db.session.commit()
        return 'New Todo Note Has Been Added Successfully.'



@app.route('/todos/update/<int:id>',methods=['GET','PUT'])
def todoUpdate(id):
    """
    Get ceriten todo with it's id with GET method, and update that todo with PUT method
    """
    todonote = Todo.query.filter_by(id=id).first()
    if request.method == 'GET':
        todo={
                'id': todonote.id,
                'title': todonote.title,
                'content': todonote.content
            }

        return jsonify({
            'todos': todo
        })
    elif request.method == 'PUT':
        todonote.title = request.json.get('title')
        todonote.content = request.json.get('content')
        db.session.commit()
        return 'New Todo Note Has Been Updated Successfully.'



@app.route('/todos/delete/<int:id>',methods=['GET','DELETE'])
def todoDelete(id):
    """
    Get ceriten todo with it's id with GET method, and remove that todo with DELETE method
    """
    todonote = Todo.query.filter_by(id=id).first()
    if request.method == 'GET':
        todo={
                'id': todonote.id,
                'title': todonote.title,
                'content': todonote.content
            }

        return jsonify({
            'todos': todo
        })
    elif request.method == 'DELETE':
        db.session.delete(todonote)
        db.session.commit()
        return 'Todo Note Has Been Deleted Successfully.'


db.create_all()
app.run(debug=True)
