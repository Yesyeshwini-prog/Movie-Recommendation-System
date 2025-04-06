import pickle
import streamlit as st
import requests
import pandas as pd
import base64
from pathlib import Path

# Function to encode the image
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


# Load background image
def load_background_image():
    image_file = 'bg_image.jpg'
    if not Path(image_file).exists():
        st.error(f"Background image file '{image_file}' not found. Please check the file path.")
        return None
    return get_base64_of_bin_file(image_file)


background_image = load_background_image()

# Custom HTML and CSS for background image and enhanced UI
background_style = f"""
background-image: url("data:image/jpg;base64,{background_image}");
background-size: cover;
background-position: center;
""" if background_image else "background-color: #000;"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    body {{
        font-family: 'Roboto', sans-serif;
        color: white;
    }}

    .stApp {{
        {background_style}
    }}

    .overlay {{
        background: rgba(0, 0, 0, 0.7);
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
    }}

    h1 {{
        text-align: center;
        color: #FFD700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }}

    .movie-card {{
        background: rgba(0, 0, 0, 0.7);
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
        transition: transform 0.3s ease;
    }}

    .movie-card:hover {{
        transform: scale(1.05);
    }}

    .movie-title {{
        font-weight: bold;
        margin-bottom: 5px;
    }}

    .movie-info {{
        font-size: 0.9em;
        margin-bottom: 5px;
    }}

    .movie-overview {{
        font-size: 0.8em;
        font-style: italic;
    }}
</style>

<div class="overlay"></div>
""", unsafe_allow_html=True)

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=f8047a31d1a1cde423bb0f59f7f5b24d&language=en.US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('C:/Users/Mary Tejaswini/PycharmProjects/IR Project/movie_dict (1).pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('C:/Users/Mary Tejaswini/PycharmProjects/IR Project/similarity.pkl','rb'))


st.title('Movie Recommendation System')

selected_movie_name = st.selectbox('Type or select movies from the dropdown!', movies['title'].values)

if st.button('Show Recommendation'):
    names,posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])

# Custom HTML and CSS for background image and enhanced UI
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    body {{
        font-family: 'Roboto', sans-serif;
        color: white;
    }}

    .stApp {{
        background-image: url("data:image/jpg;base64,{background_image}");
        background-size: cover;
        background-position: center;
    }}

    .overlay {{
        background: rgba(0, 0, 0, 0.7);
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
    }}

    h1 {{
        text-align: center;
        color: #FFD700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }}

    .movie-card {{
        background: rgba(0, 0, 0, 0.7);
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
        transition: transform 0.3s ease;
    }}

    .movie-card:hover {{
        transform: scale(1.05);
    }}

    .movie-title {{
        font-weight: bold;
        margin-bottom: 5px;
    }}

    .movie-info {{
        font-size: 0.9em;
        margin-bottom: 5px;
    }}

    .movie-overview {{
        font-size: 0.8em;
        font-style: italic;
    }}
</style>

<div class="overlay"></div>
""", unsafe_allow_html=True)




# User rating system (simplified for demonstration)
st.sidebar.title("Rate this movie")
user_rating = st.sidebar.slider("How would you rate this movie?", 1, 10, 5)
if st.sidebar.button("Submit Rating"):
    st.sidebar.success(f"You rated {selected_movie_name} {user_rating}/10!")

# Add some space at the bottom
st.markdown("<br><br>", unsafe_allow_html=True)
