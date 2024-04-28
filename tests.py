import unittest
from recom import MovieRecommendation

class TestMovieRecommendation(unittest.TestCase):
    def setUp(self):
        self.recommender = MovieRecommendation()

    def test_get_movie_reviews(self):
      
      reviews = self.recommender.get_movie_reviews("1022796")
      assert type(reviews) is list, "Should return a list of reviews"
    
    def test_genre_movies_testing(self):
      movies = self.recommender.discover_movies_by_genre(["16,35"])
      assert type(movies) is list, "Should return a list of movies"
      assert 'id' in movies[0] and 'original_title' in movies[0], "Movies should have 'id' and 'original_title'"
    
    def test_invalid_genre_ids(self):
      
      movies = self.recommender.discover_movies_by_genre(["9999"]) 
      assert movies == [], "Should return an empty list for invalid genre IDs"
    

    def test_extract_keywords_from_reviews(self):
      
      mock_reviews = {
          1: [{'movie_id': 1022796, 
               'rating': 6, 
               'content': (
                'With her grandpa hitting his hundredth birthday, '
                'the precocious young "Asha" hopes that the King, keeper'
                ' well written story with good end and good acting. '
            )}]
      }
      keywords = self.recommender.extract_keywords_from_all_reviews(mock_reviews)
      assert 1 in keywords, "Movie ID should be a key in the dictionary"
      assert len(keywords[1]) > 0, "Should extract non-zero keywords"

    def test_filter_keywords(self):
      mock_pharse = "This movie overall good watch with stunning visuals and brilliant acting."
      filtered_keywords = self.recommender.filter_keywords(mock_pharse, 
                          self.recommender.positive_keywords, self.recommender.nlp)
      assert "stunning" in filtered_keywords
    
    def test_api_failure_handling(self):

      response = self.recommender.get_movie_reviews("9999999")  
      assert response == [], "Should return an empty list on API failure"
    

    def test_get_recommended_movies(self):
      
      mock_movie_keywords = {
          100: [(10, 'stunning'), (9, 'brilliant'), (8, 'emotional'), 
          (7, 'beautiful'), (6, 'cinematic'), (5, 'compelling')],

          101: [(10, 'slow'), (9, 'boring'), (8, 'dull')],

          102: [(10, 'fascinating'), (9, 'intriguing'), (8, 'thought-provoking'), 
                (7, 'intelligent'), (6, 'emotional'), (5, 'remarkable')],
                
          103: [(10, 'fast'), (9, 'slowpaced'), (8, 'hyped'), (7, 'mustwatch'), 
                (6, 'very boring'), (5, 'unwatchable')]
      }
     
      user_keywords = ['stunning', 'brilliant', 'emotional', 'beautiful', 'cinematic',
                      'compelling', 'fascinating', 'intriguing', 'thought-provoking', 
                      'intelligent', 'remarkable']
     
      recommended_movies = self.recommender.get_recommended_movies(
      mock_movie_keywords, user_keywords, self.recommender.nlp)
      assert set(recommended_movies) == {100, 102}
      assert len(recommended_movies) == 2, "Should recommend two movies based on the keyword matches"

    


if __name__ == '__main__':
    unittest.main()