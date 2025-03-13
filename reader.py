import pandas as pd

# Load your dataset (assuming you have a CSV file)
df = pd.read_csv("ml-latest-small/movies.csv")

# Function to recommend movies based on popularity (example logic)
def get_recommendations(movie_name):
    # Dummy logic: Filter movies containing the input name
    recommendations = df[df['title'].str.contains(movie_name, case=False, na=False)]
    return recommendations['title'].tolist()[:5]  # Return top 5 matches
