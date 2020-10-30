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
            omdb_response = requests.get("http://www.omdbapi.com/?i=tt3896198&apikey=3ae3134c&t={}".format(series))
            if response["results"] != [] and omdb_response.status_code == 200:
                results = response['results'][0]
                omdb_response = omdb_response.json()
                poster = "https://image.tmdb.org/t/p/original" + results["poster_path"]
                backdrop = "https://image.tmdb.org/t/p/original" + results["backdrop_path"]
                status = genre.insert_one({
                    "unique" : str(uuid.uuid4()),
                    "tmdb_id" : results["id"],
                    "poster_path" : poster,
                    "backdrop_path" : backdrop,
                    "title" : results["name"],
                    "overview" : results["overview"],
                    "release_date" : results["first_air_date"],
                    "Year" : omdb_response["Year"],
                    "Director" : omdb_response["Director"],
                    "Actors" : omdb_response["Actors"],
                    "Genre" : omdb_response["Genre"],
                    "Language" : omdb_response["Language"],
                    "imdbRating" : omdb_response["imdbRating"],
                    "Metascore" : omdb_response["Metascore"],
                    "season_collection" : [],
                    "isSeries" : True,
                    "views" : 0
                })
                if status:
                    flash('Series added successfully', 'success')
                    return redirect(url_for('admin.index'))
            flash('Series cannot be found', 'error')
            return redirect(url_for('admin.index'))

@admin.route("/episode", methods=['POST'])
def addEpisode():
    if request.method == 'POST':
        genre = request.form.get('category')
        series = request.form.get('series')
        season = request.form.get('season')
        episode = request.form.get('episode')
        mega_link = request.form.get('mega_link')
        genre = db[genre]
        season_name = series + " Season " + season
        grab_series = genre.find_one({"title" : series})
        if grab_series:
            seasons = grab_series["season_collection"]
            if season_name in seasons:
                response = requests.get("https://api.themoviedb.org/3/tv/{0}/season/{1}/episode/{2}?api_key=9b62ac1eafaa86d7ad48e61ebb6dcb5b&language=en-US".format(grab_series["tmdb_id"],season,episode))
                if response.status_code == 200:
                    response = response.json()
                    still_path = "https://image.tmdb.org/t/p/original" + response["still_path"]
                    status = db[season_name].insert_one({
                        "unique" : str(uuid.uuid4()),
                        "episode_id" : response["id"],
                        "episode_title" : response["name"],
                        "episode_overview" : response["overview"],
                        "still_path" : still_path,
                        "air_date" : response["air_date"],
                        "mega_link" : mega_link,
                        "series" : series  
                    })
                    if status:
                        flash("Episode added successfully", 'success')
                        return redirect(url_for('admin.index'))
                flash("Invalid Season or Episode", 'error')
                return redirect(url_for('admin.index'))
            else:
                seasons.append(season_name)
                seasons.sort()
                status = genre.update_one(
                        {
                            "title" : series
                        },
                        {
                            "$set" : {
                                "season_collection" : seasons
                            }
                        })
                season_col =db[season_name]
                response = requests.get("https://api.themoviedb.org/3/tv/{0}/season/{1}/episode/{2}?api_key=9b62ac1eafaa86d7ad48e61ebb6dcb5b&language=en-US".format(grab_series["tmdb_id"],season,episode))
                if response.status_code == 200:
                    response = response.json()
                    still_path = "https://image.tmdb.org/t/p/original" + response["still_path"]
                    status2 = season_col.insert_one({
                        "unique" : str(uuid.uuid4()),
                        "episode_id" : response["id"],
                        "episode_title" : response["name"],
                        "episode_overview" : response["overview"],
                        "still_path" : still_path,
                        "air_date" : response["air_date"],
                        "mega_link" : mega_link,
                        "series" : series  
                    })
                    if status and status2:
                        flash("Episode added successfully", 'success')
                        return redirect(url_for('admin.index'))
                flash("Invalid Season or Episode", 'error')
                return redirect(url_for('admin.index'))
        flash('Series not present','error')
        return redirect(url_for('admin.index'))    
 
# ------------------------SERIES ROUTES END----------------------------------


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
    omdb_response = requests.get("http://www.omdbapi.com/?i=tt3896198&apikey=3ae3134c&t={}".format(movie)).json()
    if response and omdb_response:
        genre = db[genre]
        results = response['results'][0]
        poster = "https://image.tmdb.org/t/p/original" + results["poster_path"]
        backdrop = "https://image.tmdb.org/t/p/original" + results["backdrop_path"]
        status = genre.insert_one({
            "unique" : str(uuid.uuid4()),
            "tmdb_id" : results["id"],
            "poster_path" : poster,
            "backdrop_path" : backdrop,
            "title" : results["title"],
            "overview" : results["overview"],
            "mega_link" : mega,
            "Year" : omdb_response["Year"],
            "Director" : omdb_response["Director"],
            "Actors" : omdb_response["Actors"],
            "Genre" : omdb_response["Genre"],
            "Language" : omdb_response["Language"],
            "imdbRating" : omdb_response["imdbRating"],
            "Metascore" : omdb_response["Metascore"],
            "Runtime" : omdb_response["Runtime"],           
            "isSeries" : False,
            "views" : 0
        })
        if status:
            flash("Movie added successfully", 'success')
            return redirect(url_for('admin.movie'))

# ------------------------MOVIES ROUTES END----------------------------------