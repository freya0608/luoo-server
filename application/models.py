from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import relationship

import config
from database import Base, Session

album_pattern = re.compile("^http://www.luoo.net/music/(\d+)\?sid=(\d+)$")
session = Session()


song_creator = Table('song_creator', Base.metadata,
    Column('song_id', Integer, ForeignKey('songs.id')),
    Column('artist_id', Integer, ForeignKey('artists.id'))
)

volume_song = Table('volume_song', Base.metadata,
    Column('song_id', Integer, ForeignKey('songs.id')),
    Column('volume_id', Integer, ForeignKey('volumes.id'))
)

album_song = Table('album_song', Base.metadata,
    Column('song_id', Integer, ForeignKey('songs.id')),
    Column('album_id', Integer, ForeignKey('albums.id'))
)


class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=400))

    songs = relationship('Song', secondary=song_creator, back_populates="artists")


class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(length=400))

    songs = relationship("Song", secondary=album_song)

    @property
    def poster(self):
        valuable_url = "pics/albums/{}/cover.jpg?imageView2/1/w/580/h/580".format(self.id)
        return "{}{}".format(config.LUOO_IMG_CDN_PREFIX, valuable_url)

    @property
    def poster_small(self):
        valuable_url = "pics/albums/{}/cover.jpg?imageView2/1/w/60/h/60".format(self.id)
        return "{}{}".format(config.LUOO_IMG_CDN_PREFIX, valuable_url)


class Volume(Base):
    __tablename__ = "volumes"

    id = Column(Integer, primary_key=True, autoincrement=False)
    title = Column(String(length=400))

    songs = relationship('Song', secondary=volume_song)


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, autoincrement=False)
    title = Column(String(length=400))
    valuable_url = Column(String(length=500))

    artists = relationship('Artist', secondary=song_creator, back_populates="songs")
