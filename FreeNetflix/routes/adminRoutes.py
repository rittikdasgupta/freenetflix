import requests
import uuid
import re
import re  # for case insensitive matching in mongodb
from flask import Flask, Blueprint,render_template, request, flash, jsonify, url_for, redirect
from FreeNetflix.creds import db
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
        season_name = "Season " + season
        season_selector = int(season) - 1
        grab_series = genre.find_one({"title" : re.compile(series, re.IGNORECASE)})
        if grab_series:
            seasons = grab_series["season_collection"]
            for i in seasons:        #IF SEASON PRESENT
                if season_name == i["season_name"]:  
                    for j in i["episodes"]:
                        if episode == j["episode_number"]:
                            episode_num = int(episode) - 1
                            flash("Episode already present updating mega link", 'success')
                            status = genre.update_one(
                                {"title" : re.compile(series, re.IGNORECASE)},
                                {"$set" : 
                                    {
                                        "season_collection.{0}.episodes.{1}.mega_link".format(season_selector,episode_num) :
                                        mega_link
                                    }
                                }
                            )
                            flash("Updated mega link", 'success')
                            return redirect(url_for('admin.index'))
                        else:
                            response = requests.get("https://api.themoviedb.org/3/tv/{0}/season/{1}/episode/{2}?api_key=9b62ac1eafaa86d7ad48e61ebb6dcb5b&language=en-US".format(grab_series["tmdb_id"],season,episode))
                            if response.status_code == 200:
                                response = response.json()
                                still_path = ''
                                if response["still_path"] is not None:
                                    still_path = "https://image.tmdb.org/t/p/original" + response["still_path"]
                                else:
                                    still_path = grab_series["backdrop_path"]
                                status = genre.update_one(
                                    {
                                        "title" : series,
                                    },
                                    {"$push" :
                                        {"season_collection.{}.episodes".format(season_selector) :  
                                            {
                                                "unique" : str(uuid.uuid4()),
                                                "episode_id" : response["id"],
                                                "episode_number" : episode,
                                                "episode_title" : response["name"],
                                                "episode_overview" : response["overview"],
                                                "still_path" : still_path,
                                                "air_date" : response["air_date"],
                                                "mega_link" : mega_link,
                                                "series" : series 
                                            } 
                                        
                                        }
                                    }
                                )
                                if status:
                                    flash("Episode added successfully", 'success')
                                    return redirect(url_for('admin.index'))
            
            response = requests.get("https://api.themoviedb.org/3/tv/{0}/season/{1}/episode/{2}?api_key=9b62ac1eafaa86d7ad48e61ebb6dcb5b&language=en-US".format(grab_series["tmdb_id"],season,episode))
            if response.status_code == 200:
                response = response.json()
                still_path = ''
                if response["still_path"] is not None:
                    still_path = "https://image.tmdb.org/t/p/original" + response["still_path"]
                else:
                    still_path = grab_series["backdrop_path"]
                status = genre.update_one(
                    {"title" :  re.compile(series, re.IGNORECASE)
                    },
                    {   "$push" : 
                        {   "season_collection" : 
                            {   "season_name" : season_name,
                                "episodes" : [
                                    {
                                        "unique" : str(uuid.uuid4()),
                                        "episode_id" : response["id"],
                                        "episode_title" : response["name"],
                                        "episode_number" : episode,
                                        "episode_overview" : response["overview"],
                                        "still_path" : still_path,
                                        "air_date" : response["air_date"],
                                        "mega_link" : mega_link,
                                        "series" : series  }
                                ]
                            }
                        }
                    }
                )
                if status:
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
    genre = db[genre]
    check_movie = genre.find_one({"title" : re.compile(movie, re.IGNORECASE)})
    if check_movie :
        status = genre.update_one(
            {"title" : re.compile(movie, re.IGNORECASE)},
            {"$set" : {
                "mega_link" : mega
            }}
            )
        if status:
            flash("Movie added successfully", 'success')
            return redirect(url_for('admin.movie'))
    else:
        response = requests.get("https://api.themoviedb.org/3/search/movie?api_key=9b62ac1eafaa86d7ad48e61ebb6dcb5b&language=en-US&query={}&page=1&include_adult=false".format(movie))
        omdb_response = requests.get("http://www.omdbapi.com/?i=tt3896198&apikey=3ae3134c&t={}".format(movie))
        if response.status_code == 200 and omdb_response.status_code == 200:
            response = response.json()
            omdb_response = omdb_response.json()
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