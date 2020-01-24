from wtforms import StringField, SubmitField, IntegerField, PasswordField, BooleanField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class LoginForm(FlaskForm):
    user_name = StringField('User name: ',
        validators=[DataRequired(message=None), Length(min=3, max=30)
        ]
    )
    password = PasswordField('Password: ',
        validators=[DataRequired(message=None), Length(min=5, max=30)
        ]    
    )
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign in')

class RegisterForm(FlaskForm):
    user_name = StringField('User name: ',
        validators=[DataRequired(message=None), Length(min=2, max=30)
        ]    
    )
    first_name = StringField('First name: ',
        validators=[DataRequired(message=None), Length(min=2, max=30)
        ]    
    )
    last_name = StringField('Last name: ',
        validators=[DataRequired(message=None), Length(min=2, max=30)
        ]    
    )
    password = PasswordField('Password: ',
        validators=[DataRequired(message=None), Length(min=5, max=30)
        ]    
    )
    confirm_password = PasswordField('Please confirm your password: ',
        validators=[DataRequired(message=None), Length(min=5, max=30), EqualTo('password')
        ]    
    )
    submit = SubmitField('Register')

class NewFolder(FlaskForm):
    name = StringField('Title: ',
        validators=[DataRequired(message=None), Length(min=2, max=30)
        ]    
    )

class NewPost(FlaskForm):
    title = StringField('Title: ',
        validators=[DataRequired(message=None), Length(min=2, max=30)
        ]    
    )
    content = StringField('Content: ',
        validators=[DataRequired(message=None), Length(min=2, max=250)
        ]    
    )
    image = FileField('Image', 
        validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images Only')
        ]
    )
    submit = SubmitField('Submit')