from dotenv import load_dotenv
import os
import requests
import spacy
from rake_nltk import Rake
import random

load_dotenv()

TMBD_API_KEY=os.environ["TMDB_API_KEY"]
TMBD_ACCESS_TOKEN=os.environ["TMDB_ACCESS_TOKEN"]
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


def get_movie_reviews(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}/reviews?&page=1'
    headers = {
    'Authorization': 'Bearer '+TMBD_ACCESS_TOKEN,
    'accept': 'application/json',
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        reviews_data = response.json()
        reviews_list = []
        

        for review in reviews_data.get("results", []):
            review_info = {
                "movie_id": movie_id,
                "rating": review["author_details"].get("rating"),
                "content": review["content"]
            }
            reviews_list.append(review_info)
        
        return reviews_list
    else:
        print("Failed to fetch reviews from TMDB API")
        return []  

def fetch_reviews_for_watched_movies(watched_movies):
    movie_reviews_dict = {}
    for movie_id in watched_movies:
        reviews = get_movie_reviews(movie_id)
        movie_reviews_dict[movie_id] = reviews
    return movie_reviews_dict

def ensure_nltk_data():
    import nltk
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')

def extract_keywords_from_all_reviews(movie_reviews_dict):

    ensure_nltk_data()  
    movie_keywords_dict = {} 
    
    for movie_id, reviews in movie_reviews_dict.items():
        rake = Rake()
        all_phrases_with_scores = []
        for review in reviews:
            rake.extract_keywords_from_text(review['content'])
            phrases_with_scores = rake.get_ranked_phrases_with_scores()
            all_phrases_with_scores.extend(phrases_with_scores)

        # Sort phrases by score in descending order and keep unique
        sorted_phrases_with_scores = sorted(all_phrases_with_scores, key=lambda x: x[0], reverse=True)
        unique_keywords_with_scores = []
        seen_keywords = set()
        for score, phrase in sorted_phrases_with_scores:
            if phrase not in seen_keywords:
                unique_keywords_with_scores.append((score, phrase))
                seen_keywords.add(phrase)
            if len(unique_keywords_with_scores) == 100: 
                break

        movie_keywords_dict[movie_id] = unique_keywords_with_scores

    return movie_keywords_dict
# more filteration using spacy 
def filter_keywords(text, positive_keywords, nlp):
    doc = nlp(text)
    matched_keywords = []

    # Generate a list of keyword tokens with vectors
    keywords_tokens = [nlp(keyword)[0] for keyword in positive_keywords if nlp(keyword)[0].has_vector]

    for token in doc:
        if token.pos_ == 'ADJ' and token.has_vector:
            # Check each keyword token for similarity, ensuring both tokens have vectors
            for keyword_token in keywords_tokens:
                if token.text.lower() == keyword_token.text.lower() or (keyword_token.has_vector and token.similarity(keyword_token) > 0.8):
                    matched_keywords.append(token.text.lower())

    return list(set(matched_keywords))

def list_to_pipe_string(lst):

    return "|".join(map(str, lst))

def process_reviews(movie_reviews_dict, positive_keywords, nlp):
    keywords = extract_keywords_from_all_reviews(movie_reviews_dict)
    all_phrases = []
    for keywords_with_scores in keywords.values():
        for _, phrase in keywords_with_scores:
            all_phrases.append(phrase)  # Collecting phrases only

    text = '. '.join(all_phrases)
    final_output = filter_keywords(text, positive_keywords, nlp)
    return final_output

def discover_movies_by_genre(genre_ids):
    all_filtered_results = [] 

    for page in range(1, 10):  
        url = f'https://api.themoviedb.org/3/discover/movie?with_genres={"|".join(genre_ids)}&page={page}'
        headers = {
            'Authorization': 'Bearer ' + TMBD_ACCESS_TOKEN,
            'accept': 'application/json',
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            results = response.json()['results']
            filtered_results = [
                {
                    'id': movie['id'],
                    'original_title': movie['original_title'],
                    #'popularity': movie['popularity'],
                    #'vote_count': movie['vote_count']
                }
                for movie in results
            ]
            all_filtered_results.extend(filtered_results)  
        else:
            print(f"Failed to fetch movies from TMDB API for page {page}")
            break  
    return all_filtered_results
# i have another funtion
def fetch_movie_reviews(movie_id):

    reviews_url = f'https://api.themoviedb.org/3/movie/{movie_id}/reviews?language=en-US&page=1'
    headers = {
    'Authorization': 'Bearer '+TMBD_ACCESS_TOKEN,
    'accept': 'application/json',
    }
    response = requests.get(reviews_url,headers=headers)
    if response.status_code == 200:
        reviews_data = response.json()
        reviews_list = []
        

        for review in reviews_data.get("results", []):
            review_info = {
                "movie_id": movie_id,
                "rating": review["author_details"].get("rating"),
                "content": review["content"]
            }
            reviews_list.append(review_info)
        
        return reviews_list
    return []

# function for getting all reviews for a genre
def fetch_reviews_for_genre_movies(genre_ids):

    movies = discover_movies_by_genre(genre_ids)
     
    movie_reviews_dict = {} 
    # Iterate over each movie to fetch its reviews
    for movie in movies:
        movie_id = movie['id']
        reviews = fetch_movie_reviews(movie_id)  
        movie_reviews_dict[movie_id] = reviews   
    print("total movies for genre is:",len(movie_reviews_dict)) 
    return movie_reviews_dict

#  duplicate functoin
def extract_keywords_from_reviews(reviews):
    ensure_nltk_data()  # Ensure NLTK data is available
    rake = Rake()
    all_phrases_with_scores = []
    for review in reviews:
        rake.extract_keywords_from_text(review['content'])
        phrases_with_scores = rake.get_ranked_phrases_with_scores()
        all_phrases_with_scores.extend(phrases_with_scores)

    # Sort keywords by score in descending order
    sorted_phrases_with_scores = sorted(all_phrases_with_scores, key=lambda x: x[0], reverse=True)

    # Filter to keep only unique keywords, maintaining the order and their scores
    unique_keywords_with_scores = []
    seen_keywords = set()
    for score, phrase in sorted_phrases_with_scores:
        if phrase not in seen_keywords:
            unique_keywords_with_scores.append((score, phrase))
            seen_keywords.add(phrase)
        if len(unique_keywords_with_scores) == 100:
            break

    return unique_keywords_with_scores

def extract_keywords_for_all_movies(reviews_dict):
    movie_keywords_dict = {}
    for movie_id, reviews in reviews_dict.items():
        # Extract keywords from the list of reviews for the current movie
        keywords_with_scores = extract_keywords_from_reviews(reviews)
        # Store the extracted keywords in the dictionary with the movie ID as the key
        movie_keywords_dict[movie_id] = keywords_with_scores
    return movie_keywords_dict

def get_similarity_score(movie_keywords, user_keywords, nlp):
    scores = []
    for user_keyword in user_keywords:
        user_token = nlp(user_keyword)
        max_similarity = 0
        for movie_keyword in movie_keywords:
            movie_token = nlp(movie_keyword)
            if user_token.has_vector and movie_token.has_vector:
                similarity = user_token.similarity(movie_token)
                max_similarity = max(max_similarity, similarity)
        scores.append(max_similarity)
    return sum(scores) / len(scores) if scores else 0

def get_recommended_movies(movie_keywords_dict, user_keywords, nlp):
    movie_scores = []

    for movie_id, keywords_with_scores in movie_keywords_dict.items():
        keywords_text = '. '.join([phrase for score, phrase in keywords_with_scores])
        matched_keywords = filter_keywords(keywords_text, user_keywords, nlp)
        
        if matched_keywords:
            matched_count = len(matched_keywords)
            movie_scores.append((movie_id, matched_count))

    sorted_movie_ids = [movie_id for movie_id, _ in sorted(movie_scores, key=lambda x: x[1], reverse=True)]
    print("total recommened movies",len(sorted_movie_ids))
    top_20_movies = random.sample(sorted_movie_ids, min(20, len(sorted_movie_ids)))

    return top_20_movies

def fetch_movie_title(movie_id):
    movie_url = f'https://api.themoviedb.org/3/movie/{movie_id}'
    headers = {
    'Authorization': 'Bearer '+TMBD_ACCESS_TOKEN,
    'accept': 'application/json',
    }
    response = requests.get(movie_url, headers=headers)
    if response.status_code == 200:
        movie_data = response.json()
        return movie_data['title']
    else:
        print(f"Failed to fetch title for movie ID {movie_id}")
        return None




watched_movies = [346698,693134,577922,27205,1726,1724, 27205, 272, 24428, 585244]
genre_ids = ["878"]
def main():
    print("Starting the recommendation process")
    print('Fetching reviews for watched movies')
    movies_reviews = fetch_reviews_for_watched_movies(watched_movies)
    print('Processing reviews for watched movies')
    user_keywords = process_reviews(movies_reviews,positive_keywords,nlp)
    print('User Keywords:', user_keywords)
    print('Fetching reviews for genre movies')
    genre_reviews = fetch_reviews_for_genre_movies(genre_ids)
    print('Processing reviews for genre movies')
    genre_keywords = extract_keywords_from_all_reviews(genre_reviews)
    print('Getting recommended movies')
    recommended_movies = get_recommended_movies(genre_keywords, user_keywords, nlp)
    return recommended_movies

movies = main()

print(len(movies))
for movie_id in movies[:40]:
    title = fetch_movie_title(movie_id)
    if title:
        print(title)

