import json
import pandas as pd


class RecommendationEngine:

    def __init__(self, movies_file, history_file, users_file):
        self.movies = pd.read_csv(movies_file)
        self.history = pd.read_csv(history_file)

        with open(users_file, "r") as file:
            self.users = json.load(file)

    def get_user(self, user_id):
        return next(
            (user for user in self.users if user["user_id"] == user_id),
            None
        )

    def get_user_history(self, user_id):
        return self.history[
            self.history["user_id"] == user_id
        ].copy()

    def calculate_genre_ratings(self, user_history):
        if user_history.empty:
            return {}

        user_history_with_genres = user_history.merge(
            self.movies[["movie_id", "genre"]],
            on="movie_id",
            how="left"
        )

        return (
            user_history_with_genres
            .groupby("genre")["rating"]
            .mean()
            .to_dict()
        )

    def calculate_genre_activity(self, user_history):
        if user_history.empty:
            return {}

        user_history_with_genres = user_history.merge(
            self.movies[["movie_id", "genre"]],
            on="movie_id",
            how="left"
        )

        return (
            user_history_with_genres["genre"]
            .value_counts()
            .to_dict()
        )

    def calculate_personal_rating_score(
        self,
        genre,
        genre_ratings,
        overall_rating
    ):
        if genre in genre_ratings:
            rating = genre_ratings[genre]
        else:
            rating = overall_rating

        if rating >= 4:
            return 1.0
        elif rating >= 3:
            return 0.6
        elif rating >= 2:
            return 0.3
        else:
            return 0.0

    def calculate_recommendation_score(
        self,
        recommendations,
        preferences,
        genre_ratings,
        genre_activity,
        overall_rating,
        history_size
    ):

        # User preference
        recommendations["preferred_genre"] = recommendations[
            "genre"
        ].apply(
            lambda genre: 1 if genre in preferences else 0
        )

        # User's historical rating for each genre
        recommendations["user_genre_score"] = recommendations[
            "genre"
        ].apply(
            lambda genre: (
                genre_ratings.get(genre, overall_rating) / 5
            )
        )

        # User activity by genre
        def calculate_activity_score(genre):

            activity_count = genre_activity.get(genre, 0)

            if activity_count >= 3:
                return 1.0
            elif activity_count >= 1:
                return 0.5
            else:
                return 0.0

        recommendations["activity_score"] = recommendations[
            "genre"
        ].apply(calculate_activity_score)

        # Personal rating behavior
        recommendations["personal_rating_score"] = recommendations[
            "genre"
        ].apply(
            lambda genre: self.calculate_personal_rating_score(
                genre,
                genre_ratings,
                overall_rating
            )
        )

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

        # Adapt scoring according to history size
        if history_size >= 5:
            preference_weight = 0.40
            genre_weight = 0.15
            activity_weight = 0.15
            personal_rating_weight = 0.10
            quality_weight = 0.10
            popularity_weight = 0.10

        elif history_size >= 1:
            preference_weight = 0.45
            genre_weight = 0.15
            activity_weight = 0.10
            personal_rating_weight = 0.10
            quality_weight = 0.10
            popularity_weight = 0.10

        else:
            preference_weight = 0.55
            genre_weight = 0.10
            activity_weight = 0.00
            personal_rating_weight = 0.00
            quality_weight = 0.20
            popularity_weight = 0.15

        # Main personalized recommendation score
        recommendations["recommendation_score"] = (
            recommendations["preferred_genre"]
            * preference_weight

            + recommendations["user_genre_score"]
            * genre_weight

            + recommendations["activity_score"]
            * activity_weight

            + recommendations["personal_rating_score"]
            * personal_rating_weight

            + recommendations["movie_quality"]
            * quality_weight

            + recommendations["popularity"]
            * popularity_weight
        )

        return recommendations

    def recommend_movies(
        self,
        user_id,
        number_of_recommendations=5
    ):

        user = self.get_user(user_id)

        if user is None:
            print(f"User {user_id} was not found.")
            return pd.DataFrame()

        preferences = user.get("preferences", [])

        user_history = self.get_user_history(user_id)

        watched_movies = set(user_history["movie_id"])

        recommendations = self.movies[
            ~self.movies["movie_id"].isin(watched_movies)
        ].copy()

        if recommendations.empty:
            return pd.DataFrame()

        genre_ratings = self.calculate_genre_ratings(
            user_history
        )

        genre_activity = self.calculate_genre_activity(
            user_history
        )

        if len(user_history) > 0:
            overall_rating = user_history["rating"].mean()
        else:
            overall_rating = 3.0

        recommendations = self.calculate_recommendation_score(
            recommendations,
            preferences,
            genre_ratings,
            genre_activity,
            overall_rating,
            len(user_history)
        )

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


# Create the recommendation engine
engine = RecommendationEngine(
    "processed_movies.csv",
    "clean_viewing_history.csv",
    "clean_users.json"
)


# Test the engine with Users 1 to 5
if __name__ == "__main__":

    for user_id in range(1, 6):

        recommendations = engine.recommend_movies(
            user_id,
            number_of_recommendations=5
        )

        print(f"USER {user_id}:")
        print()

        if recommendations.empty:
            print("No recommendations available.")
        else:
            print(recommendations.to_string(index=False))

        print()