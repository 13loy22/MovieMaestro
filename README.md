# 🎬 AI-Based Movie Personalization Engine

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Tableau](https://img.shields.io/badge/Tableau-Dashboard-orange.svg)](https://www.tableau.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

## 📖 Overview
Welcome to the **AI-Based Movie Personalization Engine**. This project is a collaborative, two-person initiative designed to deliver highly accurate, individualized movie recommendations. By leveraging a hybrid approach that combines collaborative filtering and content-based metadata, this engine predicts user preferences and serves tailored cinematic suggestions.

## ✨ Features
- **Hybrid Recommendation Algorithm:** Combines collaborative filtering (user-item interactions) with content-based filtering (genre, director, cast, and plot).
- **Robust Data Pipeline:** Efficiently processes large datasets of movie ratings and metadata using optimized dataframes.
- **Interactive Visualization:** Includes a dedicated analytics dashboard to monitor recommendation accuracy, catalog trends, and user engagement metrics.
- **Scalable Database Architecture:** Utilizes a custom star schema optimized for fast analytical queries and secure view generation.

## 🛠️ Tech Stack
- **Language:** Python (Pandas, NumPy, Scikit-Learn)
- **Visualization:** Tableau Public
- **Version Control:** Git & GitHub (Feature-branch workflow)

## 🚀 Installation & Setup

### Prerequisites
- Python 3.9+
- Git

### Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/movie-personalization-engine.git
   cd movie-personalization-engine
   ```

## 🧠 Model Architecture & Data Flow
Our engine processes data in three main stages:
1. **Data Ingestion & Cleaning:** Raw datasets (e.g., MovieLens, TMDB) are ingested, cleaned via automated Python scripts, and mapped into our PostgreSQL database.
2. **Feature Engineering:** We extract TF-IDF vectors for text-heavy features (like overviews) and encode categorical metadata to build comprehensive item profiles.
3. **Training & Inference:** A matrix factorization model computes latent user/item factors, dynamically generating a top-N recommendation list for any given user ID.

## 📊 Analytics Dashboard
We maintain a connected **Tableau** dashboard to visualize:
- Decadal shifts in genre popularity and release trends.
- Recommendation hit rates and algorithmic precision metrics.
- User rating distributions across different demographic clusters.

## 🤝 Collaboration Workflow
As a two-person development team, we divide responsibilities to ensure smooth integration:
- **Developer 1 (Data & Analytics):** Focuses on the PostgreSQL data pipeline, schema design, exploratory data analysis (EDA), and Tableau visual reporting.
- **Developer 2 (ML & Engineering):** Focuses on algorithmic model training in Python, feature engineering, and recommendation endpoint development.

*Both developers enforce strict code reviews via GitHub Pull Requests before merging to the `main` branch.*

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
