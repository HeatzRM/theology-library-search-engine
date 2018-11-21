from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.models import User, Article

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        if email.data != self.email:
            email = User.query.filter_by(email=self.email.data).first()
            if email is not None:
                raise ValidationError('Please use a different email.')

class AddArticleForm(FlaskForm):
    title = StringField('Title*', validators=[DataRequired()])
    subtitle = StringField('Subtitle')
    abstract = TextAreaField('Abstract')
    author = StringField('Author')
    journal_title = StringField('Journal Title')
    place_of_publisher = StringField('Place of Publisher')
    name_of_publisher = StringField('Name of Publisher')
    issn = StringField('ISSN')
    volume_number = StringField('Volume Number')
    issue_number = StringField('Issue Number')
    year = StringField('Year')
    month = StringField('Month')
    no_of_pages = StringField('Number of Pages')
    subject = StringField('Subject')
    submit = SubmitField('Submit')  

class SimpleSearchForm(FlaskForm):
    query = StringField('Query', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AdvancedSearchForm(FlaskForm):
    article_title = StringField('Article Title:')
    subtitle = StringField('Subtitle:')
    author = StringField('Author:')
    journal_title = StringField('Journal Title:')
    place_of_publisher = StringField('Place of Publisher:')
    name_of_publisher = StringField('Name of Publisher:')
    issn = StringField('ISSN:')
    volume_number = StringField('Volume Number:')
    issue_number = StringField('Issue Number:')
    year = StringField('Year:')
    month = StringField('Month:')
    no_of_pages = StringField('No of Pages:')
    subject = StringField('Subject:')
    abstract = StringField('Abstract:')
    contains_these_words = StringField('Contain these words:')
        
    submit = SubmitField('Submit')

