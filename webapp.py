from flask import *
from model import *

app = Flask(__name__)

engine = create_engine('sqlite:///Database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def main_page():
	return render_template('main_')
@app.route('/login', methods=['GET ', 'POST'])
def login():

    return render_template('login.html')

@app.route('/main', method='GET')

if __name__ == '__main__':
    app.run()
