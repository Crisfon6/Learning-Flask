from flask import Flask,request
app= Flask(__name__)#object

@app.route('/')#decorator
def index():#fucntion router
    return "HEllo World"

#http://localhost:8000/params?param1=231
#http://localhost:8000/params?param1=231&param2=hola
@app.route('/params')
def params():
    param = request.args.get("param1","param no found")
    param2  =request.args.get("param2","no found param2")
    return 'the params is {}, {}'.format(param, param2)
if __name__ == "__main__":
    app.run(debug=True,
        port=8000)#This put run thex| server