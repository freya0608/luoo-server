import logging
import pickle
import re

from flask_sqlalchemy import SQLAlchemy
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist

import config.default as config
from application import create_app
from application.models import Song, Album, Artist, Volume

logger = logging.getLogger("update_songs_job")
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('job.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

volume_pattern = re.compile("^http://www.luoo.net/music/(\d+)$")
album_and_song_pattern = re.compile("/radio(\d+)/(\d+).mp3")
valuable_url_pattern = re.compile("{}(.*)".format(config.LUOO_SONG_CDN_PREFIX))
album_pattern = re.compile("albums/(\d+)/")

user_agent = """Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3)
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"""


def format_volume_url(volume_id):
    return 'http://www.luoo.net/music/{}'.format(volume_id)


def load_lowest_volume():
    try:
        with open("lowest_volume_id.pickle", "rb") as f:
            volume = pickle.load(f)
    except FileNotFoundError:
        volume = 1
        with open("lowest_volume_id.pickle", "wb") as f:
            pickle.dump(volume, f, pickle.HIGHEST_PROTOCOL)
    return volume


def get_latest_volume():
    with Browser('phantomjs', user_agent=user_agent) as browser:
        browser.visit("http://www.luoo.net/")
        latest_volume_url = browser.find_by_css(".section-vol .vol-item-lg a").first["href"]
        volume = volume_pattern.search(latest_volume_url).groups()[0]
    return int(volume)


def parse_valuable_url(song_url):
    search_result = valuable_url_pattern.search(song_url)
    if search_result is not None:
        return search_result.groups()[0]

    logger.debug("{} should be fixed!".format(song_url))

    search_result = album_and_song_pattern.search(song_url)
    if search_result is not None:
        volume_id, song_id = search_result.groups()
        return "{}luoo/radio{}/{}.mp3".format(config.LUOO_SONG_CDN_PREFIX, volume_id, song_id)


def save_song(song_dict):
    valuable_url = parse_valuable_url(song_dict["mp3"])
    song_id = song_dict["id"]
    saved_song = db.session.query(Song).get(song_id)
    if saved_song is None:
        saved_song = Song(id=song_id, title=song_dict["title"], valuable_url=valuable_url)
    return saved_song


def parse_album_id(poster_url):
    groups = album_pattern.search(poster_url).groups()
    return int(groups[0])


def create_album(song_dict):
    album_id = parse_album_id(song_dict["poster"])
    saved_album = db.session.query(Album).get(album_id)
    if saved_album is None:
        saved_album = Album(id=album_id, name=song_dict["album"])
    return saved_album


def create_artists(song_dict):
    artist_names = [name.strip() for name in song_dict["artist"].split(";")]
    return [Artist(name=artist_name) for artist_name in artist_names]


def update_lowest_volume(volume_id):
    with open("lowest_volume_id.pickle", "wb") as f:
        pickle.dump(volume_id, f, pickle.HIGHEST_PROTOCOL)


def run():
    lowest_volume = load_lowest_volume()
    latest_volume = get_latest_volume()
    is_latest_volume_saved = latest_volume < lowest_volume
    if is_latest_volume_saved:
        logger.info('Latest volume {} had been saved'.format(latest_volume))
        return

    with Browser('phantomjs', user_agent=user_agent) as browser:
        for volume_id in range(lowest_volume, latest_volume + 1):
            volume_url = format_volume_url(volume_id)
            logger.info('Parsing songs of volume: {}'.format(volume_id))
            browser.visit(volume_url)

            try:
                img_404_not_present = browser.is_element_not_present_by_css(
                    "img[src='http://s.luoo.net/img/icon_404.png']")
                if not img_404_not_present:
                    lowest_volume += 1
                    update_lowest_volume(lowest_volume)
                    continue
                title = browser.find_by_css(".vol-name .vol-title").first.text
            except ElementDoesNotExist:
                logger.debug("Volume {} has no title!".format(volume_url))
                browser.driver.save_screenshot("exception.png")
                raise

            with app.app_context():
                try:
                    volume = Volume(id=volume_id, title=title)
                    song_list = browser.evaluate_script('window.luooPlayer.playlist')
                    for s in song_list:
                        song = save_song(s)
                        artists = create_artists(s)
                        song.artists.extend(artists)

                        album = create_album(s)
                        album.songs.append(song)
                        volume.songs.append(song)
                        db.session.add(volume)
                        db.session.add(album)
                    db.session.commit()
                    lowest_volume += 1
                    update_lowest_volume(lowest_volume)
                except:
                    db.session.rollback()
                    raise


if __name__ == '__main__':
    app = create_app()
    db = SQLAlchemy()
    db.init_app(app)
    run()
