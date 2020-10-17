import requests
import uuid
import re  # for case insensitive matching in mongodb
from flask import Flask, Blueprint,render_template, request, flash, jsonify, url_for, redirect
from FreeNetflix.creds import db
from .find_movies import operations
admin = Blueprint("admin",__name__)

@admin.route("/", methods=['GET'])
def index():
    return render_template("index.html",)

# ----------------------------------SERIES ROUTES-------------------------------
@admin.route("/series", methods=['POST'])
def addSeries():
    if request.method == 'POST':
        genre = request.form.get("category")
        series = request.form.get("Series")
        genre = db[genre]
        isSeries = genre.find_one({"title" : series})
        if isSeries:
            flash("Series already present", 'error')
            return redirect(url_for('admin.index'))
        else:
            response = requests.get("https://api.themoviedb.org/3/search/tv?api_key=9b62ac1eafaa86d7ad48e61ebb6dcb5b&language=en-US&page=1&query={}&include_adult=false".format(series)).json()
            results = response['results'][0]
            poster = "https://image.tmdb.org/t/p/w500" + results["poster_path"]
            backdrop = "https://image.tmdb.org/t/p/w500" + results["backdrop_path"]
            status = genre.insert_one({
                "unique" : str(uuid.uuid4()),
                "tmdb_id" : results["id"],
                "poster_path" : poster,
                "backdrop_path" : backdrop,
                "title" : results["name"],
                "overview" : results["overview"],
                "vote_average" : results['vote_average'],
                "release_date" : results["first_air_date"],
                "season_collection" : [],
                "isSeries" : True,
                "views" : 0
            })
            if status:
                flash('Series added successfully', 'success')
                return redirect(url_for('admin.index'))

@admin.route("/episode", methods=['POST'])
def addEpisode():
    if request.method == 'POST':
        genre = request.form.get('category')
        series = request.form.get('series')
        season = request.form.get('season')
        title = request.form.get('title')
        mega_link = request.form.get('mega_link')
        genre = db[genre]
        collection = series + " " + season
        check_collection = db.collection_names()
        isColPresent = False
        for col in check_collection:
            if col == collection:
                isColPresent = True
                col = db[collection]
                status = col.insert_one({
                    "unique" : str(uuid.uuid4()),
                    "episode" : title,
                    "mega_link" : mega_link,
                    "series" : series  
                })
                if status:
                    flash("Episode added successfully", 'success')
                return redirect(url_for('admin.index'))
        if isColPresent == False:
            find_series = genre.find_one({'title' : series})
            if find_series:
                col = db[collection]
                status = col.insert_one({
                    "unique" : str(uuid.uuid4()),
                    "episode" : title,
                    "mega_link" : mega_link,
                    "series" : series  
                })
                if status:
                    update_status = genre.update_one(
                        {
                            "title" : series
                        },
                        {
                            "$push" : {
                                "season_collection" : collection
                            }
                        }
                    )
                    if update_status:
                        flash('Episode added successfully', 'success')
                        return redirect(url_for('admin.index'))
            flash('Series not present','error')
            return redirect(url_for('admin.index'))            
# ------------------------SERIES ROUTES END----------------------------------


# ------------------------SEARCH ROUTES----------------------------------
@admin.route('/search/<film>', methods=['GET'])
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

@admin.route('/api/search/<film>', methods=['GET'])
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


# ------------------------MOVIES ROUTES--------------------------------------
@admin.route('/movie',methods=['GET'])
def movie():
    return render_template('moviepage.html')

@admin.route('/addmovies', methods=['POST'])
def add_movies():
    genre = request.form.get("category")
    movie = request.form.get("movie")
    mega = request.form.get("mega")
    response = requests.get("https://api.themoviedb.org/3/search/movie?api_key=9b62ac1eafaa86d7ad48e61ebb6dcb5b&language=en-US&query={}&page=1&include_adult=false".format(movie)).json()
    if response:
        genre = db[genre]
        results = response['results'][0]
        poster = "https://image.tmdb.org/t/p/w500" + results["poster_path"]
        backdrop = "https://image.tmdb.org/t/p/w500" + results["backdrop_path"]
        status = genre.insert_one({
            "unique" : str(uuid.uuid4()),
            "tmdb_id" : results["id"],
            "poster_path" : poster,
            "backdrop_path" : backdrop,
            "title" : results["title"],
            "overview" : results["overview"],
            "mega_link" : mega,
            "vote_average" : results['vote_average'],
            "release_date" : results["release_date"],
            "isSeries" : False,
            "views" : 0
        })
        if status:
            flash("Movie added successfully", 'success')
            return redirect(url_for('admin.movie'))

# ------------------------MOVIES ROUTES END----------------------------------