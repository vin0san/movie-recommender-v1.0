from flask import Flask, render_template, request
from reader import *  # Imports function from reader.py

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    recommendations = None

    if request.method == "POST":
        movie_name = request.form.get("movie")
        recommendations = get_recommendations(movie_name)

    return render_template("home.html", recommendations=recommendations)



if __name__ == "__main__":
    app.run(debug=True)
