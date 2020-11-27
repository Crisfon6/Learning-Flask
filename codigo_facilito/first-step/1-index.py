from flask import Flask,request
app= Flask(__name__)#object

@app.route('/')
def index():
    return   "Hello World"
if __name__ == "__main__":
    app.run(debug=True,
        port=8000)#This put run thex| server