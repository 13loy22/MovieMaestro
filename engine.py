import json
import pandas as pd


movies = pd.read_csv("processed_movies.csv")
history = pd.read_csv("clean_viewing_history.csv")

with open("clean_users.json", "r") as file:
    users = json.load(file)


def recommend_movies(user_id, number_of_recommendations=5):

    user = next((u for u in users if u["user_id"] == user_id), None)

    if user is None:
        print(f"User {user_id} was not found.")
        return pd.DataFrame()

    preferences = user.get("preferences", [])

    user_history = history[
        history["user_id"] == user_id
    ].copy()

    watched_movies = set(user_history["movie_id"])

    recommendations = movies[
        ~movies["movie_id"].isin(watched_movies)
    ].copy()

    if recommendations.empty:
        return pd.DataFrame()

    # Connect viewing history with movie genres
    user_history_with_genres = user_history.merge(
        movies[["movie_id", "genre"]],
        on="movie_id",
        how="left"
    )

    # Calculate user's average rating for each genre
    genre_ratings = (
        user_history_with_genres
        .groupby("genre")["rating"]
        .mean()
        .to_dict()
    )

    # Overall user rating
    if len(user_history) > 0:
        overall_rating = user_history["rating"].mean()
    else:
        overall_rating = 3.0

    # User preference
    recommendations["preferred_genre"] = recommendations[
        "genre"
    ].apply(
        lambda genre: 1 if genre in preferences else 0
    )

    # User's historical rating for each genre
    def user_genre_score(genre):

        if genre in genre_ratings:
            return genre_ratings[genre] / 5

        return overall_rating / 5

    recommendations["user_genre_score"] = recommendations[
        "genre"
    ].apply(user_genre_score)

    # Movie quality
    recommendations["movie_quality"] = (
        recommendations["rating"] / 10
    )

    # Movie popularity
    max_views = recommendations["viewing_count"].max()

    if max_views > 0:
        recommendations["popularity"] = (
            recommendations["viewing_count"] / max_views
        )
    else:
        recommendations["popularity"] = 0

    # Main recommendation score
    recommendations["recommendation_score"] = (
        recommendations["preferred_genre"] * 0.55
        + recommendations["user_genre_score"] * 0.20
        + recommendations["movie_quality"] * 0.15
        + recommendations["popularity"] * 0.10
    )

    # Preferred genres are ranked first
    recommendations = recommendations.sort_values(
        by=[
            "preferred_genre",
            "recommendation_score"
        ],
        ascending=[False, False]
    )

    result = recommendations[
        [
            "movie_id",
            "genre",
            "rating",
            "viewing_count",
            "recommendation_score"
        ]
    ].head(number_of_recommendations)

    return result


# Test the engine with User 1

user_id = 1

recommendations = recommend_movies(
    user_id,
    number_of_recommendations=5
)

print(f"Recommended movies for user {user_id}")
print()

if recommendations.empty:
    print("No recommendations available.")
else:
    print(recommendations.to_string(index=False))