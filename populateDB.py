from model import *


engine = create_engine('sqlite:///Database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

users = [
    {'fullname': 'Uria Cohen', 'address': 'Alon HaGalil', 'username': 'uriacohen',
        'email': 'uriacohen0@gmail.com', 'password': 'ASDqwe123','artist': False,}

]

everyone = session.query(User).all()
for i in everyone:
    session.delete(i)
    session.commit()

for user in users:
    newUser = User(
        fullname=user['fullname'],
        address=user['address'],
        email=user['email'],
        password=user['password'],
        username=user['username'],
        artist=user['artist'])
    session.add(newUser)
    session.commit()