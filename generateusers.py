import json
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

number_of_users = 1000
number_of_movies = 1000

genres = [
    "Action",
    "Comedy",
    "Drama",
    "Horror",
    "Sci-Fi"
]

first_names = [
    "John", "Emma", "Michael", "Sophia", "William", "Olivia",
    "James", "Ava", "Alexander", "Isabella", "Daniel", "Mia",
    "Matthew", "Charlotte", "Joseph", "Amelia", "David",
    "Harper", "Jackson", "Evelyn", "Lucas", "Abigail"
]

users = []

for user_id in range(1, number_of_users + 1):
    name = random.choice(first_names)
    age = random.randint(18, 65)

    preferences = random.sample(
        genres,
        random.randint(1, 3)
    )

    watch_history = []

    for movie_id in random.sample(
        range(1, number_of_movies + 1),
        random.randint(2, 8)
    ):
        watch_history.append({
            "movie_id": movie_id,
            "rating": random.randint(1, 5)
        })

    users.append({
        "user_id": user_id,
        "name": name,
        "age": age,
        "preferences": preferences,
        "watch_history": watch_history
    })

with open(BASE_DIR / "user_data.json", "w", encoding="utf-8") as file:
    json.dump(users, file, indent=4)

print(f"Created {len(users)} users.")
print("Saved to user_data.json.")