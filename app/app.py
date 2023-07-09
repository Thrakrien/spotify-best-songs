import streamlit as st
import pandas as pd
import os
import pickle
import boto3
from io import BytesIO
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

# Conexão com o S3 para consumo do artefato do modelo
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv('ACCESS_KEY'),
    aws_secret_access_key=os.getenv('SECRET_KEY')
)

# Utilizando o dotenv para ocultar as credenciais da API
load_dotenv(r'D:\Estudos\Codes\spotify-best-songs\notebooks\.env')
client_id=os.getenv('CLIENT_ID')
client_secret=os.getenv('CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id= client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

# Definindo o nome do bucket e o artefato
response = s3_client.get_object(Bucket = 'models-portifolio', Key = 'spotify-top-songs/reg_2.pkl')
file_content = response['Body'].read()

# Carregando o modelo
model = pickle.load(BytesIO(file_content))

#@ st.cache_data

# Criando a função search_music para buscar as musicas
def search_music(music):
    """
    Realiza a busca da musica que deseja-se realizar a predição da
    popularidade.

    Args:
        music (string): Texto de busca da música a ser buscada.
    
    Returns:
        None
    """
    choosed_music = sp.search(q=music,type='track')

    # Musica buscada salva em DataFrame formatada para realizar a predição.
    music_df = pd.DataFrame.from_dict(choosed_music,orient='index')
    music_df = music_df.explode('items')
    music_df = music_df['items'][0]
    
    song_id = music_df['id']

    # Definindo o primeiro resultado da pesquisa como o dado de entrada
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

# Definindo o design do Streamlit
st.image(r"https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_RGB_Green.png")
st.title('Popularidade da Música - Spotify')


st.markdown(
    """
    O app em questão realiza a predição da popularidade da música pesquisada abaixo.
    """
)

input = st.text_area('Insira uma música', 'Digite aqui')
with st.spinner('Calculando...'):
    output = search_music(input)


if st.button('Prever a Popularidade:'):
    st.success(f'A popularidade da música é: {output[0]:.2f}')