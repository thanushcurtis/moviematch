from flask import Flask, request, jsonify, session, Response,stream_with_context
from config import ApplicationConfig
import json
from werkzeug.security import check_password_hash, generate_password_hash
from flask_cors import CORS
from flask_session import Session
from flask_cors import cross_origin
import requests
import requests
import spacy
from flask_pymongo import PyMongo
from recom import MovieRecommendation
import os
from flask import send_from_directory
import subprocess






app = Flask(__name__, static_folder='frontend/build', static_url_path='')
recommender = MovieRecommendation()



app.config.from_object(ApplicationConfig)
CORS(app, origins="http://localhost:3000", supports_credentials=True,samesite=None, secure=False)
tmdb_api_key = app.config["TMDB_API_KEY"]
TMBD_ACCESS_TOKEN=app.config["TMDB_ACCESS_TOKEN"]
nlp = spacy.load("en_core_web_md")
positive_keywords = [
    "3-D", "absorbing", "acclaimed", "adult", "adventurous", "ambitious", "artistic",
    "astonishing", "avant-garde", "award-winning", "awe-inspiring", "based on", "beautiful",
    "beautifully filmed", "beautifully shot", "big-budget", "bold", "breathtaking", "brilliant",
    "captured", "cerebral", "character-driven", "charismatic", "cinematic", "coherent", "colorful",
    "comic", "compelling", "complex", "conceptual", "contemplative", "contemporary", "controversial",
    "conversational", "convincing", "creative", "critically acclaimed", "cult", "current", "daring",
    "deep", "important", "in-depth", "independent", "infused", "insightful", "inspirational", "inspired",
    "intellectual", "intellectually invigorating", "intelligent", "intense", "intensive", "interesting",
    "introspective", "intuitive", "inventive", "inventively edited", "ironic", "layered", "legendary",
    "light-hearted", "magical", "magnetic", "mature", "meaningful", "memorable", "mind-blowing", "modern",
    "moving", "must-see", "mysterious", "mystical", "narrative", "non-stop", "offbeat", "original",
    "passionate", "phenomenal", "playful", "plot-driven", "ponderous", "delightful", "dizzying", "dramatic",
    "edgy", "effective", "elevating", "eloquent", "emotional", "emotionally charged", "emotionally resonant",
    "enchanted", "engaging", "engrossing", "enigmatic", "entertaining", "epic", "evocative", "exceptional",
    "exciting", "exquisite", "extraordinary", "family-friendly", "fascinating", "fast-paced", "feel-good",
    "filmed", "filmed live", "fluid", "fresh", "fun", "funny", "futuristic", "graceful", "graphic", "gripping",
    "highly original", "historical", "honest", "humorous", "imaginative", "immensely talented",
    "potent", "powerful", "profound", "provoking", "pure", "quirky", "rated", "realistic", "recommended",
    "refined", "refreshing", "relevant", "remarkable", "resourceful", "revealing", "rich", "riveting",
    "romantic", "rousing", "sad", "sappy", "satirical", "sentimental", "sexy", "small-budget", "star-studded",
    "strong", "stunning", "superb", "suspenseful", "sweet", "theatrical", "thrilling", "touching",
    "underground", "unforgettable", "visionary", "visual", "well-paced", "worthwhile"
]

sess = Session()
sess.init_app(app)
try:
    mongo = PyMongo(app)
    app.logger.info("Connected to MongoDB")
except Exception as e:
    app.logger.error("Failed to connect to MongoDB: {}".format(str(e)), exc_info=True)


@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route("/login/", methods=["POST"])
@cross_origin(supports_credentials=True)
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user = mongo.db.users.find_one({"username": username})
    
    if user and check_password_hash(user['password'], password):
        session['username'] = username  
        session.modified = True  
        print(session['username'])
        response = jsonify({'message': 'Login successful'})
        return response, 200
    else:
        return jsonify({'message': 'Login failed! Please check your credentials.'}), 401
    
@app.route("/login_status/")
def login_status():
    user = session.get('username')
    print(user)
    if not user:
        return jsonify({'message': 'Not logged in'}), 401
    if user is not None:
        return jsonify({'username': user}), 200
    

@app.route("/user-preference/")
def user_preference():
    login_status = login_status()
    if(login_status == 401):
        return jsonify({'message': 'Not logged in'}), 401
    else:
        print("User is logged in")
    
@app.route("/get_current_user/")
def get_current_user():
    username = session.get('username')
    if not username:
        return jsonify({"error": "Unauthorized"}), 401
    
    user = mongo.db.users.find_one({"username": username})

    if user is not None:
        return jsonify({
            "username": user['username'],
            "first_name": user['name'],
        })
    else:
        return jsonify({"error": "User not found"}), 404


@app.route("/logout/")
def logout():
    session.pop("username", None)
    return jsonify({'message': 'Logout successful'}), 200 


@app.route("/register/", methods=["POST"])
def register():
    print(app.config["MONGO_URI"])  

    try:
        data = request.get_json()
        username = data.get("username")
        name = data.get("name")
        password = data.get("password")

        if not username or not name or not password:
            return jsonify({'message': 'Missing fields'}), 400
    
        user = mongo.db.users.find_one({"username": username})
        if user:
            return jsonify({'message': 'User already exists'}), 400

        hashed_password = generate_password_hash(password)
        mongo.db.users.insert_one({"username": username, "name": name, "password": hashed_password})

        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        app.logger.error("Error in /register/: {}".format(str(e)), exc_info=True)
        return jsonify({'message': 'An error occurred'}), 500


@app.route("/get_movies/", methods=['GET'])
def get_movie_details():
    print("get_movies")
    search_query = request.args.get('query', '')  
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={tmdb_api_key}&query={search_query}"
    search_response = requests.get(search_url).json()

    if search_response['results']:
        top_movie = search_response['results'][0]  # Get the top result
        movie_id = top_movie['id']
        # Fetch more details about the movie using its ID
        detail_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_api_key}"
        detail_response = requests.get(detail_url).json()
        movie_details = {
            'name': detail_response.get('title', 'N/A'),
            'id': detail_response.get('id', 'N/A'),
            'release_year': detail_response.get('release_date', 'N/A')[:4] if detail_response.get('release_date') else 'N/A',
            'poster_path': f"https://image.tmdb.org/t/p/w200{detail_response.get('poster_path')}" if detail_response.get('poster_path') else None
        }
        return jsonify(movie_details)
    else:
        return jsonify({'error': 'Movie not found'}), 404


@app.route("/post_watched_movie/", methods=['POST'])
def post_watched_movie():
    data = request.get_json()
    username = session.get('username')
    movie_id = data.get('movieId')
    
    if not username:
        return {"error": "Unauthorized"}, 401
    if not movie_id:
        return {"error": "Missing movieId"}, 400
    
    user_doc = mongo.db.users.find_one({"username": username})
    
    if not user_doc:
        return {"error": "User not found"}, 404

    if 'watchedMovies' in user_doc:
        mongo.db.users.update_one(
            {"username": username},
            {"$addToSet": {"watchedMovies": movie_id}}
        )
    else:
        mongo.db.users.update_one(
            {"username": username},
            {"$set": {"watchedMovies": [movie_id]}}
        )
    
    user_doc = mongo.db.users.find_one({"username": username})
    watched_movies = user_doc.get('watchedMovies', [])
    movie_reviews = recommender.fetch_reviews_for_watched_movies(watched_movies)
    user_keywords = recommender.process_reviews(movie_reviews,positive_keywords,nlp)

    if 'userKeywords' in user_doc:
        mongo.db.users.update_one(
            {"username": username},
            {"$addToSet": {"userKeywords": {"$each": user_keywords}}}
        )
    else:
        mongo.db.users.update_one(
            {"username": username},
            {"$set": {"userKeywords":user_keywords}}
        )
    
    return {"message": "Movie added to watched list"}, 200



@app.route("/get_genres/", methods=['GET'])
def get_genres():
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={tmdb_api_key}&language=en-US"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        genre_names = [genre['name'] for genre in data['genres']]
        

        return jsonify(genre_names)
    
    except requests.RequestException as e:
        print(e)
        return jsonify({"error": "Failed to fetch genres from TMDB"}), 500
    


@app.route("/get_recommendations/", methods=['POST'])
def get_recommendations():
    data = request.get_json()
    username = session.get('username')

    genre_names = data.get('genres', [])

    genre_mapping = {genre['name']: str(genre['id']) for genre in mongo.db.genres.find()}

    genre_ids = [genre_mapping[name] for name in genre_names if name in genre_mapping]


    print(genre_ids)  


    print("Fetching Genre Movies")
    genre_reviews = recommender.fetch_reviews_for_genre_movies(genre_ids) 
    print("Fetching Genre Keywords")
    genre_keywords = recommender.extract_keywords_from_all_reviews(genre_reviews)

    user_doc = mongo.db.users.find_one({"username": username})
    user_keywords = user_doc.get('userKeywords', [])
    print("Getting Recommendations")
    recommended_movies = recommender.get_recommended_movies(genre_keywords, user_keywords, nlp)

    recommended_movies_details = []
    for movie_id in recommended_movies:
        movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_api_key}&language=en-US"
        movie_details_response = requests.get(movie_url).json()

        if 'title' in movie_details_response:
            recommended_movies_details.append({
                'id':movie_details_response['id'],
                'name': movie_details_response['title'],
                'year': movie_details_response['release_date'][:4] if 'release_date' in movie_details_response else 'N/A',
                'poster_path': f"https://image.tmdb.org/t/p/w200{movie_details_response['poster_path']}" if 'poster_path' in movie_details_response else None
            })

    print("Recommendations Sent")
    return jsonify(recommended_movies_details)

    

@app.route('/movie-details/<movie_id>', methods=['GET'])
def movie_details(movie_id):

    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_api_key}&append_to_response=videos,credits'
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json() 
        movie_reviews= recommender.get_movie_reviews(movie_id)
        movie_keywords= recommender.process_reviews({movie_id: movie_reviews},positive_keywords,nlp)
        movie_details = {
            'title': data['title'],
            'release_date': data['release_date'],
            'poster_path': f"https://image.tmdb.org/t/p/original{data['poster_path']}",
            'overview': data['overview'],
            'cast': [cast_member['name'] for cast_member in data['credits']['cast'][:5]],  # Top 5 cast members
            'user_score': data['vote_average'],
            'keywords': movie_keywords
        }
        return jsonify(movie_details)
    else:
        return jsonify({'error': 'Failed to fetch movie details'}), 404
    

@app.route('/movie-details/post_watchlist/<movie_id>', methods=['POST'])
def add_watchlist_movie(movie_id):
    username = session.get('username')
    if not username:
        return {"error": "Unauthorized"}, 401
    if not movie_id:
        return {"error": "Missing movieId"}, 400
    
    user_doc = mongo.db.users.find_one({"username": username})
    
    if not user_doc:
        return {"error": "User not found"}, 404

    if 'watchlist' in user_doc:
        mongo.db.users.update_one(
            {"username": username},
            {"$addToSet": {"watchlist": movie_id}}
        )
    else:
        mongo.db.users.update_one(
            {"username": username},
            {"$set": {"watchlist": [movie_id]}}
        )

    return {"message": "Movie added to watchlist"}, 200

@app.route('/get_watchlist/', methods=['GET'])
def get_watchlist():
    username = session.get('username')
    if not username:
        return {"error": "Unauthorized"}, 401

    user_doc = mongo.db.users.find_one({"username": username})
    watchlist = user_doc.get('watchlist', [])
    watchlist_details = []
    for movie_id in watchlist:
        movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_api_key}&language=en-US"
        movie_details_response = requests.get(movie_url).json()

        if 'title' in movie_details_response:
            watchlist_details.append({
                'id': movie_details_response['id'],
                'name': movie_details_response['title'],
                'year': movie_details_response['release_date'][:4] if 'release_date' in movie_details_response else 'N/A',
                'poster_path': f"https://image.tmdb.org/t/p/w200{movie_details_response['poster_path']}" if 'poster_path' in movie_details_response else None
            })

    return jsonify(watchlist_details)

@app.route('/movie-details/remove_from_watchlist/<movie_id>', methods=['DELETE'])
def remove_from_watchlist(movie_id):
    username = session.get('username')
    if not username:
        return {"error": "Unauthorized"}, 401
    if not movie_id:
        return {"error": "Missing movieId"}, 400
    user_doc = mongo.db.users.find_one({"username": username})
    watchlist = user_doc.get('watchlist', [])

    if movie_id in watchlist:
        mongo.db.users.update_one(
            {"username": username},
            {"$pull": {"watchlist": movie_id}}
        )
        return {"message": "Movie removed from watchlist"}, 200
    else:
        return {"error": "Movie not in watchlist"}, 404

@app.route('/get_watchlist_ids/', methods=['GET'])
def get_watchlist_ids():
    username = session.get('username')
    if not username:
        return {"error": "Unauthorized"}, 401
    user_doc = mongo.db.users.find_one({"username": username})
    watchlist = user_doc.get('watchlist', [])
    return watchlist


if __name__ == "__main__":
    os.system("gunicorn -w 4 -b 0.0.0.0:8080 -t 300 app:app")