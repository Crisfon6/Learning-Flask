from flask import Flask,render_template
app= Flask(__name__)#object

#http://localhost:8000/user/crist
@app.route('/user/<name>')
def index(name=""):
    age = 20
    my_list= [2,4,23,4]
    return   render_template("user.html",name=name,age=age,my_list=my_list)

if __name__ == "__main__":
    app.run(debug=True,
        port=8000)#This put run thex| server