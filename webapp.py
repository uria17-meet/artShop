from flask import Flask, url_for, flash, render_template, redirect, request, g
from flask import session as login_session
from model import *


app = Flask(__name__)

app.secret_key = 'meet_is_so_cool'
engine = create_engine('sqlite:///Database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app.url_map.strict_slashes = False


def verify_password(username, password):
    user = session.query(User).filter_by(username=username).first()
    if not user or not user.password == password or not user.username == username:
        return False
    return True


@app.route('/', methods=['GET', 'POST'])
def landing():
    if request.method == 'GET':
        return render_template('landing.html')
        print(shaa)
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if verify_password(username, password):
            user = session.query(User).filter_by(username=username).one()
            login_session['username'] = user.username
            login_session['id'] = user.id
            print('LALALALALAL')
            return redirect(url_for('logged'))
        else:
            flash("invalid username password combination", 'danger')
            return redirect(url_for('landing'))


@app.route('/logged')
def logged():
    if login_session['username'] is not None:
        return login_session['username']


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    print('0')
    if request.method == 'POST':
        print('1')
        username = request.form['username']
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']
        artist = request.form['artist']
        if session.query(User).filter_by(username=username).first() is None:
            newuser = User(email=email, fullname=fullname, username=username,password=password, address=address, artist=artist)
            session.add(newuser)
            session.commit()
            print('commit')
            return redirect(url_for('landing'))
            flash("Sign up successful, now just log in .",'success')
    else:
        return render_template('sign_up.html')
        


if __name__ == '__main__':
    app.run(debug=True,)
