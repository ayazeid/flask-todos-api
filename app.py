# imports
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (JWTManager, create_access_token, jwt_required, get_jwt_identity,get_jwt)
from datetime import timedelta, datetime, timezone
import redis
# # Create Flask class instance
# def create_app():
app = Flask(__name__)
DATABASE_URI = "sqlite:///todos.db"
#DATABASE_URI = "postgresql://yoda:yoda@localhost:5432/flaskdb"
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

# user class model
class User(db.Model):
    __tablename__='Users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False,unique=True)
    password = db.Column(db.String, nullable=False)


ACCESS_EXPIRE = timedelta(hours=1)
app.config['JWT_SECRET_KEY'] = 'grogu12345'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = ACCESS_EXPIRE

jwt=JWTManager(app)

# jwt_redis_blocklist = redis.StrictRedis(
#     host="localhost", port=6379, db=0, decode_responses=True
# )
jwt_blocklist = set()

# Callback function to check if a JWT exists in the redis blocklist
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_token):
    return jwt_token['jti'] in jwt_blocklist
   



# register view
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return jsonify({
            'message':"Please Register with username and password to access"
        })
    elif request.method == 'POST':
        new_username = request.json.get('username')
        new_password = request.json.get('password')
        new_user = User(username=new_username,password=new_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            'message':"Register done successfully"
        })


# login view
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return jsonify({
            'Message':"Please login with username and password to access"
        })
    elif request.method == 'POST':
        loged_username = request.json.get('username')
        loged_password = request.json.get('password')
        loged_user = User.query.filter_by(username=loged_username).first()
        if loged_user.password == loged_password:
            access_token = create_access_token(identity=loged_username)
            return jsonify({
                
                'status':'success',
                'data':{
                    'access_token':access_token
                } })
        return jsonify({
                'status':'Fail',
                'message':'Wrong cridentials, Please check your username and password'
            })

# logout view
@app.route('/logout',methods=["POST"])
@jwt_required
def logout():
    jti = get_jwt()["jti"]
    jwt_blocklist.add(jti)
    return jsonify(msg="Access token revoked")



      
        

@app.route('/',methods=['GET','POST'])
@jwt_required()
def todoMain():
    """
    The todos main view for listing all todos with GET method, or add new todo with POST method
    """
    username =get_jwt_identity()
    # if User.query.filter_by(username=username).first().is_loged:
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
@jwt_required()
def todoUpdate(id):
    """
    Get ceriten todo with it's id with GET method, and update that todo with PUT method
    """
    username =get_jwt_identity()
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
@jwt_required()
def todoDelete(id):
    """
    Get ceriten todo with it's id with GET method, and remove that todo with DELETE method
    """
    username =get_jwt_identity()
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
