#how validate routes

from flask import Flask,request
app= Flask(__name__)#object

@app.route('/')#decorator
def index():#fucntion router
    return "HEllo World"

#http://localhost:8000/params/carlos/guzman
#http://localhost:8000/params/carlos/guzman
@app.route('/params/')
@app.route('/params/<name>/')
@app.route('/params/<name>/<last_name>')
@app.route('/params/<name>/<last_name>/<int:age>')
def params(name="",last_name="",age=0):

   return "the params is  {}, {}, have {} age".format(name,last_name,age)
if __name__ == "__main__":
    app.run(debug=True,
        port=8000)#This put run thex| server