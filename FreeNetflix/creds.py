from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://adminnfx:nydqqzuy1324@cluster0.fglir.mongodb.net/?retryWrites=true&w=majority")
db = cluster['FreeNetflix']
