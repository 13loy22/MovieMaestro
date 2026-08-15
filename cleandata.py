import json

import pandas as pd


movies = pd.read_csv("movies.csv")

with open("user_data.json", "r") as file:
    users = json.load(file)

viewing_history = pd.read_csv("viewing_history.csv")


movies = movies.drop_duplicates().dropna()

movies["movie_id"] = movies["movie_id"].astype(int)
movies["votes"] = movies["votes"].astype(int)
movies["runtime"] = movies["runtime"].astype(int)
movies["release_year"] = movies["release_year"].astype(int)
movies["rating"] = movies["rating"].round(2)
movies["revenue"] = movies["revenue"].round(2)


viewing_history = viewing_history.drop_duplicates().dropna()

viewing_history["user_id"] = viewing_history["user_id"].astype(int)
viewing_history["movie_id"] = viewing_history["movie_id"].astype(int)
viewing_history["rating"] = viewing_history["rating"].astype(int)

viewing_history = viewing_history[
    viewing_history["rating"].between(1, 5)
]

viewing_history["timestamp"] = pd.to_datetime(
    viewing_history["timestamp"],
    errors="coerce"
)

viewing_history = viewing_history.dropna(
    subset=["timestamp"]
)


valid_movie_ids = set(movies["movie_id"])
valid_genres = set(movies["genre"].unique())

clean_users = []

for user in users:
    user_id = int(user["user_id"])
    name = str(user["name"])
    age = int(user["age"])

    if not 18 <= age <= 65:
        continue

    preferences = [
        genre
        for genre in user["preferences"]
        if genre in valid_genres
    ]

    watch_history = []

    for watch in user["watch_history"]:
        movie_id = int(watch["movie_id"])
        rating = int(watch["rating"])

        if movie_id in valid_movie_ids and 1 <= rating <= 5:
            watch_history.append({
                "movie_id": movie_id,
                "rating": rating
            })

    clean_users.append({
        "user_id": user_id,
        "name": name,
        "age": age,
        "preferences": preferences,
        "watch_history": watch_history
    })


movie_stats = (
    viewing_history
    .groupby("movie_id")
    .agg(
        viewing_count=("user_id", "count"),
        average_user_rating=("rating", "mean")
    )
    .reset_index()
)

movie_stats["average_user_rating"] = (
    movie_stats["average_user_rating"].round(2)
)


processed_movies = movies.merge(
    movie_stats,
    on="movie_id",
    how="left"
)

processed_movies["viewing_count"] = (
    processed_movies["viewing_count"]
    .fillna(0)
    .astype(int)
)

processed_movies["average_user_rating"] = (
    processed_movies["average_user_rating"]
    .fillna(0)
    .round(2)
)


user_stats = (
    viewing_history
    .groupby("user_id")
    .agg(
        total_views=("movie_id", "count"),
        average_rating=("rating", "mean")
    )
    .reset_index()
)

user_stats["average_rating"] = (
    user_stats["average_rating"].round(2)
)


user_movie_data = viewing_history.merge(
    movies,
    on="movie_id",
    how="left",
    suffixes=("_user", "_movie")
)


processed_movies.to_csv(
    "processed_movies.csv",
    index=False
)

viewing_history.to_csv(
    "clean_viewing_history.csv",
    index=False
)

user_stats.to_csv(
    "user_stats.csv",
    index=False
)

user_movie_data.to_csv(
    "user_movie_data.csv",
    index=False
)


with open("clean_users.json", "w") as file:
    json.dump(clean_users, file, indent=4)


print("Data processing completed successfully.")
print(f"Movies: {len(processed_movies)}")
print(f"Users: {len(clean_users)}")
print(f"Viewing events: {len(viewing_history)}")
print(f"User-movie records: {len(user_movie_data)}")