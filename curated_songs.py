import pandas as pd
import numpy as np
from voyager import Index, Space
import time
from auth import get_spotify_clients

# get authenticated spotify clients
sp_user, sp_public = get_spotify_clients()


def get_top_tracks(limit=20, time_range="short_term"):
    """
    retrieve users top tracks
    short_term -> last 4 weeks. 
    
    """
    results = sp_user.current_user_top_tracks(limit=limit, time_range=time_range)
    tracks = results['items']

    track_data = []
    for track in tracks:
        track_data.append({
            'id': track['id'],
            'name': track['name'],
            'artists': ", ".join([artist['name'] for artist in track['artists']]),
            'popularity': track['popularity']
        })

    return track_data


def get_audio_features(track_ids):
    """
    get audio features for a list of track IDS
    
    """
    # filter out None, or empty track IDs. 
    valid_track_ids = [tid for tid in track_ids if tid and isinstance(tid, str)]
    # debugging purposes
    print(f"Fetching audio features for {len(valid_track_ids)} tracks...")

    try:
        features = sp_public.audio_features(valid_track_ids)

        # filter non responses
        features = [f for f in features if f] # filtering None responses. 
        print(f"Successfully retrieved audio features for {len(features)} tracks")

        return features
    except Exception as e:
        print(f"Error fetching audio features: {e}")
        raise

    
if __name__ == "__main__":

    # getting top tracks
    top_tracks = get_top_tracks(limit=20, time_range="short_term")
    print("Top 20 Most Listened Songs")
    for idx, track in enumerate(top_tracks, start=1):
        print(f"{idx}. {track['name']} by {track['artists']} (Popularity: {track['popularity']})")

    # getting track IDs and audio features
    track_ids = [track['id'] for track in top_tracks]
    print(f"\nTrack IDs: {track_ids[:3]}...") # printing the first 3 IDs. 

    try:
        audio_features = get_audio_features(track_ids)

        if audio_features:
            print(f"Example features: {list(audio_features[0].keys())}")
            print(f"\nSuccessfully retrieved audio features for {len(audio_features)} tracks")
        else:
            print("\n no features were retreived")
            
    except Exception as e:
        print(f"Failed to get audio features {e}")



    







