from model import *


engine = create_engine('sqlite:///Database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

users = [
    {'fullname': 'Uria Cohen', 'address': 'Alon HaGalil', 'username': 'uriacohen',
        'email': 'uriacohen0@gmail.com', 'password': 'ASDqwe123', 'artist': 1, 'phone':'0544911263'}

]

artworks = [
    {'name': 'the TEST', 'height': '70cm', 'width': '50cm', 'material': 'oil on canvas', 'price': 23145,
        'photo': 'http://upload.wikimedia.org/wikipedia/commons/d/d5/Mona_Lisa_(copy,_Hermitage).jpg', 'artist_id': 1,}
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
        artist=user['artist'],
        phone=user['phone'])
    session.add(newUser)
    session.commit()

# for artwork in artworks:
#     newArtwork = Artwork(
#         artist_id=artwork['artist_id'],
#         name=artwork['name'],
#         height=artwork['height'],
#         width=artwork['width'],
#         material=artwork['material'],
#         price=artwork['price'],
#         photo=artwork['photo'])
#     session.add(newArtwork)
#     session.commit()
