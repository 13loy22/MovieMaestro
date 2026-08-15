import json
import random
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / "user_data.json", "r", encoding="utf-8") as file:
    users = json.load(file)

movies = pd.read_csv(BASE_DIR / "movies.csv")

movie_ids = movies["movie_id"].tolist()

viewing_history = []

for user in users:
    user_id = user["user_id"]

    number_of_views = random.randint(5, 20)

    selected_movies = random.sample(
        movie_ids,
        min(number_of_views, len(movie_ids))
    )

    for movie_id in selected_movies:
        viewing_history.append({
            "user_id": user_id,
            "movie_id": movie_id,
            "rating": random.randint(1, 5)
        })

viewing_history_df = pd.DataFrame(viewing_history)

viewing_history_df.to_csv(
    BASE_DIR / "viewing_history.csv",
    index=False
)

print(f"Created {len(viewing_history_df)} viewing events.")
print("Saved to viewing_history.csv.")