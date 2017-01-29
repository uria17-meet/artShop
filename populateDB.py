from model import *


engine = create_engine('sqlite:///Database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

users = [
    {'fullname': 'Uria Cohen', 'address': 'Alon HaGalil', 'username': 'uriacohen',
        'email': 'uriacohen0@gmail.com', 'password': 'ASDqwe123'}

]
for user in users:
    newUser = User(
        fullname=user['fullname'],
        address=user['address'],
        email=user['email'],
        password=user['password'],)

    session.add(newUser)
    session.commit()