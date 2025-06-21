from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

from recommender import Recommender

# Load environment variables from .env
load_dotenv()
tmdb_api_key = os.getenv("TMDB_API_KEY")

recommender = Recommender(
    movie_path="ml-latest-small/movies.csv",
    tag_path="ml-latest-small/tags.csv",
    ratings_path="ml-latest-small/ratings.csv",
    links_path="ml-latest-small/links.csv",
    tmdb_api_key=tmdb_api_key
)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    matched_title = None
    recommendations = None

    if request.method == "POST":
        movie_name = request.form.get("movie") or ""
        selected_genre = request.form.get("genre")
        selected_mood = request.form.get("mood")

        recommendations = recommender.get_recommendations(
            title=movie_name,
            genre=selected_genre,
            mood=selected_mood
        )

        # Show matched title only if input title was given
        if movie_name.strip():
            matched_title = getattr(recommender, "last_matched_title", None)

    return render_template("index.html", recommendations=recommendations, matched_title=matched_title)

if __name__ == "__main__":
    app.run(debug=True)
