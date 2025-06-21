# reader.py


'''this file is mean't for testing the recommender module
and can be used as playground for testing the recommender'''

from recommender import Recommender

recommender = Recommender(
    "ml-latest-small/movies.csv",
    "ml-latest-small/tags.csv",
    "ml-latest-small/ratings.csv"
)

print(recommender.get_recommendations("superman"))

