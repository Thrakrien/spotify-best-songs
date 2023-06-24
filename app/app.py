import streamlit as st
import pandas as pd
import pickle
from PIL import Image
from st_files_connection import FilesConnection

# Buscando o pickle do modelo
with open(r'C:\Users\calebe.albertino\Desktop\Dinamica\notebooks\reg.pkl','rb') as file:
    model = pickle.load(file)

conn = st.experimental_connection('s3', type=FilesConnection)
model = conn.read("s3://models-portifolio/spotify-top-songs/reg.pkl")

# Salvando os dados em cache
@ st.cache_data

def predict(year, bpm, energy,
            danceability, dB,
            liveness, valence,
            duration, acousticness,
            speechiness):
    
    prediction = model.predict(pd.DataFrame([[year, bpm, energy,
                                              danceability, dB, liveness,
                                              valence, duration, acousticness,
                                              speechiness]], columns=[
                                                  'year', 'bpm', 'energy',
                                                  'danceability', 'dB', 'liveness',
                                                  'valence', 'duration', 'acousticness',
                                                  'speechiness']))
    return prediction


image = Image.open(r"C:\Users\calebe.albertino\Pictures\logo-spotify-verde-PNG.png")


st.image(image)
st.title('Popularidade da Música - Spotify')


st.markdown(
    """
    **👈 Selecione as variaveis ao lado!**
"""
)

st.sidebar.success("Defina as variáveis abaixo:")

year = st.sidebar.number_input('Ano da Música:', min_value=1500, max_value=2030, value=2023)

bpm = st.sidebar.number_input('BPM da música:', min_value=10,max_value=100000, value=100)

energy = st.sidebar.number_input('Energia:', min_value=10,max_value=1000,value=100)

danceability = st.sidebar.number_input('Taxa Dança:', min_value=10,max_value=1000,value=100)

dB = st.sidebar.number_input('Taxa Barulho:', min_value=-30, max_value=0, value=-5)

liveness = st.sidebar.number_input('Taxa Ao Vivo:', min_value=0.1, max_value=100.0, value=1.0)

valence = st.sidebar.number_input('Taxa Humor Positivo:', min_value=0.0, max_value=200.0, value=10.0)

duration = st.sidebar.number_input('Duração (s):', min_value=0, max_value=90000000, value=150)

acousticness = st.sidebar.number_input('Taxa Acústica:', min_value=0.0, max_value=200.0, value=10.0)

speechiness = st.sidebar.number_input('Taxa Cantada:', min_value=0.0, max_value=200.0, value=10.0)



if st.button('Popularidade da Música'):
    popularity = predict(year, bpm, energy,danceability,
                    dB, liveness,valence, duration,
                    acousticness,speechiness)
    st.success(f'A popularidade da música é: {popularity[0]:.2f}')