import requests
import spacy
from rake_nltk import Rake
import random
import nltk
from dotenv import load_dotenv
import os
from concurrent.futures import ThreadPoolExecutor



class MovieRecommendation:
    def __init__(self):
        load_dotenv()
        self.TMDB_API_KEY = os.getenv("TMDB_API_KEY")
        self.TMDB_ACCESS_TOKEN = os.getenv("TMDB_ACCESS_TOKEN")
        self.positive_keywords =  [
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
        nltk_data_path = os.path.join(os.path.dirname(__file__), 'nltk_data')
        nltk.data.path.append(nltk_data_path)
        self.ensure_nltk_data()
        self.load_spacy_model()
    def ensure_nltk_data(self):
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
        except LookupError:
            raise Exception("Required NLTK datasets are missing!")
    
    def load_spacy_model(self):
        try:
            self.nlp = spacy.load("en_core_web_md", disable=["parser", "ner"])
        except OSError:
            print("Downloading NLTK data and SpaCy models...")
            from spacy.cli import download
            download("en_core_web_md")
            self.nlp = spacy.load("en_core_web_md", disable=["parser", "ner"])


    # Fetch movie reviews from TMDB API
    def get_movie_reviews(self,movie_id):
        url = f'https://api.themoviedb.org/3/movie/{movie_id}/reviews?&page=1'
        headers = {
            'Authorization': 'Bearer ' + self.TMDB_ACCESS_TOKEN,
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


    # Fetch reviews for a list of watched movies
    def fetch_reviews_for_watched_movies(self,watched_movies):
        movie_reviews_dict = {}
        for movie_id in watched_movies:
            reviews = self.get_movie_reviews(movie_id)
            movie_reviews_dict[movie_id] = reviews
        return movie_reviews_dict


    def extract_keywords_from_all_reviews(self,movie_reviews_dict):

        self.ensure_nltk_data()  
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

    def filter_keywords(self,text, positive_keywords, nlp):
        doc = nlp(text)
        matched_keywords = []

        keywords_tokens = [nlp(keyword)[0] for keyword in positive_keywords]

        for token in doc:

            if token.pos_ == 'ADJ':
                for keyword_token in keywords_tokens:
                
                    if token.text.lower() == keyword_token.text.lower() or token.similarity(keyword_token) > 0.8:
                        matched_keywords.append(token.text.lower())

        return list(set(matched_keywords))


    def list_to_pipe_string(self,lst):

        return "|".join(map(str, lst))

    def process_reviews(self,movie_reviews_dict, positive_keywords, nlp):
        keywords = self.extract_keywords_from_all_reviews(movie_reviews_dict)
        all_phrases = []
        for keywords_with_scores in keywords.values():
            for _, phrase in keywords_with_scores:
                all_phrases.append(phrase)  # Collecting phrases only

        text = '. '.join(all_phrases)
        final_output = self.filter_keywords(text, positive_keywords, nlp)
        return final_output


    def fetch_reviews_for_genre_movies(self,genre_ids):

        movies = self.discover_movies_by_genre(genre_ids)
        
        movie_reviews_dict = {} 
        # Iterate over each movie to fetch its reviews
        for movie in movies:
            movie_id = movie['id']
            reviews = self.fetch_movie_reviews(movie_id)  
            movie_reviews_dict[movie_id] = reviews    
        return movie_reviews_dict


    def discover_movies_by_genre(self,genre_ids):
        all_filtered_results = [] 

        for page in range(1, 10):  
            url = f'https://api.themoviedb.org/3/discover/movie?with_genres={"|".join(genre_ids)}&page={page}'
            headers = {
                'Authorization': 'Bearer ' + self.TMDB_ACCESS_TOKEN,
                'accept': 'application/json',
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                results = response.json()['results']
                filtered_results = [
                    {
                        'id': movie['id'],
                        'original_title': movie['original_title'],
                    }
                    for movie in results
                ]
                all_filtered_results.extend(filtered_results)  
            else:
                print(f"Failed to fetch movies from TMDB API for page {page}")
                break  
        return all_filtered_results


    # i have another funtion
    def fetch_movie_reviews(self,movie_id):

        reviews_url = f'https://api.themoviedb.org/3/movie/{movie_id}/reviews?language=en-US&page=1'
        headers = {
        'Authorization': 'Bearer '+self.TMDB_ACCESS_TOKEN,
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

    def preprocess_keywords(self,movie_keywords_dict):
        return {movie_id: '. '.join(phrase for score, phrase in keywords_with_scores)
            for movie_id, keywords_with_scores in movie_keywords_dict.items()}

    def match_and_score(self,movie_id, keywords_text, user_keywords, nlp, top_movies):
        matched_keywords = self.filter_keywords(keywords_text, user_keywords, nlp)
        if matched_keywords:
            matched_count = len(matched_keywords)
            if len(top_movies) < 20 or matched_count > top_movies[0][1]:
                if len(top_movies) >= 20:
                    heapq.heappop(top_movies)
                heapq.heappush(top_movies, (matched_count, movie_id))

    def get_recommended_movies(self, movie_keywords_dict, user_keywords, nlp):
        preprocessed_keywords = self.preprocess_keywords(movie_keywords_dict)
        top_movies = []

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.match_and_score, movie_id, keywords_text, user_keywords, nlp, top_movies)
                    for movie_id, keywords_text in preprocessed_keywords.items()]

        top_20_movies = [movie_id for _, movie_id in sorted(top_movies, reverse=True)]
        return top_20_movies


            



