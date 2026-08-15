import pandas as pd
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Load processed datasets

movies = pd.read_csv(BASE_DIR / "processed_movies.csv")
history = pd.read_csv(BASE_DIR / "clean_viewing_history.csv")
with open(BASE_DIR / "clean_users.json", "r", encoding="utf-8") as file:
    users = pd.DataFrame(json.load(file))

# --------------------------------------------------
# BASIC DATASET INFORMATION
# --------------------------------------------------

print("\nDATASET OVERVIEW")
print("----------------")
print("Movies:", len(movies))
print("Users:", len(users))
print("Viewing events:", len(history))


# --------------------------------------------------
# MOVIE ANALYSIS
# --------------------------------------------------

print("\nMOVIE ANALYSIS")
print("--------------")

# Most watched movies

most_watched_movies = (
    history.groupby("movie_id")
    .size()
    .reset_index(name="view_count")
    .sort_values("view_count", ascending=False)
)

most_watched_movies = most_watched_movies.merge(
    movies[["movie_id", "genre", "rating", "release_year", "runtime", "revenue"]],
    on="movie_id",
    how="left"
)

print("\nTop 10 most watched movies:")
print(most_watched_movies.head(10).to_string(index=False))


# Highest rated movies

highest_rated_movies = (
    movies.sort_values("rating", ascending=False)
    [["movie_id", "rating", "genre", "release_year", "votes"]]
)

print("\nTop 10 highest-rated movies:")
print(highest_rated_movies.head(10).to_string(index=False))


# --------------------------------------------------
# GENRE ANALYSIS
# --------------------------------------------------

print("\nGENRE ANALYSIS")
print("--------------")

genre_analysis = (
    movies.groupby("genre")
    .agg(
        movie_count=("movie_id", "count"),
        average_movie_rating=("rating", "mean"),
        average_revenue=("revenue", "mean"),
        average_runtime=("runtime", "mean")
    )
    .round(2)
    .sort_values("average_movie_rating", ascending=False)
)

print("\nGenre statistics:")
print(genre_analysis)


# Most watched genres

history_with_genre = history.merge(
    movies[["movie_id", "genre"]],
    on="movie_id",
    how="left"
)

genre_views = (
    history_with_genre.groupby("genre")
    .size()
    .reset_index(name="view_count")
    .sort_values("view_count", ascending=False)
)

print("\nMost watched genres:")
print(genre_views.to_string(index=False))


# Average user rating by genre

genre_user_ratings = (
    history_with_genre.groupby("genre")["rating"]
    .mean()
    .reset_index(name="average_user_rating")
    .sort_values("average_user_rating", ascending=False)
)

genre_user_ratings["average_user_rating"] = (
    genre_user_ratings["average_user_rating"].round(2)
)

print("\nAverage user rating by genre:")
print(genre_user_ratings.to_string(index=False))


# --------------------------------------------------
# USER ANALYSIS
# --------------------------------------------------

print("\nUSER ANALYSIS")
print("------------")

user_stats = (
    history.groupby("user_id")
    .agg(
        total_views=("movie_id", "count"),
        average_rating=("rating", "mean"),
        unique_movies=("movie_id", "nunique")
    )
    .reset_index()
)

user_stats["average_rating"] = user_stats["average_rating"].round(2)

print("\nUser statistics:")
print(user_stats.head(10).to_string(index=False))


# Most active users

most_active_users = (
    user_stats.sort_values("total_views", ascending=False)
    .head(10)
)

print("\nTop 10 most active users:")
print(most_active_users.to_string(index=False))


# Users with highest average ratings

highest_rated_users = (
    user_stats.sort_values("average_rating", ascending=False)
    .head(10)
)

print("\nTop 10 users by average rating:")
print(highest_rated_users.to_string(index=False))


# --------------------------------------------------
# AGE ANALYSIS
# --------------------------------------------------

print("\nAGE ANALYSIS")
print("------------")

users_with_stats = users[["user_id", "age"]].merge(
    user_stats,
    on="user_id",
    how="left"
)

age_groups = pd.cut(
    users_with_stats["age"],
    bins=[17, 25, 35, 45, 55, 65],
    labels=[
        "18-25",
        "26-35",
        "36-45",
        "46-55",
        "56-65"
    ]
)

age_analysis = (
    users_with_stats.groupby(age_groups, observed=False)
    .agg(
        users=("user_id", "count"),
        average_views=("total_views", "mean"),
        average_rating=("average_rating", "mean")
    )
    .round(2)
)

print("\nAge group analysis:")
print(age_analysis)


# --------------------------------------------------
# USER PREFERENCES
# --------------------------------------------------

print("\nUSER PREFERENCE ANALYSIS")
print("------------------------")

preference_counts = {}

for user in users.to_dict("records"):
    for preference in user.get("preferences", []):
        preference_counts[preference] = (
            preference_counts.get(preference, 0) + 1
        )

preference_analysis = (
    pd.DataFrame(
        list(preference_counts.items()),
        columns=["genre", "users_with_preference"]
    )
    .sort_values("users_with_preference", ascending=False)
)

print("\nMost common user preferences:")
print(preference_analysis.to_string(index=False))


# --------------------------------------------------
# MOVIE PERFORMANCE
# --------------------------------------------------

print("\nMOVIE PERFORMANCE")
print("-----------------")

movie_performance = (
    history.groupby("movie_id")
    .agg(
        viewing_count=("user_id", "count"),
        average_user_rating=("rating", "mean"),
        unique_users=("user_id", "nunique")
    )
    .reset_index()
)

movie_performance = movie_performance.merge(
    movies[
        [
            "movie_id",
            "genre",
            "rating",
            "votes",
            "runtime",
            "release_year",
            "revenue"
        ]
    ],
    on="movie_id",
    how="left"
)

movie_performance["average_user_rating"] = (
    movie_performance["average_user_rating"].round(2)
)

print("\nTop 10 movies by viewing count:")
print(
    movie_performance
    .sort_values("viewing_count", ascending=False)
    .head(10)
    .to_string(index=False)
)


# --------------------------------------------------
# IMPORTANT OBSERVATIONS
# --------------------------------------------------

print("\nOBSERVATIONS")
print("------------")

most_watched_genre = genre_views.iloc[0]["genre"]
most_watched_genre_views = genre_views.iloc[0]["view_count"]

highest_rated_genre = genre_user_ratings.iloc[0]["genre"]
highest_rated_genre_score = genre_user_ratings.iloc[0]["average_user_rating"]

most_popular_movie = most_watched_movies.iloc[0]["movie_id"]
most_popular_movie_views = most_watched_movies.iloc[0]["view_count"]

highest_rated_movie = highest_rated_movies.iloc[0]["movie_id"]
highest_rated_movie_score = highest_rated_movies.iloc[0]["rating"]

most_active_user = most_active_users.iloc[0]["user_id"]
most_active_user_views = most_active_users.iloc[0]["total_views"]

print(
    f"1. The most watched genre is {most_watched_genre} "
    f"with {most_watched_genre_views} viewing events."
)

print(
    f"2. The genre with the highest average user rating is "
    f"{highest_rated_genre} with a rating of "
    f"{highest_rated_genre_score}/5."
)

print(
    f"3. The most watched movie is Movie {most_popular_movie} "
    f"with {most_popular_movie_views} viewing events."
)

print(
    f"4. The highest-rated movie in the movie dataset is "
    f"Movie {highest_rated_movie} with a rating of "
    f"{highest_rated_movie_score}/10."
)

print(
    f"5. The most active user is User {most_active_user} "
    f"with {most_active_user_views} viewing events."
)


# --------------------------------------------------
# SAVE ANALYSIS RESULTS
# --------------------------------------------------

genre_analysis.to_csv("analysis_genres.csv")
genre_views.to_csv("analysis_genre_views.csv", index=False)
genre_user_ratings.to_csv("analysis_genre_ratings.csv", index=False)
user_stats.to_csv("analysis_user_stats.csv", index=False)
movie_performance.to_csv("analysis_movie_performance.csv", index=False)
age_analysis.to_csv("analysis_age_groups.csv")

print("\nAnalysis completed successfully.")
print("Analysis result files have been created.")