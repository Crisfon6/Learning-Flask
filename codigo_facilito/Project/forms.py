from wtforms import  Form, StringField, TextField,validators,HiddenField,PasswordField
from wtforms.fields.html5 import EmailField
from models import User


def length_honeypot(form,field):
    if len(field.data)>0:
        raise validators.ValidationError("The field must be empty")

class CommentForm(Form):
    
    
    comment = TextField('Comment')
    honeypot = HiddenField('',[
        length_honeypot
    ])

# class LoginForm(Form):
#     username=  StringField('username',
#     [validators.Length(min=4,max=25,message="Invalid Username"),
#     validators.Required("The username is required!")]),
#     # password = PasswordField('Password',[
#     #     validators.Required(message="password required")
#     # ])
class LoginForm(Form):
    username=  StringField('username',
    [validators.Length(min=4,max=25,message="Invalid Username"),
    validators.Required("The username is required!")])
    password = PasswordField('Password',
    [
        validators.Required(message="The password is required!"),
        
    ])


class CreateForm(Form):
    username = TextField('Username',[
        validators.Required(message="Username is required"),
        validators.length(min=4,max=50,message="Enter username valid")
    ])
    email = EmailField('Email',[
        validators.Required(message="Email is required"),
        validators.Email(message="Enter valid email"),
        validators.length(min=4,max=50,message="Enter email valid")
    ])
    password = PasswordField('Password',[
        validators.Required(message="Password is required"),
        validators.length(min=4,max=50,message="Enter password valid")
    ])

    def validate_username(form,field):
        username = field.data
        user = User.query.filter_by(username=username).first()
        if user is not None:
            raise validators.ValidationError('Username already exist')
