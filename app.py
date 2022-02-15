# imports
from flask import Flask, jsonify, request

# Create Flask class instance
app = Flask(__name__)

# todo list inital data
todos=[{'title':'Todo Note Title','content':'Todo Note Content'}]

# app routing views
@app.route('/',methods=['GET','POST'])
def todoMain():
    """
    The todos main view for listing all todos with GET method, or add new todo with POST method
    """
    if request.method == 'GET':
        return jsonify({
            'todos': todos
        })
    elif request.method == 'POST':
        notetitle = request.json.get('title')
        notecontent = request.json.get('content')

        newnote = {
            'title': notetitle,
            'content': notecontent
        }

        todos.append(newnote)
        return 'New Todo Note Has Been Added Successfully.'


    
    
@app.route('/todos/update/<int:id>',methods=['GET','PUT'])
def todoUpdate(id):
    """
    Get ceriten todo with it's id with GET method, and update that todo with PUT method
    """
    id-=1
    if request.method == 'GET':
        return jsonify({
            'todos': todos[id]
        })
    elif request.method == 'PUT':
        notetitle = request.json.get('title')
        notecontent = request.json.get('content')

        updatenote = {
            'title': notetitle,
            'content': notecontent
        }
        todos[id]= updatenote
        return 'New Todo Note Has Been Updated Successfully.'


@app.route('/todos/delete/<int:id>',methods=['GET','DELETE'])
def todoDelete(id):
    """
    Get ceriten todo with it's id with GET method, and remove that todo with DELETE method
    """
    id-=1
    if request.method == 'GET':
        return jsonify({
            'todos': todos[id]
        })
    elif request.method == 'DELETE':
        todos.pop(id)
        return 'Todo Note Has Been Deleted Successfully.'




app.run(debug=True)
