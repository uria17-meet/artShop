from flask import *
from model import *


app = Flask(__name__)

engine = create_engine('sqlite:///Database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app.url_map.strict_slashes = False


@app.route('/')
def landing_page():
    return "hello"



if __name__ == '__main__':
    app.run(debug=True,)
