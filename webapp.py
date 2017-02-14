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
            return redirect(url_for('home'))
            flash('Login successful','success')
        else:
            flash("invalid username password combination", 'danger')
            return redirect(url_for('landing'))




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
        phone = request.form['phone']
        if session.query(User).filter_by(username=username).first() is None:
            newuser = User(email=email, fullname=fullname, username=username,password=password, address=address, artist=artist,phone=phone)
            session.add(newuser)
            session.commit()
            print('commit')
            return redirect(url_for('landing'))
            flash("Sign up successful, now just log in .",'success')
    else:
        return render_template('sign_up.html')
        
@app.route('/gallery')
def gallery():
    artworks = session.query(Artwork).all()
    return render_template('gallery.html', artworks=artworks)

@app.route('/home')
def home():
    if login_session['username'] is not None:
        user = session.query(User).filter_by(username=login_session['username'])
        return render_template('home.html',user=user)
    else:
        return redirect(url_for('landing'))
        flash("Login first",'danger')

@app.route('/shop')
def shop():
    if login_session['username'] is not None:
        artworks = session.query(Artwork).all()
        user = session.query(User).filter_by(username=login_session['username']).first()
        return render_template('shop.html',artworks=artworks ,user=user)
    else:
        return redirect(url_for('landing'))
        flash("Login first",'danger')

@app.route('/logout')
def logout():
    if login_session['username'] is not None:
        login_session.pop('username',None)
        return redirect(url_for('landing'))
    else:
        return redirect(url_for('landing'))
        flash("Login first",'danger')



if __name__ == '__main__':
    app.run(debug=True,)
