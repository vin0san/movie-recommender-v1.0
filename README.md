# Movie Recommendation Website
This is a Movie Recommendation Web App built with Flask (Python backend) and a clean HTML/CSS frontend. The app suggests movies based on user input and displays poster images, titles, and other relevant details in a responsive and retro-minimalist layout.

# Features
 Search a movie and get recommendations based on content similarity

🎨 Clean, retro-minimal UI design

🖼️ Displays movie posters* and titles

🧠 Uses precomputed similarity scores (cosine similarity or content-based filtering)

🔥 Lightweight and fast Flask backend.

# Tech Stack

| Layer    | Technology                       |
| -------- | -------------------------------- |
| Backend  | Python, Flask                    |
| Frontend | HTML5, CSS3                      |
| Data     | CSV dataset (movies metadata)    |
| ML Model | Cosine Similarity (from sklearn) |

# How It Works
User Inputs Movie Name

On the homepage (index.html), the user enters a movie title.

Flask Backend Handles Request

app.py uses the input to find the most similar movies using a similarity matrix.

Recommendations Displayed

The results are passed to recommend.html, which renders recommended movies with poster images.
