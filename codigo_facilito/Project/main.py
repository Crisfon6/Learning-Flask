from flask import Flask, render_template, request, make_response, session, redirect, url_for, flash,g
from flask import copy_current_request_context
from flask_wtf.csrf import CSRFProtect
import forms
import json
from config import DevelopmentConfig

from models import db,User,Comment
from helper import date_format
from flask_mail import Mail,Message
import threading

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()
mail = Mail()

def send_email(user_email,user_name):
    msg = Message("Thanks for your register!",
    sender=app.config['MAIL_USERNAME'],
    recipients=[user_email])

    msg.html= render_template('email.html',user=user_name)
    mail.send(msg)


@app.before_request#execute before the petitions
def before_request():
    g.test = "Hola"
    if 'username' not in session and request.endpoint in ['comment']:
        return redirect(url_for('login'))
    elif 'username' in session and request.endpoint in ['login','create']:
        return redirect(url_for('index'))
@app.after_request
def after_request(response):
    print("After")
    #print(g.test) 
    return response

@app.errorhandler(404)
def page_no_found(eror):
    return render_template('404.html'), 404


@app.route('/', methods=['GET', 'POST'])
def index():
    # custom_cookie = request.cookies.get("custom_cookie",'undefined')
    # print(custom_cookie)
    if 'username' in session:
        username = session['username']
        print(username)
   
    title = "Flask Course"
    return render_template('index.html', title=title)

@app.route('/comment', methods=['GET','POST'])
def comment():
    comment_form = forms.CommentForm(request.form)   
    
    if request.method == "POST" and comment_form.validate():
        user_id = session['user_id']
        comment = Comment(user_id=user_id,text=comment_form.comment.data)
        print(comment.user_id)
        print(comment.text)
        db.session.add(comment)
        db.session.commit()

        success_message= "Created comment"
        flash(success_message)
    else:
        error_message= "Error Creating comment"
        flash(error_message)
    title="Comments"
    return render_template('comment.html', title=title, form=comment_form)
    
@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = forms.LoginForm(request.form)
    if request.method == "POST" and login_form.validate():
        # session['username'] = login_form.username.data
        username = login_form.username.data
        password = login_form.password.data

        user = User.query.filter_by( username = username).first()
        if user is not None and user.verify_password(password):
            success_message = "Welcome {}".format(username)
            flash(success_message)
            session['username'] =username
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:   
            error_message = "User or password no valid"
            flash(error_message)
            


    else:
        print("Error in the form")
    title = "Login"

    return render_template('login.html', form=login_form, title=title)

@app.route('/create',methods=['POST','GET'])
def create():
    create_form = forms.CreateForm(request.form)
    if request.method == "POST" and create_form.validate():
        user = User(create_form.username.data,
        create_form.password.data,
        create_form.email.data)
        db.session.add(user)
        db.session.commit()
        @copy_current_request_context
        def send_message(email,username):
            send_email(user_email=email,user_name=username)


        sender = threading.Thread(name="mail_sender",target= send_message,args=(user.email,user.username))
        sender.start()
        success_message = "Save successful"
        flash(success_message)
    else:
        print("error saving")

    return render_template('create.html',form=create_form)

# work with cookie
@app.route('/cookie')
def cookie():
    response = make_response(render_template('cookie.html'))
    response.set_cookie("custom_cookie", "Cris")
    return response


@app.route('/ajax-login', methods=['POST'])
def ajax_login():
    print(request.form)
    username = request.form['username']
    response = json.dumps({'status': 200, 'username': username, 'id': 1})
    return response
@app.route('/reviews/',methods=['GET'])
@app.route('/reviews/<int:page>',methods=['GET'])
def reviews(page=1):
    per_page =3 
    comment_list = Comment.query.join(User).add_columns( User.username,Comment.text,
                                                        Comment.create_date).paginate(page,per_page,False)
    
    return render_template('reviews.html',comments= comment_list,title="Comments",date_format=date_format)

if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(port=8000)
