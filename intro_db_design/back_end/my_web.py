import sys
import bottle
from bottle import route, run, static_file, request, post, get
import pymysql as db
import my_settings
import my_web_app

@route('/PresentationOfArtists', method = 'POST')
def PresentationOfArtists():
    return bottle.template('PresentationOfArtists.tpl')

@route('/ViewArtistResults' , method = 'POST')
def do_PresentationOfArtists():
    return my_web_app.presentation_of_artists()

@route('/UpdateArtistInformation' ,method = 'POST')
def do_ViewArtistResults():
    return my_web_app.view_artist_results()

@route('/Update_info' ,method = 'POST')
def do_UpdateArtistInformation():
    return my_web_app.update_artist_information()

@route('/PresentationOfSongs', method = 'POST')
def PresentationOfSongs():
    return bottle.template('PresentationOfSongs.tpl')

@route('/ViewSongsResults', method = 'POST')
def do_PresentationOfSongs():
    return my_web_app.presentation_of_songs()

@route('/InsertArtist', method = 'POST')
def InsertArtist():
    return bottle.template("InsertArtist.tpl")

@route('/Insert_Artist_Info', method = 'POST')
def do_InsertArtist():
    return my_web_app.insert_artist_information()

@route('/InsertSong', method = 'POST')
def InsertSong():
    return my_web_app.insert_song_preview()

@route('/Insert_Song_Info', method = 'POST')
def do_InsertSong():
    return my_web_app.insert_song_information()

@route('/')
def root():

    return bottle.template('root.tpl')

@route('/',method = 'POST')
def return_to_root():

    return bottle.template('root.tpl')

run(host = my_settings.mysql_host, port= my_settings.web_port, reloader=True, debug=True)
