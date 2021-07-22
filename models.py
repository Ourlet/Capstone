import os
from typing import Collection
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from sqlalchemy.sql.schema import ForeignKey
db = SQLAlchemy()
'''
setup_db(app):
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    database_name ='local_capstone'
    default_database_path= "postgres://{}:{}@{}/{}".format('postgres', 'Salope59', 'localhost:5432', database_name)
    database_path = os.getenv('DATABASE_URL', default_database_path)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
'''
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


'''
Distribution
Table to allow many-to-many relationship between Actors and Movies
'''
distribution = db.Table(
  'distribution',
  Column('actor_id', Integer, ForeignKey('actors.id'), primary_key=True),
  Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True)
)

'''
Movie 
Have title, release date and distribution foreign key
'''
class Movie(db.Model):  
  __tablename__ = 'movies'

  id = Column(Integer, primary_key = True)
  title = Column(String, nullable = False)
  release_date = Column(db.DateTime, nullable = False)
  distribution = db.relationship('Actor', secondary=distribution, backref=db.backref('movie', lazy = True))

  def __init__(self, title, release_date):
    self.title = title
    self.release_date = release_date
  
  def insert(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def list_movie(self):
    return {
      "id": self.id,
      "title" : self.title,
      "release_date" : self.release_date
    }

  def list_movie_with_actors(self):
    return {
    "id" : self.id,
    "title" : self.title,
    "distribution" : [actor.name for actor in self.distribution]
    }

  def __repr__(self):
    return "<Movie {} {} />".format(self.title, self.release_date)


'''
Actor 
Have name, age, gender and distribution foreign key
'''

class Actor(db.Model):  
  __tablename__ = 'actors'

  id = Column(Integer, primary_key = True)
  name = Column(String(100), nullable = False)
  age = Column(Integer(), nullable = False)
  gender = Column(String(), nullable = False)

  def __init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def actors(self):
    return {
      "id": self.id,
      "name" : self.name,
      "age" : self.age,
      "gender" : self.gender
    }

  def movies_per_actor(self):
    return {
      "name" : self.name,
      "movies" : [movie.title for movie in self.movies ]
    }

  def __repr__(self):
    return "<Actor {} {} {} />".format(self.name, self.age, self.gender)