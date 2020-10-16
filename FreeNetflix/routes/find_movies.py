from FreeNetflix.creds import db
class operations:
    def find_movies(self,movie,genre):
        genre = db[genre]
        data = db.genre.find_one({'title' : movie})
        if data:
            return data
        else:
            return False