# 🎬 Movie Recommender v1.0

A personalized movie recommendation system built with Python, Flask, and the TMDb API.

It suggests movies based on:
- 🎞️ Movie title (including similar, sequels & prequels)
- 🎭 Genre
- 🧠 Mood (user tags)
- 📊 Popularity (average rating & vote count)

With a simple, retro-inspired UI (because I don’t bang my head around frontend stuff).

---

## 🧠 Features

- 🔍 **Title-based Search** — Find movies similar to a specific title.
- 🎯 **Genre & Mood Filters** — Browse by mood (e.g., "dark", "uplifting") and genres.
- 🧮 **Smart Ranking** — Uses TF-IDF & Cosine Similarity + rating data.
- 🎞️ **Posters via TMDb API** — Fetches movie posters dynamically.
- 🖥️ **Retro UI Vibes** — Simple UI styled like an old imageboard for that vintage feel.

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Machine Learning**: scikit-learn (TF-IDF + cosine similarity)
- **Dataset**: [MovieLens (ml-latest-small)](https://grouplens.org/datasets/movielens/)
- **API**: [TMDb API](https://www.themoviedb.org/documentation/api)
- **Frontend**: HTML, CSS (retro-inspired)


## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/movie-recommender.git
cd movie-recommender
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Your API Key

Create a .env file and place your API key
```
TMDB_API_KEY=your_tmdb_api_key_here
```
### 4. Run the App

```bash
python app.py
```

### Note: This project is for fun, and no deployment is planned.
