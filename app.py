
import streamlit as st
import joblib as j
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Function to fetch image URL from MyAnimeList
def fetch_image_url(anime_id):
    url = f"https://myanimelist.net/anime/{anime_id}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        image_tag = soup.find('img', {'class': 'ac'})  # You need to inspect the page source to find the appropriate class
        if image_tag:
            image_url = image_tag['data-src']
            return image_url
    return None

# Function to recommend anime
def recommend(anime):
    anime_index = animes[animes['English'] == anime].index[0]
    similar_anime_indices = sorted(list(enumerate(related[anime_index])), reverse=True, key=lambda x: x[1])[0:3]
    anime_recommendations = []
    for idx, similarity in similar_anime_indices:
        similar_anime_id = animes.iloc[idx]['ID']  # Get the similar anime ID
        similar_anime_name = animes.iloc[idx]['English']  # Get the similar anime name
        similar_anime_link = f"https://myanimelist.net/anime/{similar_anime_id}"  # Construct the link using anime_id
        similar_anime_image = fetch_image_url(similar_anime_id)  # Fetch the image URL
        if similar_anime_image:
            anime_recommendations.append((similar_anime_name, similar_anime_link, similar_anime_image))
    return anime_recommendations

# Load data
ani_lis = j.load(open('anime_li', 'rb'))
related = j.load(open('similarity', 'rb'))
animes = pd.DataFrame(ani_lis)

# Custom CSS
custom_css = """
/* Apply custom styles to the "Details" link */
.stButton a {
    background-color: #3498db;
    color: white;
    text-decoration: none;
    padding: 8px 16px;
    border-radius: 15px; /* Decrease border radius for a more oval shape */
    display: inline-block;
    text-align: center;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.3s ease, color 0.3s ease;
}

.stButton a:hover {
    background-color: #e74c3c; /* Change hover background color */
    transform: scale(1.05);
    color: white; /* Change hover text color */
}

/* Apply styles to the image title */
.image-title {
    text-align: center;
    font-weight: bold;
    margin-top: 10px;
}

/* Center the contents of each container */
.stContainer {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 15px;
    padding: 15px;
    border: 1px solid #ccc;
    border-radius: 10px;
    transition: box-shadow 0.3s ease;
}

/* Add a subtle shadow on container hover */
.stContainer:hover {
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
}

/* Apply a hover effect to containers */
.stContainer:hover {
    transform: translateY(-5px);
    transition: transform 0.3s ease;
    border: 2px solid #3498db;
    border-radius: 12px;
}

/* Apply a hover effect to images */
.stContainer:hover img {
    transform: scale(1.05);
    transition: transform 0.3s ease;
}

/* Center the buttons within the container */
.stButton {
    display: flex;
    justify-content: center;
    margin-top: 15px;

}
/* Apply styles to the "Show Recommendation" button */
.stButton button {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 15px;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.3s ease, color 0.3s ease;
}

.stButton button:hover {
    background-color: #e74c3c;
    transform: scale(1.05);
    color: white;
}

"""

# Streamlit app
st.set_page_config(page_title="Anime Recommender System",page_icon='🌟')
st.title("🌟Anime Recommender System")
st.markdown('<style>body { background-color: #000000; }</style>', unsafe_allow_html=True)
st.markdown('<div style="padding: 20px;">', unsafe_allow_html=True)
st.markdown('<style>.stApp { background-color: #000000; }</style>', unsafe_allow_html=True)

s_anime = st.selectbox("Search for Related Anime", animes['English'].values)

# Import your custom CSS styles
st.markdown('<style>' + custom_css + '</style>', unsafe_allow_html=True)


custom_css = """
/* Rest of your CSS rules... */

/* Apply styles to the "Show Recommendation" button */
.stButton button {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 15px;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.3s ease, color 0.3s ease;
}

.stButton button:hover {
    background-color: #e74c3c;
    transform: scale(1.05);
    color: white;
}
"""



# Rest of your app...

if st.button('Show Recommendation'):
    recommendations = recommend(s_anime)
    
    col1, col2, col3 = st.columns(3)
    recommendations = recommend(s_anime)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container():
            st.image(recommendations[0][2], width=150, use_column_width=True)
            st.markdown(f"<p class='image-title'>{recommendations[0][0]}</p>", unsafe_allow_html=True)
            st.markdown(f"<div class='stButton'><a href='{recommendations[0][1]}' target='_blank'><i class='fas fa-info-circle'></i> Details</a></div>", unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.image(recommendations[1][2], width=150, use_column_width=True)
            st.markdown(f"<p class='image-title'>{recommendations[1][0]}</p>", unsafe_allow_html=True)
            st.markdown(f"<div class='stButton'><a href='{recommendations[1][1]}' target='_blank'><i class='fas fa-info-circle'></i> Details</a></div>", unsafe_allow_html=True)
    
    with col3:
        with st.container():
            st.image(recommendations[2][2], width=150, use_column_width=True)
            st.markdown(f"<p class='image-title'>{recommendations[2][0]}</p>", unsafe_allow_html=True)
            st.markdown(f"<div class='stButton'><a href='{recommendations[2][1]}' target='_blank'><i class='fas fa-info-circle'></i> Details</a></div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
