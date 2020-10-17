import re
from flask import Blueprint,jsonify, render_template
from flask_cors import cross_origin
from FreeNetflix.creds import db
bp = Blueprint("bp",__name__)

# ------------------------SEARCH ROUTES----------------------------------
@bp.route('/search/<film>', methods=['GET'])
def search(film):
    genre_list = ['Horror','EnglishSeries','HindiSeries','Romantic','Scifi','Action','others']
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


@bp.route('/api/search/<film>', methods=['GET'])
@cross_origin()
def apisearch(film):
    genre_list = ['Horror','EnglishSeries','HindiSeries','Romantic','Scifi','Action','others']
    output = []
    for genre in genre_list:
        genre = db[genre]
        data = genre.find_one({'title' : re.compile(film, re.IGNORECASE)})  # case insensitive matching
        if data:
            if data["isSeries"] == True:
                series_data = {
                    "unique" : data["unique"],
                    "tmdb_id" : data["tmdb_id"],
                    "poster_path" : data["poster_path"],
                    "backdrop_path" : data["backdrop_path"],
                    "title" : data["title"],
                    "overview" : data["overview"],
                    "vote_average" : data["vote_average"],
                    "release_date" : data["release_date"],
                    "season_collection" : data["season_collection"],
                    "isSeries" : True,
                    "views" : data["views"]
                }
                output.append(series_data)
            elif data["isSeries"] == False:
                movies_data = {
                    "unique" : data["unique"],
                    "tmdb_id" : data["tmdb_id"],
                    "poster_path" : data["poster_path"],
                    "backdrop_path" : data["backdrop_path"],
                    "title" : data["title"],
                    "overview" : data["overview"],
                    "mega_link" : data["mega_link"],
                    "vote_average" : data["vote_average"],
                    "release_date" : data["release_date"],
                    "isSeries" : False,
                    "views" : data["views"]
                }
                output.append(movies_data)
            return jsonify({'status' : 200,'result' : output})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})
# ------------------------SEARCH ROUTES END----------------------------------

# ------------------------INFORMATION ROUTES---------------------------------

@bp.route("/api/horror/all", methods=['GET'])   # ALL FILM IN HORROR
@cross_origin()
def get_horror_all():
    response = db.Horror.find()
    output = []
    if response:
        for data in response:
            if data["isSeries"] == True:
                series_data = {
                    "unique" : data["unique"],
                    "tmdb_id" : data["tmdb_id"],
                    "poster_path" : data["poster_path"],
                    "backdrop_path" : data["backdrop_path"],
                    "title" : data["title"],
                    "overview" : data["overview"],
                    "vote_average" : data["vote_average"],
                    "release_date" : data["release_date"],
                    "season_collection" : data["season_collection"],
                    "isSeries" : True,
                    "views" : data["views"]
                }
                output.append(series_data)
            elif data["isSeries"] == False:
                movies_data = {
                    "unique" : data["unique"],
                    "tmdb_id" : data["tmdb_id"],
                    "poster_path" : data["poster_path"],
                    "backdrop_path" : data["backdrop_path"],
                    "title" : data["title"],
                    "overview" : data["overview"],
                    "mega_link" : data["mega_link"],
                    "vote_average" : data["vote_average"],
                    "release_date" : data["release_date"],
                    "isSeries" : False,
                    "views" : data["views"]
                }
                output.append(movies_data)
        return jsonify({'status' : 200,'result' : output})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})


@bp.route("/api/horror/<film>", methods=['GET'])    # SPECIFIC FILM IN HORROR
@cross_origin()
def get_horror(film):
    data = db.Horror.find_one({'title' : re.compile(film, re.IGNORECASE)})
    if data:
        if data["isSeries"] == True:
            series_data = {
                "unique" : data["unique"],
                "tmdb_id" : data["tmdb_id"],
                "poster_path" : data["poster_path"],
                "backdrop_path" : data["backdrop_path"],
                "title" : data["title"],
                "overview" : data["overview"],
                "vote_average" : data["vote_average"],
                "release_date" : data["release_date"],
                "season_collection" : data["season_collection"],
                "isSeries" : True,
                "views" : data["views"]
            }
            return jsonify({'status' : 200,'result' : series_data})
        elif data["isSeries"] == False:
            movies_data = {
                "unique" : data["unique"],
                "tmdb_id" : data["tmdb_id"],
                "poster_path" : data["poster_path"],
                "backdrop_path" : data["backdrop_path"],
                "title" : data["title"],
                "overview" : data["overview"],
                "mega_link" : data["mega_link"],
                "vote_average" : data["vote_average"],
                "release_date" : data["release_date"],
                "isSeries" : False,
                "views" : data["views"]
            }
            return jsonify({'status' : 200,'result' : movies_data})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})


@bp.route("/api/scifi/all", methods=['GET'])   # ALL FILM IN HORROR
@cross_origin()
def get_scifi_all():
    response = db.Scifi.find()
    output = []
    if response:
        for data in response:
            if data["isSeries"] == True:
                series_data = {
                    "unique" : data["unique"],
                    "tmdb_id" : data["tmdb_id"],
                    "poster_path" : data["poster_path"],
                    "backdrop_path" : data["backdrop_path"],
                    "title" : data["title"],
                    "overview" : data["overview"],
                    "vote_average" : data["vote_average"],
                    "release_date" : data["release_date"],
                    "season_collection" : data["season_collection"],
                    "isSeries" : True,
                    "views" : data["views"]
                }
                output.append(series_data)
            elif data["isSeries"] == False:
                movies_data = {
                    "unique" : data["unique"],
                    "tmdb_id" : data["tmdb_id"],
                    "poster_path" : data["poster_path"],
                    "backdrop_path" : data["backdrop_path"],
                    "title" : data["title"],
                    "overview" : data["overview"],
                    "mega_link" : data["mega_link"],
                    "vote_average" : data["vote_average"],
                    "release_date" : data["release_date"],
                    "isSeries" : False,
                    "views" : data["views"]
                }
                output.append(movies_data)
        return jsonify({'status' : 200,'result' : output})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})


@bp.route("/api/Scifi/<film>", methods=['GET'])    # SPECIFIC FILM IN HORROR
@cross_origin()
def get_scifi(film):
    data = db.Scifi.find_one({'title' : re.compile(film, re.IGNORECASE)})
    if data:
        if data["isSeries"] == True:
            series_data = {
                "unique" : data["unique"],
                "tmdb_id" : data["tmdb_id"],
                "poster_path" : data["poster_path"],
                "backdrop_path" : data["backdrop_path"],
                "title" : data["title"],
                "overview" : data["overview"],
                "vote_average" : data["vote_average"],
                "release_date" : data["release_date"],
                "season_collection" : data["season_collection"],
                "isSeries" : True,
                "views" : data["views"]
            }
            return jsonify({'status' : 200,'result' : series_data})
        elif data["isSeries"] == False:
            movies_data = {
                "unique" : data["unique"],
                "tmdb_id" : data["tmdb_id"],
                "poster_path" : data["poster_path"],
                "backdrop_path" : data["backdrop_path"],
                "title" : data["title"],
                "overview" : data["overview"],
                "mega_link" : data["mega_link"],
                "vote_average" : data["vote_average"],
                "release_date" : data["release_date"],
                "isSeries" : False,
                "views" : data["views"]
            }
            return jsonify({'status' : 200,'result' : movies_data})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})


@bp.route("/api/Romantic/all", methods=['GET'])   # ALL FILM IN HORROR
@cross_origin()
def get_romantic_all():
    response = db.Romantic.find()
    output = []
    if response:
        for data in response:
            if data["isSeries"] == True:
                series_data = {
                    "unique" : data["unique"],
                    "tmdb_id" : data["tmdb_id"],
                    "poster_path" : data["poster_path"],
                    "backdrop_path" : data["backdrop_path"],
                    "title" : data["title"],
                    "overview" : data["overview"],
                    "vote_average" : data["vote_average"],
                    "release_date" : data["release_date"],
                    "season_collection" : data["season_collection"],
                    "isSeries" : True,
                    "views" : data["views"]
                }
                output.append(series_data)
            elif data["isSeries"] == False:
                movies_data = {
                    "unique" : data["unique"],
                    "tmdb_id" : data["tmdb_id"],
                    "poster_path" : data["poster_path"],
                    "backdrop_path" : data["backdrop_path"],
                    "title" : data["title"],
                    "overview" : data["overview"],
                    "mega_link" : data["mega_link"],
                    "vote_average" : data["vote_average"],
                    "release_date" : data["release_date"],
                    "isSeries" : False,
                    "views" : data["views"]
                }
                output.append(movies_data)
        return jsonify({'status' : 200,'result' : output})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})


@bp.route("/api/romantic/<film>", methods=['GET'])    # SPECIFIC FILM IN HORROR
@cross_origin()
def get_romantic(film):
    data = db.Romantic.find_one({'title' : re.compile(film, re.IGNORECASE)})
    if data:
        if data["isSeries"] == True:
            series_data = {
                "unique" : data["unique"],
                "tmdb_id" : data["tmdb_id"],
                "poster_path" : data["poster_path"],
                "backdrop_path" : data["backdrop_path"],
                "title" : data["title"],
                "overview" : data["overview"],
                "vote_average" : data["vote_average"],
                "release_date" : data["release_date"],
                "season_collection" : data["season_collection"],
                "isSeries" : True,
                "views" : data["views"]
            }
            return jsonify({'status' : 200,'result' : series_data})
        elif data["isSeries"] == False:
            movies_data = {
                "unique" : data["unique"],
                "tmdb_id" : data["tmdb_id"],
                "poster_path" : data["poster_path"],
                "backdrop_path" : data["backdrop_path"],
                "title" : data["title"],
                "overview" : data["overview"],
                "mega_link" : data["mega_link"],
                "vote_average" : data["vote_average"],
                "release_date" : data["release_date"],
                "isSeries" : False,
                "views" : data["views"]
            }
            return jsonify({'status' : 200,'result' : movies_data})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})


@bp.route("/api/action/all", methods=['GET'])   # ALL FILM IN HORROR
@cross_origin()
def get_action_all():
    response = db.Action.find()
    output = []
    if response:
        for data in response:
            if data["isSeries"] == True:
                series_data = {
                    "unique" : data["unique"],
                    "tmdb_id" : data["tmdb_id"],
                    "poster_path" : data["poster_path"],
                    "backdrop_path" : data["backdrop_path"],
                    "title" : data["title"],
                    "overview" : data["overview"],
                    "vote_average" : data["vote_average"],
                    "release_date" : data["release_date"],
                    "season_collection" : data["season_collection"],
                    "isSeries" : True,
                    "views" : data["views"]
                }
                output.append(series_data)
            elif data["isSeries"] == False:
                movies_data = {
                    "unique" : data["unique"],
                    "tmdb_id" : data["tmdb_id"],
                    "poster_path" : data["poster_path"],
                    "backdrop_path" : data["backdrop_path"],
                    "title" : data["title"],
                    "overview" : data["overview"],
                    "mega_link" : data["mega_link"],
                    "vote_average" : data["vote_average"],
                    "release_date" : data["release_date"],
                    "isSeries" : False,
                    "views" : data["views"]
                }
                output.append(movies_data)
        return jsonify({'status' : 200,'result' : output})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})


@bp.route("/api/action/<film>", methods=['GET'])    # SPECIFIC FILM IN HORROR
@cross_origin()
def get_action(film):
    data = db.Action.find_one({'title' : re.compile(film, re.IGNORECASE)})
    if data:
        if data["isSeries"] == True:
            series_data = {
                "unique" : data["unique"],
                "tmdb_id" : data["tmdb_id"],
                "poster_path" : data["poster_path"],
                "backdrop_path" : data["backdrop_path"],
                "title" : data["title"],
                "overview" : data["overview"],
                "vote_average" : data["vote_average"],
                "release_date" : data["release_date"],
                "season_collection" : data["season_collection"],
                "isSeries" : True,
                "views" : data["views"]
            }
            return jsonify({'status' : 200,'result' : series_data})
        elif data["isSeries"] == False:
            movies_data = {
                "unique" : data["unique"],
                "tmdb_id" : data["tmdb_id"],
                "poster_path" : data["poster_path"],
                "backdrop_path" : data["backdrop_path"],
                "title" : data["title"],
                "overview" : data["overview"],
                "mega_link" : data["mega_link"],
                "vote_average" : data["vote_average"],
                "release_date" : data["release_date"],
                "isSeries" : False,
                "views" : data["views"]
            }
            return jsonify({'status' : 200,'result' : movies_data})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})


@bp.route("/api/others/all", methods=['GET'])   # ALL FILM IN HORROR
@cross_origin()
def get_others_all():
    response = db.others.find()
    output = []
    if response:
        for data in response:
            if data["isSeries"] == True:
                series_data = {
                    "unique" : data["unique"],
                    "tmdb_id" : data["tmdb_id"],
                    "poster_path" : data["poster_path"],
                    "backdrop_path" : data["backdrop_path"],
                    "title" : data["title"],
                    "overview" : data["overview"],
                    "vote_average" : data["vote_average"],
                    "release_date" : data["release_date"],
                    "season_collection" : data["season_collection"],
                    "isSeries" : True,
                    "views" : data["views"]
                }
                output.append(series_data)
            elif data["isSeries"] == False:
                movies_data = {
                    "unique" : data["unique"],
                    "tmdb_id" : data["tmdb_id"],
                    "poster_path" : data["poster_path"],
                    "backdrop_path" : data["backdrop_path"],
                    "title" : data["title"],
                    "overview" : data["overview"],
                    "mega_link" : data["mega_link"],
                    "vote_average" : data["vote_average"],
                    "release_date" : data["release_date"],
                    "isSeries" : False,
                    "views" : data["views"]
                }
                output.append(movies_data)
        return jsonify({'status' : 200,'result' : output})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})


@bp.route("/api/others/<film>", methods=['GET'])    # SPECIFIC FILM IN HORROR
@cross_origin()
def get_others(film):
    data = db.others.find_one({'title' : re.compile(film, re.IGNORECASE)})
    if data:
        if data["isSeries"] == True:
            series_data = {
                "unique" : data["unique"],
                "tmdb_id" : data["tmdb_id"],
                "poster_path" : data["poster_path"],
                "backdrop_path" : data["backdrop_path"],
                "title" : data["title"],
                "overview" : data["overview"],
                "vote_average" : data["vote_average"],
                "release_date" : data["release_date"],
                "season_collection" : data["season_collection"],
                "isSeries" : True,
                "views" : data["views"]
            }
            return jsonify({'status' : 200,'result' : series_data})
        elif data["isSeries"] == False:
            movies_data = {
                "unique" : data["unique"],
                "tmdb_id" : data["tmdb_id"],
                "poster_path" : data["poster_path"],
                "backdrop_path" : data["backdrop_path"],
                "title" : data["title"],
                "overview" : data["overview"],
                "mega_link" : data["mega_link"],
                "vote_average" : data["vote_average"],
                "release_date" : data["release_date"],
                "isSeries" : False,
                "views" : data["views"]
            }
            return jsonify({'status' : 200,'result' : movies_data})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})


@bp.route("/api/english/series/all", methods=['GET'])   # ALL ENGLISH SERIES
@cross_origin()
def get_english_series_all():
    response = db.EnglishSeries.find()
    output = []
    if response:
        for data in response:
            series_data = {
                "unique" : data["unique"],
                "tmdb_id" : data["tmdb_id"],
                "poster_path" : data["poster_path"],
                "backdrop_path" : data["backdrop_path"],
                "title" : data["title"],
                "overview" : data["overview"],
                "vote_average" : data["vote_average"],
                "release_date" : data["release_date"],
                "season_collection" : data["season_collection"],
                "isSeries" : True,
                "views" : data["views"]
            }
            output.append(series_data)
        return jsonify({'status' : 200,'result' : output})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})


@bp.route("/api/english/series/<film>", methods=['GET'])    # SPECIFIC ENGLISH SERIES
@cross_origin()
def get_english_series(film):
    data = db.EnglishSeries.find_one({'title' : re.compile(film, re.IGNORECASE)})
    if data:
        series_data = {
            "unique" : data["unique"],
            "tmdb_id" : data["tmdb_id"],
            "poster_path" : data["poster_path"],
            "backdrop_path" : data["backdrop_path"],
            "title" : data["title"],
            "overview" : data["overview"],
            "vote_average" : data["vote_average"],
            "release_date" : data["release_date"],
            "season_collection" : data["season_collection"],
            "isSeries" : True,
            "views" : data["views"]
        }
        return jsonify({'status' : 200,'result' : series_data})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})


@bp.route("/api/hindi/series/all", methods=['GET'])   # ALL HINDI SERIES
@cross_origin()
def get_hindi_series_all():
    response = db.HindiSeries.find()
    output = []
    if response:
        for data in response:
            series_data = {
                "unique" : data["unique"],
                "tmdb_id" : data["tmdb_id"],
                "poster_path" : data["poster_path"],
                "backdrop_path" : data["backdrop_path"],
                "title" : data["title"],
                "overview" : data["overview"],
                "vote_average" : data["vote_average"],
                "release_date" : data["release_date"],
                "season_collection" : data["season_collection"],
                "isSeries" : True,
                "views" : data["views"]
            }
            output.append(series_data)
        return jsonify({'status' : 200,'result' : output})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})


@bp.route("/api/hindi/series/<film>", methods=['GET'])    # SPECIFIC HINDI SERIES
@cross_origin()
def get_hindi_series(film):
    data = db.HindiSeries.find_one({'title' : re.compile(film, re.IGNORECASE)})
    if data:
        series_data = {
            "unique" : data["unique"],
            "tmdb_id" : data["tmdb_id"],
            "poster_path" : data["poster_path"],
            "backdrop_path" : data["backdrop_path"],
            "title" : data["title"],
            "overview" : data["overview"],
            "vote_average" : data["vote_average"],
            "release_date" : data["release_date"],
            "season_collection" : data["season_collection"],
            "isSeries" : True,
            "views" : data["views"]
        }
        return jsonify({'status' : 200,'result' : series_data})
    return jsonify({'status' : 404, 'message' : 'Movie/Series not found'})

# ------------------------INFORMATION ROUTES END-----------------------------