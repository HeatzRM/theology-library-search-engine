import json
import os
import shutil
import threading
from threading import Thread
from datetime import datetime, timedelta
from base64 import b64encode
from uuid import uuid4
from config import Config
from operator import attrgetter
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, desc
from flask import render_template, flash, redirect, url_for, request, Flask
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.exceptions import HTTPException
from app import app, db
from app.forms import (
    LoginForm,
    RegistrationForm,
    EditProfileForm,
    SimpleSearchForm,
    AdvancedSearchForm,
    AddArticleForm,
)
from app.models import User, Article, PDFFile

from .resulthandler import (
    get_search_result,
    make_list_cluster_docs,
    get_specific_search,
)
from .textmining import TextMiner
from .texthandler import TextHandler

import boto3

# Create an instance of the engine and the session
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)
Session = sessionmaker(bind=engine)

# creates database on first run
@app.before_first_request
def create_database():
    db.create_all()
    db.session.commit()


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route("/")  # set root directory
@app.route("/index", methods=["GET", "POST"])  # set index directory
def index():
    login_form = LoginForm()
    since = datetime.now() - timedelta(hours=8766)  # 1 year
    articles = (
        Article.query.filter(Article.timestamp > since)
        .order_by(desc(Article.timestamp))
        .limit(8)
        .all()
    )
    return render_template("index.html", title="Home Page", articles=articles)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
# @login_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template("user.html", user=user)


@app.route("/article/<articleid>")
def article(articleid):
    article_converted_text = None
    article = Article.query.filter_by(id=articleid).first_or_404()
    return render_template(
        "article.html", article=article, article_converted_text=article_converted_text
    )


@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username, current_user.email)
    if request.method == "POST":
        if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.set_password(form.password.data)
            db.session.commit()
            flash("Your changes have been saved.")
            return redirect(url_for("edit_profile"))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("edit_profile.html", title="Edit Profile", form=form)


@app.route("/search", methods=["GET", "POST"])
def simple_search_engine():
    form = SimpleSearchForm()
    query = ""

    # checks if the form input text fields are empty
    if form.query.data != "" and form.query.data != None:
        query = form.query.data
    else:
        try:
            query = request.form["search"]
        except HTTPException as ex:
            print(ex)

    if request.method == "POST":
        out_articles = []
        documents_list = []
        out_cluster_terms = []
        try:
            out_articles = get_search_result(query)
        except TypeError as ex:
            print("An error occured!  " + str(ex))
        except LookupError as ex:
            print('Lookup error download nltk.....: '  + str(ex) )
            # import nltk
            # nltk.download("all")
        try:
            documents_list = make_list_cluster_docs()
        except NameError as ex:
            print("An error occured!  " + str(ex))
        try:
            out_cluster_terms = TextMiner().get_cluster_terms(query, documents_list)
        except ValueError as ex:
            print("An error occured!  " + str(ex))
        print("out_cluster_terms:" + " " + str(out_cluster_terms))
        print("query:" + " " + str(query))
        print("out_articles " + str(out_articles))
        out_articles = [i for i in out_articles if i is not None]
        return search_results(out_articles, out_cluster_terms, query)
    return render_template("search.html", title="Search", form=form)


@login_required
@app.route("/delete/<int:article_num>", methods=["GET"])
def delete(article_num):
    if request.method == "GET":
        # Delete Images on static
        article = Article.query.filter_by(id=article_num).first_or_404()
        try:
            shutil.rmtree(
                os.path.dirname(os.path.abspath(__file__))
                + "//static//images"
                + "//"
                + article.img_url
            )
        except Exception as e:
            print(e)
        # Delete Files on index.JSON
        indexfile = ""
        try:
            indexfile = TextHandler().OpenTextFrom(
                os.path.dirname(os.path.abspath(__file__)) + "//" + "static",
                "index.JSON",
            )
            indexfile = json.loads(indexfile)
        except Exception as ex:
            print(ex)
        try:
            indexfile.pop(str(article_num))
        except Exception as ex:
            print(ex)
        try:
            TextHandler().SaveFileTo(
                os.path.dirname(os.path.abspath(__file__)) + "//static",
                "index.JSON",
                json.dumps(indexfile),
            )
            # Delete The Article by ID in the Database
            db.session.delete(article)
            db.session.commit()
            flash("Article was successfully deleted")
        except Exception as ex:
            print(ex)
        return redirect(url_for("index"))


@app.route("/advanced-search", methods=["GET", "POST"])
def advanced_search_engine():
    form = AdvancedSearchForm()
    if request.method == "POST":
        # Creates a search with these parameters
        query = {
            "Title": form.article_title.data.lower(),
            "Subtitle": form.subtitle.data.lower(),
            "Author": form.author.data.lower(),
            "JournalTitle": form.journal_title.data.lower(),
            "PlaceOfPublisher": form.place_of_publisher.data.lower(),
            "NameOfPublisher": form.name_of_publisher.data.lower(),
            "ISSN": form.issn.data.lower(),
            "VolumeNumber": form.volume_number.data.lower(),
            "IssueNumber": form.issue_number.data,
            "YearOfPublication": form.year.data.lower(),
            "MonthOfPublication": form.month.data.lower(),
            "NoOfPages": form.no_of_pages.data.lower(),
            "Subject": form.subject.data.lower(),
            "ContainsTheseWords": form.contains_these_words.data.lower(),
        }
        new_query_list = {}
        for q in query:
            if query[q] != "":
                new_query_list[q] = query[q]
        # print(new_query_list)
        return search_results(
            get_specific_search(new_query_list), input_cluster_terms="", query=""
        )
    return render_template("advanced_search.html", title="Advanced Search", form=form)


@app.route("/results", methods=["GET", "POST"])
def search_results(input_articles, input_cluster_terms, query):
    form = SimpleSearchForm()
    return render_template(
        "results.html",
        title="Search Results",
        form=form,
        articles=input_articles,
        cluster_terms=input_cluster_terms,
        query=query,
    )


@app.route("/add_article", methods=["GET", "POST"])
@login_required
def add_article():
    form = AddArticleForm()
    if form.validate_on_submit():
        if request.method == "POST":

            session = boto3.Session(
                aws_access_key_id=app.config["AWS_ACCESS_KEY_ID"], 
                aws_secret_access_key=app.config["AWS_SECRET_ACCESS_KEY"], 
            )

            # try:
            #     for file in request.files.getlist("pdf"):
            #         s3_client = session.resource('s3')
            #         s3_client.Bucket(app.config["S3_BUCKET"]).put_object(Key=str(uuid4())+"_"+file.filename, Body=file, ACL='private')
            # except Exception as ex:
            #     print(ex)
            
            # try:
            #     for file in request.files.getlist("pages"):
            #         s3_client = session.resource('s3')
            #         s3_client.Bucket(app.config["S3_BUCKET"]).put_object(Key=str(uuid4())+"_"+file.filename, Body=file, ACL='private')
            # except Exception as ex:
            #     print(ex)
            
            try:
                for file in request.files.getlist("cover_img"):
                    s3_client = session.resource('s3')
                    s3_client.Bucket(app.config["S3_BUCKET"]).put_object(Key=str(uuid4())+"_"+file.filename, Body=file, ACL='public-read')
            except Exception as ex:
                print(ex)


            flash("ARTICLE IS NOW BEING CONVERTED")
            flash("YOU MAY ADD ANOTHER ARTICLE OR LEAVE THIS PAGE")

            return redirect(url_for("add_article"))

    # This will be executed on GET request.
    return render_template("add_article.html", Title="Add Article", form=form)


@app.route("/all_articles/<int:page_num>", methods=["GET", "POST"])
def all_articles(page_num):
    simple_search_form = SimpleSearchForm()
    articles = Article.query.paginate(per_page=10, page=page_num, error_out=True)
    return render_template(
        "all_articles.html",
        title="All Articles",
        articles=articles,
        simple_search_form=simple_search_form,
    )
