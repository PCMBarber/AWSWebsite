import boto3, botocore
from flask import render_template, redirect, url_for, Response, request
from flask_login import login_user, current_user, logout_user, login_required
from application import app, db, password_hash as pw
from application.forms import LoginForm, RegisterForm, NewFolder, NewPost
from Application.models import users, posts

@app.route('/')
@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = users.query.filter_by(user_name=form.user_name.data).first()
        if user and pw.verify_password(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('dashboard'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if form.validate_on_submit():
        hashed = pw.hash_password(form.password.data)
        user = users(
            user_name=form.user_name.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=hashed,
            admin=False
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    else:
        print(RegisterForm.errors)
        return render_template('register.html', title='Register', form=form)

@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    s3 = boto3.client('s3')
    bucket_name = "milestone-piers-1"
    forums = []
    response = s3_client.list_objects_v2(
                Bucket= bucket_name,
                Prefix = "Forums/",
                MaxKeys= 100
                )
    for entry in response:
        key = entry.Contents.Key()
        tmplist = key.split("/")
        index = tmplist.index("Forum")
        forumName = tmplist[(index + 1)]
        if forumName is in forums:
            continue
        else:
            forums.append(forumName)
    return render_template('dashboard.html', title='Dashboard', forums=forums)

@app.route('/createForum/<forum>', methods=['GET','POST'])
@login_required
def createForum(forum):
    s3 = boto3.client('s3')
    bucket_name = "milestone-piers-1"
    directory_name = ("milestone-piers-1/Forums/"+forum)
    s3.put_object(Bucket=bucket_name, Key=(directory_name+'/'))
    return redirect(url_for('dashboard'))

@app.route('/createThread/<forum>/<thread>', methods=['GET','POST'])
@login_required
def createThread(forum, thread):
    s3 = boto3.client('s3')
    bucket_name = "milestone-piers-1"
    directory_name = ("milestone-piers-1/Forums/"+forum+"/"+thread)
    s3.put_object(Bucket=bucket_name, Key=(directory_name+'/'))
    return redirect(url_for('dashboard'))

@app.route('/forum/<forum>', methods=['GET','POST'])
@login_required
def forum(forum):
    s3 = boto3.client('s3')
    bucket_name = "milestone-piers-1"
    threads = []
    response = s3_client.list_objects_v2(
                Bucket= bucket_name,
                Prefix = ("Forums/"+forum+"/"),
                MaxKeys= 100 
                )
    for entry in response:
        key = entry.Contents.Key()
        tmplist = key.split("/")
        index = tmplist.index("Forum")
        threadName = tmplist[(index + 2)]
        if threadName is in threads:
            continue
        else:
            threads.append(threadName)
    return render_template('forum.html', title=forum, threads=threads)

@app.route('/thread/<forum>/<thread>', methods=['GET','POST'])
@login_required
def thread(forum, thread):
    query = posts.query.filter_by(forum=forum, thread=thread).all()    
    return render_template('thread.html', title=thread, posts=query, forum=forum, thread=thread)

@app.route('/upload/<forum>/<thread>', methods = ['GET','POST'])
@login_required
def upload(forum, thread):
   if request.method == 'POST':
      f = request.files['file']
      s3 = boto3.client('s3')
      bucket_name = "milestone-piers-1"
      s3.meta.client.upload_file(("Forum/"+forum+"/"+thread+"/"+f),​bucket_name,f)
      return redirect(url_for('thread', forum=forum, thread=thread))

@app.route('/new_forum', methods=['GET','POST'])
@login_required
def thread():
    form = NewFolder()
    if form.validate_on_submit():
        return redirect(url_for('createThread', forum=forum, thread=form.name.data))
    return render_template('newfolder.html', title='New Forum', form=form)

@app.route('/new_thread/<forum>', methods=['GET','POST'])
@login_required
def thread(forum):
    form = NewFolder()
    if form.validate_on_submit():
        return redirect(url_for('createForum', forum=form.name.data))
    return render_template('newfolder.html', title='New Thread', form=form)

@app.route('/view_post/<post>', methods = ['GET','POST'])
@login_required
def view_post(post):
    query = posts.query.filter_by(title=post).first()
    if query.image != NULL:
        try:
            s3.Bucket("milestone-piers-1").download_file(query.image,('Images/'+query.image))
            full_filename = os.path.join(app.config['UPLOAD_FOLDER'], query.image)
            return render_template('post.html', title=post, content=query, image=full_filename)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise
    else:
        return render_template('post.html', title=post, content=query)

@app.route('/new_post/<forum>/<thread>', methods=['GET','POST'])
@login_required
def new_post(forum, thread):
    form = NewPost()
    if form.validate_on_submit():
        post = posts(
            forum=forum,
            thread=thread,
            title=form.title.data,
            content=form.content.data,
            image=form.image.data.filename
        )
        db.session.add(post)
        db.session.commit()
            forum=forum,
            thread=thread,
            title=form.title.data,
            content=form.content.data,
            image=form.image.data.filename
        )
        db.session.add(post)
        db.session.commit()
        s3 = boto3.client('s3')
        bucket_name = "milestone-piers-1"
        s3.meta.client.upload_file(("Forum/"+forum+"/"+thread+"/"+'''FILE'''),​bucket_name,'''FILE''')
        return redirect(url_for('thread', forum=forum, thread=thread))
    return render_template('newpost.html', title='New Post', form=form)one-piers-1"
        s3.meta.client.upload_file(("Forum/"+forum+"/"+thread+"/"+'''FILE'''),​bucket_name,'''FILE''')
        return redirect(url_for('thread', forum=forum, thread=thread))
    return render_template('newpost.html', title='New Post', form=form)