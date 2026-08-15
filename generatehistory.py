import json
import random
from datetime import datetime, timedelta

import pandas as pd


with open("user_data.json", "r") as file:
    users = json.load(file)

movies = pd.read_csv("movies.csv")

movie_ids = movies["movie_id"].tolist()

viewing_history = []

end_date = datetime.now()
start_date = end_date - timedelta(days=30)

for user in users:
    user_id = user["user_id"]

    number_of_views = random.randint(5, 20)

    selected_movies = random.sample(
        movie_ids,
        min(number_of_views, len(movie_ids))
    )

    for movie_id in selected_movies:
        random_seconds = random.randint(
            0,
            int((end_date - start_date).total_seconds())
        )

        timestamp = start_date + timedelta(
            seconds=random_seconds
        )

        viewing_history.append({
            "user_id": user_id,
            "movie_id": movie_id,
            "rating": random.randint(1, 5),
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })


viewing_history_df = pd.DataFrame(viewing_history)

viewing_history_df.to_csv(
    "viewing_history.csv",
    index=False
)

print("Data generation completed successfully.")
print(f"Created {len(viewing_history_df)} viewing events.")
print("Saved to viewing_history.csv.")