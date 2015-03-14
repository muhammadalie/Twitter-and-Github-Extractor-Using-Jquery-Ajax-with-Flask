#!flask/bin/python
import sqlite3
from flask import Flask
from flask.ext.login import LoginManager
app= Flask(__name__)
app.config.from_object('config')
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required,user_logged_in
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField,PasswordField, validators,TextField,TextAreaField,IntegerField
from wtforms.validators import DataRequired
import requests
import json
import twitter
import oauth2 as oauth,json
def oauth_req(url, key='597987159-cX3oqo8rGFVC0i1WZZuN8hI0qKXjcAQBZlE66un7', secret='7idwwQzFB1TqRmKBcTSFwW79BGKMkykb6c2oT1s2GLWoN', http_method="GET", post_body=None, http_headers=None):
    consumer = oauth.Consumer(key='GcPPtjWQoHZiLWTpMQa3z44Es', secret='JJo4VbMBKJ6J9FdSl6x10tpGWGh2mEBjc1NzHXxDWCNo3mhILz')
    token = oauth.Token(key=key, secret=secret)
    client = oauth.Client(consumer, token)
    resp, content = client.request( url)
    return content
class URLForm(Form):
	url = StringField('url', validators=[DataRequired()])
	git = StringField('git', validators=[DataRequired()])
class URForm(Form):
        url = StringField('url', validators=[DataRequired()])



@app.route('/', methods=['GET', 'POST'])
def home():
	form= URLForm()
	#git= URForm()
	r=[]
	l=""
	#if form.validate_on_submit():
	if request.method == 'POST' and request.form["subm"] == "twit":
		name=form.url.data
		a= oauth_req('https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name='+name+'&count=10')
		r=json.loads(a)
		f=open('static/tweet.txt','w+')
		f.write('<ol>')
		for tweet in r:
			f.write('<li>'+tweet["text"]+'\n')
		f.write('</ol>')
		return render_template('home.html',form=form,loaddata="loaddata()")

	#if git.validate_on_submit():

	elif request.method == 'POST' and request.form["subm"] == "git":

                name=form.git.data
		url='https://api.github.com/users/'+name+'/repos'
		r=requests.get(url)
		a=r.text
		repos=json.loads(a)
                f=open('static/gith.txt','w+')
                f.write('<ol>')
                for rep in repos:
                        f.write('<li>'+rep["name"]+'\n')
                f.write('</ol>')
                return render_template('home.html',form=form,loadgit='loadgit()')
	
	return render_template('home.html',form=form)
app.run(debug=True)
