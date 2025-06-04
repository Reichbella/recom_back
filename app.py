from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app) 

GENRES = [
    "Action", "Adventure", "Animation", "Children's", "Comedy", "Crime",
    "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical",
    "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western", "(unknown)"
]

def load_movielens_data():
    columns = ['user_id', 'movie_id', 'rating', 'timestamp']
    ratings = pd.read_csv('https://files.grouplens.org/datasets/movielens/ml-100k/u.data',
                         sep='\t', names=columns)
    movie_columns = ['movie_id', 'title', 'release_date', 'video_release_date', 'IMDb_URL'] + [f'genre_{i}' for i in range(19)]
    movies = pd.read_csv('https://files.grouplens.org/datasets/movielens/ml-100k/u.item',
                         sep='|', names=movie_columns, encoding='latin-1')
    user_movie_matrix = ratings.pivot(index='user_id', columns='movie_id', values='rating')
    return user_movie_matrix, movies

def compute_user_similarity(user_movie_matrix):
    user_movie_matrix_filled = user_movie_matrix.fillna(0)
    similarity = cosine_similarity(user_movie_matrix_filled)
    similarity_df = pd.DataFrame(similarity, index=user_movie_matrix.index, columns=user_movie_matrix.index)
    return similarity_df

def precompute_recommendations(user_movie_matrix, similarity_df, movies, top_n=5):
    recommendations = {}
    user_id = 1
    similar_users = similarity_df[user_id].sort_values(ascending=False)[1:]
    similar_users = similar_users[similar_users > 0].index
    unrated_movies = user_movie_matrix.columns[user_movie_matrix.loc[user_id].isna()]

    predictions = {}
    for movie in unrated_movies:
        weighted_sum = 0
        similarity_sum = 0
        for sim_user in similar_users:
            if not np.isnan(user_movie_matrix.loc[sim_user, movie]):
                sim_score = similarity_df.loc[user_id, sim_user]
                weighted_sum += sim_score * user_movie_matrix.loc[sim_user, movie]
                similarity_sum += sim_score
        if similarity_sum > 0:
            predictions[movie] = weighted_sum / similarity_sum

    for genre_idx, genre in enumerate(GENRES):
        genre_col = f'genre_{genre_idx}'
        genre_movies = movies[movies[genre_col] == 1]['movie_id']
        filtered_predictions = {movie_id: score for movie_id, score in predictions.items() if movie_id in genre_movies.values}
        top_recs = sorted(filtered_predictions.items(), key=lambda x: x[1], reverse=True)[:top_n]
        recommendations[genre] = [
            {"title": movies[movies['movie_id'] == movie_id]['title'].iloc[0], "score": round(score, 2)}
            for movie_id, score in top_recs
        ]
    return recommendations

user_movie_matrix, movies = load_movielens_data()
similarity_df = compute_user_similarity(user_movie_matrix)
precomputed_recommendations = precompute_recommendations(user_movie_matrix, similarity_df, movies)

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    genre = data.get('genre')
    if not genre:
        return jsonify({"error": "Le genre est requis"}), 400
    if genre not in precomputed_recommendations:
        return jsonify({"error": f"Genre {genre} non valide. Choisissez parmi : {', '.join(GENRES)}"}), 400
    return jsonify({"recommendations": precomputed_recommendations[genre]})

if __name__ == '__main__':
    app.run(debug=True, port=5000)