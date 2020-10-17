from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://admin:nydqqzuy1324@cluster0.ufhv8.mongodb.net/")
db = cluster['FreeNetflix']