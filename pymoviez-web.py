# http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

# http://webpy.org/  http://webpy.org/docs/0.3/tutorial
# https://github.com/defunkt/pystache 
#!/usr/bin/env python
# http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

import os
import sys
import flask
import signal

from pymoviez import *

HOST='127.0.0.1'
PORT=12000

moviesList = None
serverApp = flask.Flask(__name__)
serverApp.secret_key = os.urandom(24)
serverApp.debug = True

@serverApp.route('/')
def show_index():
    return flask.render_template('index.html', movies = moviesList)

@serverApp.route('/search/<string:field>/<string:token>', methods = ['GET'])
def show_search(field, token):
    resultList = []
    for movie in moviesList:
        if movie[field] == token:
            resultList.append(movie)
    
    return flask.render_template('index.html', movies = resultList)

@serverApp.route('/genre')
def show_genre():
    stats = {}
    genre = []
    allGenre = []

    for movie in moviesList:
        for genre in movie['Genre']:
            allGenre.append(genre)
        genre = list(set(allGenre))

    for i in xrange(len(genre)):
        genre[i] = (genre[i], allGenre.count(genre[i]))

    return flask.render_template('2_colum_table.html', data = genre)

@serverApp.route('/director')
def show_director():
    stats = {}
    director = []
    allDirector = []

    for movie in moviesList:
        for director in movie['Director']:
            allDirector.append(director)
        director = list(set(allDirector))

    for i in xrange(len(director)):
        director[i] = (director[i], allDirector.count(director[i]))

    return flask.render_template('2_colum_table.html', data = director)

@serverApp.route('/actor')
def show_actor():
    stats = {}
    actor = []
    allActor = []

    for movie in moviesList:
        for actor in movie['Actor']:
            allActor.append(actor)
        actor = list(set(allActor))

    for i in xrange(len(actor)):
        actor[i] = (actor[i], allActor.count(actor[i]))

    return flask.render_template('2_colum_table.html', data = actor)

@serverApp.route('/statistics')
def show_statistics():
    stats = {}
    stats['movieCount'] = len(moviesList)

    media = []
    allMedia = []
    for movie in moviesList:
        for medium in movie['Medium']:
            allMedia.append(medium)
        media = list(set(allMedia))

    for i in xrange(len(media)):
        media[i] = (media[i], allMedia.count(media[i]))

    stats['dtest'] = [('test', 'ok')]

    stats['media'] = media
    stats['numMedia'] = len(media)

    return flask.render_template('statistics.html', statsData = stats)

@serverApp.route('/movie/<int:movieId>', methods = ['GET'])
def movie_detail(movieId):
    movieData = moviesList[movieId]
    # try:
    return flask.render_template('movie_details.html', movie = movieData)
    # except 
    flask.abort(404)

@serverApp.route('/images/<int:movieId>', methods = ['GET'])
def get_cover(movieId):
    cover = moviesList[movieId]['Cover']
    if cover:
        return flask.send_from_directory('output', cover)
    else:
        flask.abort(404)

@serverApp.route('/static/<string:folderName>/<string:fileName>', methods = ['GET'])
def get_static(fileName, folderName):
    if fileName:
        return flask.send_from_directory('static/' + folderName, fileName)
    else:
        flask.abort(404)

if __name__ == '__main__':

    if not moviesList:
        output_dir = "output/"
        xml_file_path = process_zip('movies.zip', output_dir)
        moviesList = process_xml('output/export.xml')

        if moviesList:
            for movieData in moviesList:
                movieData['Directortring'] = ', '.join(movieData['Director'])
                movieData['Actortring'] = ', '.join(movieData['Actor'])
                movieData['MediaString'] = ', '.join(movieData['Medium'])
                movieData['Genretring'] = ', '.join(movieData['Genre'])
                movieData['index'] = moviesList.index(movieData)

            print "Loaded %s movies" % len(moviesList)
            # print moviesList

            # go into endless loop
            # serverApp.run(host='0.0.0.0')
            serverApp.run(host=HOST, port=PORT)
            # process = Process(target=serverApp.run(host='0.0.0.0'))

        else:
            print "unrecoverable errors found. exiting!"