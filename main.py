"""
Using Voyager vector similarity library from spotify
the lib returns squared Euclidean distances, instead of the std. 
query() -> method allows finding the k nearest int key to a provided List[float]        

"""

import numpy as np
from voyager import Index, Space

class VectorIndex:
    
    # wrapper functions
    def __init__(self, num_dimensions, space=Space.Euclidean):
        self.index = Index(space, num_dimensions=num_dimensions)
        self.num_dimensions = num_dimensions

    def add_vector(self, vector, id=None):
        vector = np.array(vector, dtype=np.float32)
        if vector.shape[0] != self.num_dimensions:
            raise ValueError(f"Vector must have {self.num_dimensions} dimensions.")
        return self.index.add_item(vector, id=id)
    
    def add_vectors(self, vectors, ids=None):
        vectors = np.array(vectors, dtype=np.float32)
        if vectors.shape[1] != self.num_dimensions:
            raise ValueError(f"Each vector must have {self.num_dimensions} dimensions.")
        return self.index.add_items(vectors, ids=ids)
    
    def query(self, vector, k=1):
        vector = np.array(vector, dtype=np.float32)
        neighbors, distances = self.index.query(vector, k=k)
        return neighbors, distances
    
    def __contains__(self, id):
        return id in self.index
    
    def __len__(self):
        return len(self.index)
    
if __name__ == "__main__":
    vi = VectorIndex(num_dimensions=5)
    id_a = vi.add_vector([1, 2, 3, 4, 5])
    id_b = vi.add_vector([6, 7, 8, 9, 10])

    neighbors, distances = vi.query([1, 2, 3, 4, 5], k=2)
    print("Neighbors IDs:", neighbors)
    print("Squared Distance:", distances)