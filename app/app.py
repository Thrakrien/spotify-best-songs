import streamlit as st
import pandas as pd
import os
import pickle
import boto3
from io import BytesIO
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

# Configurar as credenciais do AWS
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv('ACCESS_KEY'),
    aws_secret_access_key=os.getenv('SECRET_KEY')
)


load_dotenv(r'D:\Estudos\Codes\spotify-best-songs\notebooks\.env')
client_id=os.getenv('CLIENT_ID')
client_secret=os.getenv('CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id= client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

response = s3_client.get_object(Bucket = 'models-portifolio', Key = 'spotify-top-songs/reg_2.pkl')
file_content = response['Body'].read()


model = pickle.load(BytesIO(file_content))

@ st.cache_data

def search_music(music):
    choosed_music = sp.search(q=music,type='track')
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
    prediction = model.predict(data_clean)
    return prediction


st.image(r"https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_RGB_Green.png")
st.title('Popularidade da Música - Spotify')


st.markdown(
    """
    **👈 Selecione as variaveis ao lado!**
"""
)

input = st.text_area('Insira uma música', 'Digite aqui')
with st.spinner('Fazendo coisas de AI'):
    output = search_music(input)


if st.button('Popularidade da Música'):
    st.success(f'A popularidade da música é: {output[0]:.2f}')