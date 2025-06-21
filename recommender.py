from dotenv import load_dotenv
import os

# Load from .env file
load_dotenv()
api_key = os.getenv("TMDB_API_KEY")



import pandas as pd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Recommender:
    def __init__(self, movie_path, tag_path, ratings_path, links_path, tmdb_api_key):
        self.movies = pd.read_csv(movie_path)
        self.tags = pd.read_csv(tag_path)
        self.ratings = pd.read_csv(ratings_path)
        self.links = pd.read_csv(links_path)
        self.api_key = tmdb_api_key
        self.model_ready = False
        self._prepare_data()

    def _prepare_data(self):
        # Merge tags
        tag_data = self.tags.groupby('movieId')['tag'].apply(lambda x: ' '.join(x)).reset_index()
        self.movies = self.movies.merge(tag_data, on='movieId', how='left')
        self.movies['tag'] = self.movies['tag'].fillna('')

        # Merge links
        self.movies = self.movies.merge(self.links[['movieId', 'tmdbId']], on='movieId', how='left')

        # Genres + tags
        self.movies['genres'] = self.movies['genres'].str.replace('|', ' ', regex=False)
        self.movies['combined'] = self.movies['genres'] + ' ' + self.movies['tag']

        # Ratings summary
        rating_summary = self.ratings.groupby('movieId')['rating'].agg(['mean', 'count']).reset_index()
        rating_summary.columns = ['movieId', 'avg_rating', 'num_votes']
        self.movies = self.movies.merge(rating_summary, on='movieId', how='left')

        # TF-IDF
        tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = tfidf.fit_transform(self.movies['combined'])

        # Cosine similarity
        self.similarity_matrix = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

        self.movies = self.movies.reset_index()
        self.model_ready = True

    def _get_poster_url(self, tmdb_id):
        """Fetch poster URL from TMDb"""
        if pd.isna(tmdb_id):
            return None
        try:
            url = f"https://api.themoviedb.org/3/movie/{int(tmdb_id)}?api_key={self.api_key}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data.get("poster_path"):
                    return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
        except:
            pass
        return None

    def get_recommendations(self, title=None, n=10, genre=None, mood=None):
        if not self.model_ready:
            return []

        if not title and not genre and not mood:
            return []

        # Genre/mood filter only
        if not title:
            filtered = self.movies.copy()
            if genre:
                filtered = filtered[filtered['genres'].str.contains(genre, case=False, na=False)]
            if mood:
                filtered = filtered[filtered['tag'].str.contains(mood, case=False, na=False)]
            filtered = filtered[filtered['num_votes'] > 10]
            filtered['score'] = (
                0.7 * filtered['avg_rating'].fillna(0) +
                0.3 * filtered['num_votes'].fillna(0).apply(lambda x: min(x, 1000) / 1000)
            )
            top = filtered.sort_values(by='score', ascending=False).head(n)
            return self._format_results(top)

        # Title-based similarity
        matches = self.movies[self.movies['title'].str.lower().str.contains(title.lower(), na=False)]
        if matches.empty:
            return []

        idx = matches.index[0]
        self.last_matched_title = self.movies.iloc[idx]['title']

        sim_scores = list(enumerate(self.similarity_matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:50]
        movie_indices = [i[0] for i in sim_scores]
        similar_movies = self.movies.iloc[movie_indices].copy()

        # Include keyword title matches (for sequels/prequels)
        keyword_matches = self.movies[self.movies['title'].str.lower().str.contains(title.lower(), na=False)]
        combined = pd.concat([similar_movies, keyword_matches]).drop_duplicates(subset='title')

        if genre:
            combined = combined[combined['genres'].str.contains(genre, case=False, na=False)]
        if mood:
            combined = combined[combined['tag'].str.contains(mood, case=False, na=False)]

        combined = combined[combined['num_votes'] > 10]
        combined['score'] = (
            0.7 * combined['avg_rating'].fillna(0) +
            0.3 * combined['num_votes'].fillna(0).apply(lambda x: min(x, 1000) / 1000)
        )

        top_combined = combined.sort_values(by='score', ascending=False).head(n)
        return self._format_results(top_combined)

    def _format_results(self, df):
        results = []
        for _, row in df.iterrows():
            results.append({
                "title": row['title'],
                "poster": self._get_poster_url(row['tmdbId'])
            })
        return results
