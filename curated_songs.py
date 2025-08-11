import os
import spotipy
import pandas as pd
from dotenv import load_dotenv
import numpy as np
from spotipy.oauth2 import SpotifyOAuth
from voyager import Index, Space

load_dotenv() # loading env variables 

# debugging
if not all([
    os.getenv('SPOTIFY_CLIENT_ID'),
    os.getenv('SPOTIFY_CLIENT_SECRET'),
    os.getenv('SPOTIFY_REDIRECT_URI')]):
    raise ValueError("Missing Spotify credientials in .env file")

scope = " ".join([
    'user-library-read',
    'playlist-read-private',
    'user-top-read',
    'user-read-recently-played'
])

try:
    # Spotify API
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(

        client_id=os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
        redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
        scope=scope,
        open_browser=True # opens auth page
    ))
    # verify connection
    sp.current_user()
except Exception as e:
    print(f"Authentication Error: {str(e)}")
    raise


def get_audio_features(track_ids):
    # getting audio features for a list of track IDs
    features = sp.audio_features(track_ids)
    return features

def get_liked_songs(limit=50):
    # getting users liked songs
    results = sp.current_user_saved_tracks(limit=limit)
    tracks = results['items']

    track_data = []
    for track in tracks:
        track_info = track['track']
        track_data.append({
            'id': track_info['id'],
            'name': track_info['name'],
            'artists': track_info['artists'][0]['name']
        })

    return track_data

# getting liked songs, and their features
liked_songs = get_liked_songs(limit=50)
track_ids = [song['id'] for song in liked_songs]
audio_features = get_audio_features(track_ids)

# creatung feature vectors
features_to_use = ['loudness, energy, daceability, '
                    'valence, tempo, acousticness, liveness, speechiness']

songs = {}

for i, features in enumerate(audio_features):
    # if feature exist
    if features:
        vector = [features[feat] for feat in features_to_use]
        songs[i] = vector

# Building inde with higher M value
index = Index(Space.Euclidean, num_dimensions=5, M=6)

# add songs
for song_id, features in songs.items():
    index.add_item(np.array(features, dtype=np.float32), id=song_id)

# get users taste vector from first two liked songs
liked_vectors = [songs[0], songs[1]]
taste_vector = np.mean(liked_vectors, axis=0)

# get 3 sings tailored to users taste
neighbors, distances = index.query(np.array(taste_vector, dtype=np.float32), k=3)

# priting recs
print("\nRecommended Songs:")
for neighbor_id in neighbors:
    song = liked_songs[neighbor_id]
    print(f"- {song['name']} by {song['artist']}")