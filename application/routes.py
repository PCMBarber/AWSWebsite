from flask import render_template, redirect, url_for, Response, request
from flask_login import login_user, current_user, logout_user
from application import app, password_hash as pw
from application.forms import LoginForm, RegisterForm, NewFolder, NewPost
import requests, json, sys

@app.route('/')
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        payload={'body':{"username":form.user_name.data}}
        userjson = requests.get('https://krqrgv5s6b.execute-api.eu-west-2.amazonaws.com/Forum/forumuser', json=payload)
	oof = userjson.json()
	user = oof['body']

        if user and pw.verify_password(user['password'], form.password.data):
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('dashboard'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed = pw.hash_password(form.password.data)
        user = {"body":{
            "username":form.user_name.data,
            "firstname":form.first_name.data,
            "lastname":form.last_name.data,
            "password":hashed
        }}
        response = requests.put('https://krqrgv5s6b.execute-api.eu-west-2.amazonaws.com/Forum/forumuser', json=user)
        return redirect(url_for('login'))
    else:
        print(RegisterForm.errors)
        return render_template('register.html', title='Register', form=form)

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    forums = []
    response = requests.get('https://krqrgv5s6b.execute-api.eu-west-2.amazonaws.com/Forum/forum-forums')
    forumlist = response.json()['body']
    for entry in forumlist:
        forumName = entry
        if forumName in forums:
            continue
        else:
            forums.append(forumName)
    return render_template('dashboard.html', title='Dashboard', forums=forums)

@app.route('/forum/<forum>', methods=['GET','POST'])
def forum(forum):
    threads = []
    payload={"forum":forum}
    response = requests.get('https://krqrgv5s6b.execute-api.eu-west-2.amazonaws.com/Forum/forums-threads', json=payload)
    threadlist=response.json()['body']
    for entry in threadlist:
        threadName = entry["thread"]
        if threadName in threads:
            continue
        else:
            threads.append(threadName)
    return render_template('forum.html', title=forum, threads=threads)

@app.route('/thread/<forum>/<thread>', methods=['GET','POST'])
def thread(forum, thread):
    payload={"forum":forum, "thread":thread}
    query = requests.get('https://krqrgv5s6b.execute-api.eu-west-2.amazonaws.com/Forum/forumpost', json=payload)
    postlist=query.json()['body']
    return render_template('thread.html', title=thread, posts=postlist, forum=forum, thread=thread)

@app.route('/new_forum', methods=['GET','POST'])
def new_forum():
    form = NewFolder()
    if form.validate_on_submit():
        return redirect(url_for('new_thread', forum=form.name.data))
    return render_template('newfolder.html', title='New Forum', form=form)

@app.route('/new_thread/<forum>', methods=['GET','POST'])
def new_thread(forum):
    form = NewFolder()
    if form.validate_on_submit():
        return redirect(url_for('new_post', forum=forum, thread=form.name.data))
    return render_template('newfolder.html', title='New Thread', form=form)

@app.route('/new_post/<forum>/<thread>', methods=['GET','POST'])
def new_post(forum, thread):
    form = NewPost()
    if form.validate_on_submit():
        post = {'body':{
            "forum":forum,
            "thread":thread,
            "title":form.title.data,
            "content":form.content.data,
        }}
        response = requests.post('https://krqrgv5s6b.execute-api.eu-west-2.amazonaws.com/Forum/forumpost', json=post)
        return redirect(url_for('thread', forum=forum, thread=thread))
    return render_template('newpost.html', title='New Post', form=form)

