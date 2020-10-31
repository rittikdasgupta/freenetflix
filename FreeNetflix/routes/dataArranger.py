class Formatter(object):

    @staticmethod
    def DataFormatter(data):
        if data["isSeries"] == True:
            series_data = {
                "unique" : data["unique"],
                "tmdb_id" : data["tmdb_id"],
                "poster_path" : data["poster_path"],
                "backdrop_path" : data["backdrop_path"],
                "title" : data["title"],
                "overview" : data["overview"],
                "release_date" : data["release_date"],
                "Year" : data["Year"],
                "Director" : data["Director"],
                "Actors" : data["Actors"],
                "Genre" : data["Genre"],
                "Language" : data["Language"],
                "imdbRating" : data["imdbRating"],
                "Metascore" : data["Metascore"],
                "season_collection" : data["season_collection"],
                "isSeries" : True,
                "views" : data["views"]
            }
            return series_data

        elif data["isSeries"] == False:
            movies_data = {
                "unique" : data["unique"],
                "tmdb_id" : data["tmdb_id"],
                "poster_path" : data["poster_path"],
                "backdrop_path" : data["backdrop_path"],
                "title" : data["title"],
                "overview" : data["overview"],
                "mega_link" : data["mega_link"],
                "Year" : data["Year"],
                "Director" : data["Director"],
                "Actors" : data["Actors"],
                "Genre" : data["Genre"],
                "Language" : data["Language"],
                "imdbRating" : data["imdbRating"],
                "Metascore" : data["Metascore"],
                "Runtime" : data["Runtime"],
                "isSeries" : False,
                "views" : data["views"]
            }
            return movies_data
    
    @staticmethod
    def EpisodeFormatter(data):
        if data:
            episode_data = {
                "unique" : data['unique'],
                "episode_id" : data['episode_id'],
                "episode_title" : data['episode_title'],
                "episode_overview" : data['episode_overview'],
                "still_path" : data['still_path'],
                "air_date" : data['air_date'],
                "mega_link" : data['mega_link'],
                "series" : data['series']
            }
            return episode_data
            