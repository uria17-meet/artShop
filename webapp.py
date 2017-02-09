from flask import Flask,url_for, flash, render_template, redirect, request, g
from model import *


app = Flask(__name__)

engine = create_engine('sqlite:///Database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app.url_map.strict_slashes = False

def verify_password(username, password):
	user = session.query(user).filter_by(username=username).first()
	if not user or not user.verify_password(password):
		return False
	g.user = user
	return True

@app.route('/', methods = ['GET','POST'])
def landing():
	if request.method == 'GET':
		return render_template('landing.html')
	elif request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if verify_password(username, password):
			user = session.query(User).filter_by(username=username).one()
			login_session['username'] = user.username
			login_session['id'] = user.id
			return redirect(url_for('landing'))
		else:
			flash('Incorrect username/password combination')
			return redirect(url_for('landing'))





if __name__ == '__main__':
    app.run(debug=True,)
