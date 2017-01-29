from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
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


engine = create_engine('sqlite:///Database.db')
Base.metadata.create_all(engine)
