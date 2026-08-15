import numpy as np
import pandas as pd
from IPython.display import display

# Number of movies
number_of_movies = 1000

# Generate movie data
movie_ids = np.arange(1, number_of_movies + 1)
ratings = np.random.uniform(1, 10, number_of_movies)
votes = np.random.randint(100, 100000, number_of_movies)
runtime = np.random.randint(80, 181, number_of_movies)
release_year = np.random.randint(2000, 2026, number_of_movies)
revenue = np.random.uniform(1, 500, number_of_movies)
genres = np.random.choice(
    ["Action", "Comedy", "Drama", "Horror", "Sci-Fi"],
    number_of_movies
)

# Create a DataFrame
df = pd.DataFrame({
    'movie_id': movie_ids,
    'rating': ratings,
    'votes': votes,
    'runtime': runtime,
    'release_year': release_year,
    'revenue': revenue,
    'genre': genres
})

# Save to CSV
df.to_csv('movies.csv', index=False)

print("Data generated and saved to movies.csv")
display(df.head())