import pandas as pd

# Loading dataset from CSV file
df = pd.read_csv("ml-latest-small/movies.csv")

# Function to recommend movies based on popularity
def get_recommendations(movie_name):
    recommendations = df[df['title'].str.contains(movie_name, case=False, na=False)]
    return recommendations['title'].tolist()[:5]  # Return top 5 matches
