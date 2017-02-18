from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, func

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    fullname = Column(String(60))
    address = Column(String(255))
    email = Column(String(60))
    username = Column(String(60), unique=True)
    password = Column(String(60))
    phone = Column(String(60))
    artist = Column(Integer)
    artworks = relationship('Artwork', back_populates='artist')


class Artwork(Base):
    __tablename__ = 'artwork'

    id = Column(Integer, primary_key=True)
    artist_id = Column(Integer, ForeignKey('user.id'))
    artist = relationship('User', back_populates=('artworks'))
    name = Column(String(60))
    height = Column(Integer)
    width = Column(Integer)
    material = Column(String(60))
    price = Column(Integer)
    photo = Column(String(255))

    def set_photo(self, photo):
        self.photo = 'static/art_photos/'+ str(photo)

engine = create_engine('postgres://yvzbzplexyqilh:286c9c81f55fb53c45301e9efd42f97b5249278ea8ac38528f1bfe411a557179@ec2-184-72-249-88.compute-1.amazonaws.com:5432/deluv9sufc0caq')
Base.metadata.create_all(engine)
