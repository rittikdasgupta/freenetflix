import re
from flask import Blueprint,jsonify, render_template
from FreeNetflix.creds import db
from .dataArranger import Formatter
bp = Blueprint("bp",__name__)

# ------------------------SEARCH ROUTES----------------------------------
@bp.route('/search/<film>', methods=['GET'])         #SEARCH ANY FILM/SERIES FOR POSTERS
def search(film):
    genre_list = ['Horror','series','Romantic','Scifi','Action','others']
    poster = ''
    backdrop = ''
    for genre in genre_list:
        genre = db[genre]
        data = genre.find_one({'title' : re.compile(film, re.IGNORECASE)})
        if data:
            poster = data['poster_path']
            backdrop = data['backdrop_path']
            return render_template('posterConfirm.html',poster = poster, backdrop = backdrop)
    return '<h1>Cannot Find Movie/Series</h1>'


@bp.route('/api/search/<film>', methods=['GET'])       #GET ANY FILM INFO
def apisearch(film):
    genre_list = ['Horror','series','Romantic','Scifi','Action','others']
    for genre in genre_list:
        genre = db[genre]
        response = genre.find_one({'title' : re.compile(film, re.IGNORECASE)})  # case insensitive matching
        if response:
            all_data = Formatter.DataFormatter(response)
            return jsonify({'status' : 200,'result' : all_data})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})
# ------------------------SEARCH ROUTES END----------------------------------

# ------------------------INFORMATION ROUTES---------------------------------

@bp.route("/api/horror/all/", methods=['GET'])   # ALL FILM IN HORROR
def get_horror_all():
    response = db.Horror.find()
    output = []
    if response:
        for data in response:
            all_data = Formatter.DataFormatter(data)
            output.append(all_data)
        return jsonify({'status' : 200,'result' : output})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})

@bp.route("/api/horror/10/", methods=['GET'])   # 10 FILM IN HORROR
def get_horror_ten():
    response = db.Horror.find()
    output = []
    if response:
        for data in response:
            all_data = Formatter.DataFormatter(data)
            output.append(all_data)
        return jsonify({'status' : 200,'result' : output})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})


@bp.route("/api/horror/<film>", methods=['GET'])    # SPECIFIC FILM IN HORROR
def get_horror(film):
    response = db.Horror.find_one({'title' : re.compile(film, re.IGNORECASE)})
    if response:
        all_data = Formatter.DataFormatter(response)
        return jsonify({'status' : 200,'result' : all_data})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})


@bp.route("/api/scifi/all/", methods=['GET'])   # ALL FILM IN SCI-FI
def get_scifi_all():
    response = db.Scifi.find()
    output = []
    if response:
        for data in response:
            all_data = Formatter.DataFormatter(data)
            output.append(all_data)
        return jsonify({'status' : 200,'result' : output})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})

@bp.route("/api/scifi/10/", methods=['GET'])   # 10 FILM IN SCI-FI
def get_scifi_ten():
    response = db.Scifi.find()
    output = []
    if response:
        for data in response:
            all_data = Formatter.DataFormatter(data)
            output.append(all_data)
        return jsonify({'status' : 200,'result' : output})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})

@bp.route("/api/scifi/<film>", methods=['GET'])    # SPECIFIC FILM IN SCI-FI
def get_scifi(film):
    response = db.Scifi.find_one({'title' : re.compile(film, re.IGNORECASE)})
    if response:
        all_data = Formatter.DataFormatter(response)
        return jsonify({'status' : 200,'result' : all_data})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})


@bp.route("/api/romantic/all/", methods=['GET'])   # ALL FILM IN ROMANTIC
def get_romantic_all():
    response = db.Romantic.find()
    output = []
    if response:
        for data in response:
            all_data = Formatter.DataFormatter(data)
            output.append(all_data)
        return jsonify({'status' : 200,'result' : output})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})

@bp.route("/api/romantic/10/", methods=['GET'])   # 10 FILM IN ROMANTIC
def get_romantic_ten():
    response = db.Romantic.find()
    output = []
    if response:
        for data in response:
            all_data = Formatter.DataFormatter(data)
            output.append(all_data)
        return jsonify({'status' : 200,'result' : output})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})

@bp.route("/api/romantic/<film>", methods=['GET'])    # SPECIFIC FILM IN ROMANTIC
def get_romantic(film):
    response = db.Romantic.find_one({'title' : re.compile(film, re.IGNORECASE)})
    if response:
        all_data = Formatter.DataFormatter(response)
        return jsonify({'status' : 200,'result' : all_data})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})


@bp.route("/api/action/all/", methods=['GET'])   # ALL FILM IN ACTION
def get_action_all():
    response = db.Action.find()
    output = []
    if response:
        for data in response:
            all_data = Formatter.DataFormatter(data)
            output.append(all_data)
        return jsonify({'status' : 200,'result' : output})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})

@bp.route("/api/action/10/", methods=['GET'])   # 10 FILM IN ACTION
def get_action_10():
    response = db.Action.find()
    output = []
    if response:
        for data in response:
            all_data = Formatter.DataFormatter(data)
            output.append(all_data)
        return jsonify({'status' : 200,'result' : output})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})

@bp.route("/api/action/<film>", methods=['GET'])    # SPECIFIC FILM IN ACTION
def get_action(film):
    response = db.Action.find_one({'title' : re.compile(film, re.IGNORECASE)})
    if response:
        all_data = Formatter.DataFormatter(response)
        return jsonify({'status' : 200,'result' : all_data})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})


@bp.route("/api/others/all/", methods=['GET'])   # ALL FILM IN OTHERS
def get_others_all():
    response = db.others.find()
    output = []
    if response:
        for data in response:
            all_data = Formatter.DataFormatter(data)
            output.append(all_data)
        return jsonify({'status' : 200,'result' : output})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})

@bp.route("/api/others/10/", methods=['GET'])   # 10 FILM IN OTHERS
def get_others_ten():
    response = db.others.find()
    output = []
    if response:
        for data in response:
            all_data = Formatter.DataFormatter(data)
            output.append(all_data)
        return jsonify({'status' : 200,'result' : output})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})

@bp.route("/api/others/<film>", methods=['GET'])    # SPECIFIC FILM IN OTHERS
def get_others(film):
    response = db.others.find_one({'title' : re.compile(film, re.IGNORECASE)})
    if response:
        all_data = Formatter.DataFormatter(response)
        return jsonify({'status' : 200,'result' : all_data})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})


@bp.route("/api/series/all/", methods=['GET'])   # ALL SERIES
def get_series_all():
    response = db.series.find()
    output = []
    if response:
        for data in response:
            all_data = Formatter.DataFormatter(data)
            output.append(all_data)
        return jsonify({'status' : 200,'result' : output})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})


@bp.route("/api/series/<film>", methods=['GET'])    # SPECIFIC SERIES
def get_series(film):
    response = db.series.find_one({'title' : re.compile(film, re.IGNORECASE)})
    if response:
        all_data = Formatter.DataFormatter(response)
        return jsonify({'status' : 200,'result' : all_data})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})

@bp.route("/api/episode/<series>/<season>", methods=['GET'])    # SPECIFIC EPISODE
def get_episodes(series,season):
    ep = series + " Season " + season
    ep=db[ep]
    response = ep.find()
    output = []
    if response:
        for data in response:
            all_data = Formatter.EpisodeFormatter(data)
            output.append(all_data)
        return jsonify({'status' : 200,'result' : all_data})
    return jsonify({'status' : 404, 'message' : 'Episode not found'})


# ------------------------INFORMATION ROUTES END-----------------------------