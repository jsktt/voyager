"""
Author: Junsung Kim
Simualte how spotify might curate a playlist for a user by finding songs

Through song parameters: tempo, energy, bpm, etc. Each paramater will be a different 
dimensions in the vector space. i.e. 5 parameters -> 5D vector space


"""

import numpy as np
from voyager import Index, Space

# i.e each song is represented as a vector. 
songs = {
    0: [0.8, 0.7, 120, 0.6, 0.1],
    1: [0.6, 0.8, 125, 0.7, 0.2],
    2: [0.2, 0.3, 90, 0.2, 0.8],
    3: [0.9, 0.5, 85, 0.65, 0.15],
    4: [0.3, 0.6, 118, 0.1, 0.30],
    5: [0.2, 0.2, 88, 0.15, 0.9],

}

# building the index
index = Index(Space.Euclidean, num_dimensions=5)

# adding the songs
for song_id, features in songs.items():
    index.add_item(np.array(features, dtype=np.float32), id=song_id)

liked_vectors = [songs[0], songs[3]]
taste_vectors = np.mean(liked_vectors, axis=0)

# Finding 3 songs most similar to users taste
neighbors, distances = index.query(np.array(taste_vectors, dtype=np.float32), k=3)

print("Recommened song IDs", neighbors)
print("Similiarity:", distances)