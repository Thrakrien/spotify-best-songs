import streamlit as st
import pandas as pd
import os
import pickle
from PIL import Image
import boto3
from io import BytesIO
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Configurar as credenciais do AWS
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv('ACCESS_KEY'),
    aws_secret_access_key=os.getenv('SECRET_KEY')
)

client_id='1ea081e3c4d04a178150f5287edcfb7f'
client_secret='2788f6b0446a47fca4de16f370fc98b8'

client_credentials_manager = SpotifyClientCredentials(client_id= client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

response = s3_client.get_object(Bucket = 'models-portifolio', Key = 'spotify-top-songs/reg_2.pkl')
file_content = response['Body'].read()


model = pickle.load(BytesIO(file_content))

@ st.cache_data

def predict(energy,
            danceability,
            liveness, valence,
            acousticness,
            speechiness):
    
    prediction = model.predict(pd.DataFrame([[danceability, energy, speechiness,
                                              acousticness, liveness, valence]], columns=[
                                                  'year', 'bpm', 'energy',
                                                  'danceability', 'dB', 'liveness',
                                                  'valence', 'duration', 'acousticness',
                                                  'speechiness']))
    return prediction

def search_music(music):
    choosed_music = sp.search(q=str(music),type='track')
    music_df = pd.DataFrame.from_dict(choosed_music,orient='index')
    music_df = music_df.explode('items')
    music_df = music_df['items'][0]
    
    song_id = music_df['id']

    song_info = sp.audio_features(song_id)[0]
    
    selected_data = {
    'danceability': song_info['danceability'],
    'energy': song_info['energy'],
    'speechiness': song_info['speechiness'],
    'acousticness': song_info['acousticness'],
    'liveness': song_info['liveness'],
    'valence':song_info['valence']
    }
    
    data_clean = pd.DataFrame(selected_data,index=[0])
    return data_clean

#image = Image.open(r"https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_RGB_Green.png")


st.image(r"https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_RGB_Green.png")
st.title('Popularidade da Música - Spotify')


st.markdown(
    """
    **👈 Selecione as variaveis ao lado!**
"""
)

st.sidebar.success("Digite o nome da música abaixo: ")

input = st.text_area('Insira uma música', 'Digite aqui')
with st.spinner('Fazendo coisas de AI'):
    output = predict(search_music(input))

#title = st.text_input('Movie title', 'Life of Brian')

# year = st.sidebar.number_input('Ano da Música:', min_value=1500, max_value=2030, value=2023)

# bpm = st.sidebar.number_input('BPM da música:', min_value=10,max_value=100000, value=100)

# energy = st.sidebar.number_input('Energia:', min_value=10,max_value=1000,value=100)

# danceability = st.sidebar.number_input('Taxa Dança:', min_value=10,max_value=1000,value=100)

# dB = st.sidebar.number_input('Taxa Barulho:', min_value=-30, max_value=0, value=-5)

# liveness = st.sidebar.number_input('Taxa Ao Vivo:', min_value=0.1, max_value=100.0, value=1.0)

# valence = st.sidebar.number_input('Taxa Humor Positivo:', min_value=0.0, max_value=200.0, value=10.0)

# duration = st.sidebar.number_input('Duração (s):', min_value=0, max_value=90000000, value=150)

# acousticness = st.sidebar.number_input('Taxa Acústica:', min_value=0.0, max_value=200.0, value=10.0)

# speechiness = st.sidebar.number_input('Taxa Cantada:', min_value=0.0, max_value=200.0, value=10.0)



if st.button('Popularidade da Música'):
    popularity = predict(search_music(input))
    st.success(f'A popularidade da música é: {popularity[0]:.2f}')