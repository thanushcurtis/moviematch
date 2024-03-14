
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://thanushcurtis:RA7ZX0SPl7b3lLC1@cluster0.zaick22.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))

# Select your database
db = client["moviematch"]

genre_id = 28

# Perform the aggregation
pipeline = [
    {"$unwind": "$genres"},
    {"$match": {"genres.id": genre_id}},
    {"$project": {"_id": 0, "genre_name": "$genres.name"}}
]

result = db["genres"].aggregate(pipeline)

# Extracting the genre name from the result
for doc in result:
    print("Genre Name:", doc.get("genre_name"))

# Close the connection
client.close()


# Extracting the genre name from the result
for doc in result:
    print("Genre Name:", doc.get("genre_name"))