from datetime import datetime
from time import time
from app import db, login, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
    	  #tells Python how to print objects of this class
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    subtitle = db.Column(db.String(255))
    abstract = db.Column(db.Text())
    author = db.Column(db.String(255))
    journal_title = db.Column(db.String(255))
    place_of_publisher = db.Column(db.String(255))
    name_of_publisher = db.Column(db.String(255))
    issn = db.Column(db.String(255))
    volume_number = db.Column(db.String(255))
    issue_number = db.Column(db.String(255))
    year = db.Column(db.String(255))
    month = db.Column(db.String(255))
    no_of_pages = db.Column(db.String(255))
    subject = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    img_url = db.Column(db.String(255))
    pages = db.relationship('Page', backref='journal')
    pdfs = db.relationship('PDFFile', backref='journal')
    cover = db.relationship('Cover', backref='journal')


    def __init__(self, title, subtitle, abstract, author, journal_title, place_of_publisher,\
    name_of_publisher, issn, volume_number, issue_number, year,\
    month, no_of_pages, subject, img_url):
        self.title = title
        self.subtitle = subtitle
        self.abstract = abstract
        self.author = author
        self.journal_title = journal_title
        self.place_of_publisher = place_of_publisher
        self.name_of_publisher = name_of_publisher
        self.volume_number = volume_number
        self.issue_number = issue_number
        self.issn = issn
        self.year = year
        self.month = month
        self.no_of_pages = no_of_pages
        self.subject = subject
        self.img_url = img_url

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text())
    converted_text = db.Column(db.Text())
    page_url = db.Column(db.String(255))
    page_name = db.Column(db.String(255))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))

class PDFFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text())
    converted_text = db.Column(db.Text())
    pdf_url = db.Column(db.String(255))
    pdf_name = db.Column(db.String(255))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))

class Cover(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cover_url = db.Column(db.String(255))
    cover_name = db.Column(db.String(255))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))    

    
