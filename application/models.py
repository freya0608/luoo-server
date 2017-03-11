from flask import current_app
from sqlalchemy.orm import relationship

from . import db


song_creator = db.Table('song_creator', db.metadata,
    db.Column('song_id', db.Integer, db.ForeignKey('song.id')),
    db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'))
)

volume_song = db.Table('volume_song', db.metadata,
    db.Column('song_id', db.Integer, db.ForeignKey('song.id')),
    db.Column('volume_id', db.Integer, db.ForeignKey('volume.id'))
)

album_song = db.Table('album_song', db.metadata,
    db.Column('song_id', db.Integer, db.ForeignKey('song.id')),
    db.Column('album_id', db.Integer, db.ForeignKey('album.id'))
)


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=400))

    songs = db.relationship('Song', secondary=song_creator, back_populates="artists")


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(length=400))

    songs = relationship("Song", secondary=album_song)

    @property
    def poster(self):
        valuable_url = "pics/albums/{}/cover.jpg?imageView2/1/w/580/h/580".format(self.id)
        return "{}{}".format(current_app.config['LUOO_IMG_CDN_PREFIX'], valuable_url)

    @property
    def poster_small(self):
        valuable_url = "pics/albums/{}/cover.jpg?imageView2/1/w/60/h/60".format(self.id)
        return "{}{}".format(current_app.config['LUOO_IMG_CDN_PREFIX'], valuable_url)


class Volume(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(length=400))

    songs = relationship('Song', secondary=volume_song)


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(length=400))
    valuable_url = db.Column(db.String(length=500))

    artists = relationship('Artist', secondary=song_creator, back_populates="songs")

    @property
    def url(self):
        url = "{}{}".format(current_app.config['LUOO_SONG_CDN_PREFIX'], self.valuable_url)
        return url

