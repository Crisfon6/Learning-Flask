from flask import Flask,render_template
app= Flask(__name__)#object

@app.route('/')
def index():
    return   render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True,
        port=8000)#This put run thex| server