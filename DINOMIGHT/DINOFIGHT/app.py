#!/usr/local/bin/Python

from flask import Flask, render_template, session, request, redirect, url_for, session

import db

app = Flask(__name__)
app.secret_key = "KEHTYSOEIETIRRUVSERSCY"

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html');
    else:
        if request.form['password'] != request.form['pw_verify']:
            print request.form['username'], request.form['pw_verify']
            return render_template('register.html', error='Passwords do not match')
        if db.register_user(request.form['username'],request.form['password']):
            return redirect(url_for('read'))
        else:
            return render_template('register.html', error='Username already exists')

@app.route('/login', methods=['GET','POST'])
def login():
    if 'username' in session:
        return redirect(url_for('read'))
    if request.method == 'GET':
        return render_template("login.html")
    else:
        if db.check_user(request.form['username'],request.form['password']):
            session['username'] = request.form['username']
            return redirect(url_for('read'))
        else:
            return render_template("login.html", error="Wrong username/password combination")

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('read'))

@app.route('/passchange', methods=['GET','POST'])
def passchange():
    if request.method == 'GET':
        return render_template("pwchange.html")
    if db.check_user(request.form['username'],request.form['password']) and request.form['new'] == request.form['confirm']:
        db.change_pass(request.form['username'],request.form['new'])
        return render_template("pwchange.html",error="Password changed successfully.")
    else:
        return render_template("pwchange.html",error="Incorrect username and password combination or new passwords don't match.")

@app.route('/stories')
def stories():
    return render_template('readPage.html')
    #list of user's stories

@app.route('/story/<title>', methods=['GET','POST'])
def story(title):
    if request.method == 'GET':
        sid = db.get_storyid(title)
        if sid == None:
            return render_template("404.html", obj="story")
        return None#"<h1>%s</h1>%s"%(db.get_title(sid), db.get_story(sid))

@app.route('/u/<usern>')
def profile(usern):
    if not db.user_exists(usern):
        return render_template('404.html', obj="user")
    originals = [db.get_title(sid) for sid in db.stories_by_user(usern)]
    contributed = [(len(db.contributions_to_story(usern, sid)), db.get_title(sid)) for sid in db.stories_with_user_contributions(usern)]
    contributed.sort(reverse=True)
    return render_template('user.html', username=usern, originals=originals, contribs=contributed)

@app.route('/write', methods=['GET', 'POST'])
def write():
    if not 'username' in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        storyid = db.random_story(session['username'])
        if not storyid:
            return redirect(url_for('add'))
        return render_template('writePage.html', story=db.get_story(storyid))
    else:
        pass
	#TODO: Handle POST

@app.route('/add', methods=['GET', 'POST'])
def add():
    if not 'username' in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('addPage.html')
    else:
	#TODO: Handle POST
        pass

@app.route('/')
@app.route('/read')
def read():
    return redirect(url_for('stories'))

if __name__ == '__main__':
    app.debug = True
    app.run()
