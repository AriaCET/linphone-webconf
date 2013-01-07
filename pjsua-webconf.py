#!/usr/bin/env python2
from __future__ import with_statement
from contextlib import closing

import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import os


DATABASE = 'phones.db'
DEBUG = True
SECRET_KEY = 'development key'
DEFAULTUSERNAME = 'admin'
DEFAULTPASSWORD  = 'default'
PJSUA_CONFIG_FILE = 'pjsua.cfg'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
  return sqlite3.connect(app.config['DATABASE'])

def init_db():
  with closing(connect_db()) as db:
    with app.open_resource('schema.sql') as schema:
      db.cursor().executescript(schema.read())
      setauth(db,app.config['DEFAULTUSERNAME'],app.config['DEFAULTPASSWORD'])
    db.commit()

def auth(user,password):
  import md5
  cur = g.db.execute('select username, password from auth')
  for row  in cur:
    db_user = row[0]
    db_pass = row[1]
  try:
    hash = md5.new(password)
    if (user == db_user) and (hash.hexdigest() == db_pass):
      return True
  except TypeError:
      return False
  return False

def setauth(db,user,password):
  import md5
  pashash = md5.new()
  pashash.update(password)
  db.execute("delete from auth")
  db.execute("insert into auth (username, password) values('{0}', '{1}')".format(user,pashash.hexdigest()))
  db.commit()

def writeconfig(db):
  configprefix="# This is auto generated config file.\n--local-port=5061\n"
  configaccdetails ="--id sip:{username}@{server}\n--registrar sip:{server}\n--realm *\n--username {username}\n--password {password}\n--auto-answer=200\n"
  confignextacc = "--next-account\n"
  configFile = open(app.config['PJSUA_CONFIG_FILE'],"w")
  configFile.write(configprefix)
  cur = db.execute('select username, server,password from entries order by id')
  firstacc=True
  for row in cur.fetchall():
    if(firstacc):
      firstacc = False
    else:
      configFile.write(confignextacc)
    context = configaccdetails.format(username=row[0],server=row[1],password=row[2])
    configFile.write(context)
  configFile.close()

# App stuff
@app.before_request 
def before_request():
  g.db = connect_db()
  
@app.teardown_request
def teardown_request(exception):
  g.db.close()

@app.route('/')
def show_entries():
  cur = g.db.execute('select id,title, username, server from entries order by id')
  entries = [row for row in cur.fetchall()]
  return render_template('show_entries.html',entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
  if not session.get('logged_in'):
    abort(401)
  g.db.execute('insert into entries (title, username, password, server) values(?, ?, ?, ?)', [request.form['title'],request.form['username'],request.form['password'],request.form['server']])
  g.db.commit()
  flash('New entry successfuly posted')
  return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET','POST'])
def login():
  error = None
  if request.method == 'POST':
    if not auth(request.form['username'], request.form['password']):
      error = 'Authentication failure '
    else:
      session['logged_in'] = True
      flash('You were logged in!')
      return(redirect(url_for('show_entries')))

  return render_template('login.html', error=error)
  
@app.route('/changepassword',methods=['GET','POST'])
def changepassword():
  error = None
  if request.method == 'POST':
    print request.form
    username = request.form['username']
    password = request.form['password']
    rpassword = request.form['rpassword']
    if len(username) == 0:
      error = "Username is Empty"
    elif password != rpassword:
      error = 'Passwords do not match'
    else :
      setauth(g.db,username,password)
      flash('Password changed')
      return(redirect(url_for('show_entries')))
  return render_template('password.html', error=error)

@app.route('/delete/<eID>')
def delete(eID):
  error = None
  if not session.get('logged_in'):
    abort(401)
  g.db.execute("delete from entries where id = '{0}'".format(eID))
  g.db.commit()
  flash('The entry successfuly deleted')
  return redirect(url_for('show_entries'))

@app.route('/edit/<eID>',methods=['GET','POST'])
def edit(eID):
  error = None
  if not session.get('logged_in'):
    abort(401)
  if request.method == 'POST':
    title = request.form['title']
    username = request.form['username']
    password = request.form['password']
    server = request.form['server']
    g.db.execute("update entries set title='{0}', username='{1}',password='{2}', server='{3} where id = '{4}'"\
        .format(title,username,password,server,eID))
    g.db.commit()
    flash("Updted")
    return redirect(url_for('show_entries'))
  else :
    cur = g.db.execute("select title,username, password, server from entries where id = '{0}'".format(eID))
    entry = [row for row in cur][0]
    return render_template('edit.html', error=error,entry=entry)

  
@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  flash('You were logged out')
  writeconfig(g.db)
  return redirect(url_for('show_entries'))

if __name__ == "__main__":
  if not os.path.isfile(app.config['DATABASE']):
    init_db()
  app.run()
