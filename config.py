from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()

class ApplicationConfig:
    SECRET_KEY = os.environ["SECRET_KEY"]
    MONGO_URI = os.environ["MONGO_URI"]
    TMDB_API_KEY = os.environ["TMDB_API_KEY"]
    TMDB_ACCESS_TOKEN = os.environ["TMDB_ACCESS_TOKEN"]
    SESSION_TYPE = "filesystem"
    SESSION_FILE_DIR = '/tmp/flask_session'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_COOKIE_SECURE = False 
    SESSION_COOKIE_SAMESITE = None  
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}