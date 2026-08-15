import numpy as np
import pandas as pd

number_of_movies = 1000

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

movies = pd.DataFrame({
    "movie_id": movie_ids,
    "rating": ratings.round(2),
    "votes": votes,
    "runtime": runtime,
    "release_year": release_year,
    "revenue": revenue.round(2),
    "genre": genres
})

movies.to_csv("movies.csv", index=False)

print(f"Created {len(movies)} movies.")
print(f"Saved to movies.csv.")