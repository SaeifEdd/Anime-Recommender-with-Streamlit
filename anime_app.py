import streamlit as st
import pandas as pd
import requests
import pickle
import numpy as np


anime = pickle.load(open('anime.pkl' , 'rb'))
anime_list = anime['name'].values
similarity = pickle.load(open('Csimilarity.pkl' , 'rb'))


#Streamlit deployment
st.title('Anime Recommendation System')
selected_anime = st.selectbox('Enter the name of anime', (anime_list))



def fetch_poster(anime_id):
    url = f"https://api.jikan.moe/v4/anime/{anime_id}/pictures"
    response = requests.get(url)
    data = response.json()
    
    # Check if 'data' key exists in the JSON response and is not empty
    if "data" in data and data["data"]:
        # If 'data' exists and is not empty, get the first image URL
        poster_data = data["data"][0]["jpg"]
        
        # Check if 'large_image_url' key exists in the poster data
        if "large_image_url" in poster_data and poster_data["large_image_url"]:
            poster_url = poster_data["large_image_url"]
            return poster_url
        else:
            # If 'large_image_url' is missing or empty, return None or a default image URL
            return None
    else:
        # If 'data' is missing or empty, return None or a default image URL
        return None
    
    

def recommend(anime_name):
    
    index = np.where(anime['name'] == anime_name)[0][0]
    similar_anime = sorted(enumerate(similarity[index]), key = lambda x : x[1], reverse = True)[1:6]
    
    recommended_animes = []
    animes_posters = []
    
    for i in similar_anime:
        
        recommended_animes.append(anime['name'][i[0]])
        anime_id = anime.iloc[i[0]].anime_id
        animes_posters.append(fetch_poster(anime_id))
    
    return recommended_animes, animes_posters


#https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR60O2-muWvwgWvwmzklx-IydP5j0NZsLnHpg&usqp=CAU
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://c4.wallpaperflare.com/wallpaper/173/428/954/anime-hunter-x-hunter-killua-zoldyck-wallpaper-preview.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()



if st.button('Recommend'):
    names , posters = recommend(selected_anime)

    col1 , col2 , col3 , col4 , col5 = st.columns(5)
    
    with col1:
        st.image(posters[0], width=150, use_column_width='always', output_format='auto')
        st.markdown("<p style='color: black;'>{}</p>".format(names[0]), unsafe_allow_html=True)

    with col2:
        st.image(posters[1], width=150, use_column_width='always', output_format='auto')
        st.markdown("<p style='color: black;'>{}</p>".format(names[1]), unsafe_allow_html=True)

    with col3:
        st.image(posters[2], width=150, use_column_width='always', output_format='auto')
        st.markdown("<p style='color: black;'>{}</p>".format(names[2]), unsafe_allow_html=True)

    with col4:
        st.image(posters[3], width=150, use_column_width='always', output_format='auto')
        st.markdown("<p style='color: black;'>{}</p>".format(names[3]), unsafe_allow_html=True)

    with col5:
        st.image(posters[4], width=150, use_column_width='always', output_format='auto')
        st.markdown("<p style='color: black;'>{}</p>".format(names[4]), unsafe_allow_html=True)
        
        
st.markdown(
    """
    <style>
    .stApp > div[data-baseweb="flex-grid-container"] {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        grid-gap: 100px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


