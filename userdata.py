import json
import random

# Number of users to generate
number_of_users = 1000
number_of_movies = 1000

# Aligning with the genres from your movie generation code
genres = ["Action", "Comedy", "Drama", "Horror", "Sci-Fi"]

# A list of sample names to draw from
first_names = [
    "John", "Emma", "Michael", "Sophia", "William", "Olivia", "James", "Ava",
    "Alexander", "Isabella", "Daniel", "Mia", "Matthew", "Charlotte", "Joseph",
    "Amelia", "David", "Harper", "Jackson", "Evelyn", "Lucas", "Abigail"
]

user_data = []

for _ in range(number_of_users):
    # 1. Generate basic demographics
    name = random.choice(first_names)
    age = random.randint(18, 65)

    # 2. Generate preferences (1 to 3 random genres)
    num_preferences = random.randint(1, 3)
    preferences = random.sample(genres, num_preferences)

    # 3. Generate watch history (between 2 and 8 movies per user)
    watch_history = []
    num_watched = random.randint(2, 8)

    for _ in range(num_watched):
        movie_id = random.randint(1, number_of_movies)

        watch_history.append({
            "movie": f"Movie_{movie_id}",
            "genre": random.choice(genres),
            "rating": random.randint(1, 5) # Assuming a 1-5 star rating scale for users
        })

    # 4. Construct the user dictionary
    user = {
        "name": name,
        "age": age,
        "preferences": preferences,
        "watch_history": watch_history
    }

    user_data.append(user)

# Print the first 2 users to the console to verify the format
print(json.dumps(user_data[:2], indent=4))

# Export all 1000 users to a JSON file
with open("user_data.json", "w") as file:
    json.dump(user_data, file, indent=4)

print(f"\nSuccessfully generated {number_of_users} users and saved to 'user_data.json'.")