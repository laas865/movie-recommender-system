import streamlit as st
import pickle
import pandas as pd
import requests
st.set_page_config(page_title="Movie Recommender", layout="wide")

netflix_css = """
<style>
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    
    h2, h3 {
        color: #E50914 !important;
    }
    [data-testid="stWidgetLabel"] p {
        font-size: 16px !important; 
    }
    /* Buttons */
    div.stButton > button {
        background-color: #E50914 !important;
        color: white !important;
        border: none !important;
    }

    /* Selectbox/Inputs */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #141414;
        color: white;
    }

    /* Movie Title Styling */
    .movie-title {
        color: white;
        font-size: 16px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
        height: 3rem;
        overflow: hidden;
    }
</style>
"""
st.markdown(netflix_css, unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #E50914;'>Movie Recommender System</h1>", unsafe_allow_html=True)
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

API_KEY = "5915cf81ed034415a0c271277e14c005"

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    try:
        response = requests.get(url, params={"api_key": API_KEY, "language": "en-US"}, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data.get("poster_path"):
            return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
    except Exception:
        pass
    return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movie_posters

selected_movie_name = st.selectbox(
    "Choose a movie you like:",
    movies['title'].values
)

if st.button("Recommend"):
    with st.spinner('Finding the best matches...'):
        names, posters = recommend(selected_movie_name)
    
    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.markdown(f"<div class='movie-title'>{name}</div>", unsafe_allow_html=True)
            st.image(poster, use_container_width=True)