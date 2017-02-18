from flask import Flask, url_for, flash, render_template, redirect, request, g
from flask import session as login_session
from werkzeug.utils import secure_filename
from model import *
import os


UPLOAD_FOLDER = 'static/art_photos/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

app.secret_key = 'meet_is_so_cool'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
engine = create_engine('postgres://yvzbzplexyqilh:286c9c81f55fb53c45301e9efd42f97b5249278ea8ac38528f1bfe411a557179@ec2-184-72-249-88.compute-1.amazonaws.com:5432/deluv9sufc0caq')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
            login_session['artist'] = user.artist
            flash('Login successful', 'success')
            return redirect(url_for('home'))
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
            newuser = User(email=email, fullname=fullname, username=username,
                           password=password, address=address, artist=artist, phone=phone)
            session.add(newuser)
            session.commit()
            print('commit')
            flash("Sign up successful, now just log in .", 'success')
            return redirect(url_for('landing'))
    else:
        return render_template('sign_up.html')


@app.route('/gallery')
def gallery():
    artworks = session.query(Artwork).all()
    return render_template('gallery.html', artworks=artworks)


@app.route('/home')
def home():
    if 'username' in login_session:
        user = session.query(User).filter_by(
            username=login_session['username'])
        return render_template('home.html', user=user)
    else:
        flash("An error has accured : you must login first", 'danger')
        return redirect(url_for('landing'))


@app.route('/shop')
def shop():
    if 'username' in login_session:
        artworks = session.query(Artwork).all()
        user = session.query(User).filter_by(
            username=login_session['username']).first()
        return render_template('shop.html', artworks=artworks, user=user)
    else:
        flash("An error has accured : you must login first", 'danger')
        return redirect(url_for('landing'))


@app.route('/logout')
def logout():
    if 'username' in login_session:
        login_session.pop('username', None)
        flash("Logout successful", 'success')
        return redirect(url_for('landing'))
    else:
        flash("An error has accured : you must login first", 'danger')
        return redirect(url_for('landing'))


@app.route('/myartworks')
def myartworks():
    if login_session['username'] is not None and login_session['artist'] == 1:
        artworks = session.query(Artwork).filter_by(
            artist_id=login_session['id']).all()
        user = session.query(User).filter_by(
            username=login_session['username']).first()
        return render_template('myartworks.html', artworks=artworks, user=user)
    else:
        flash("An error has accured : you must login first", 'danger')
        return redirect(url_for('landing'))


@app.route('/myartworks/deletartwork/<int:id>')
def deleteartwork(id):
    session.delete(session.query(Artwork).filter_by(
        artist_id=login_session['id']).filter_by(id=id).first())
    session.commit()

    flash("Your artwork was successfuly deleted", 'success')
    return redirect(url_for('myartworks'))


@app.route('/home/deleteacount')
def deleteacount():
    session.delete(session.query(User).filter_by(
        id=login_session['id']).first())
    session.commit()
    if login_session['id'] is not None:
        login_session.pop('id', None)
    flash("Your acount was successfuly deleted", 'success')
    return redirect(url_for('landing'))


@app.route('/myartworks/addartwork', methods=['GET', 'POST'])
def addartwork():
    if request.method == 'GET':
        return render_template('addartwork.html')
    elif request.method == 'POST':
        artist_id = login_session['id']
        name = request.form['name']
        height = request.form['height']
        width = request.form['width']
        material = request.form['material']
        price = request.form['price']
        file = request.files['file']
        if file and allowed_file(file.filename):
            artwork = Artwork(artist_id=artist_id,name=name,height=height,width=width,material=material,price=price)
            session.add(artwork)
            session.commit()
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(filename)
            artwork.set_photo(filename)
            session.add(artwork)
            session.commit()
            return redirect(url_for('myartworks'))
        else:
            flash('Please upload either a .jpg, .jpeg, .png, or .gif file.','warning')
            return redirect(url_for('addartwork'))

if __name__ == '__main__':
    app.run(debug=True,)
