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
    vi = VectorIndex(num_dimensions=3)
    id_a = vi.add_vector([1, 2, 3]) # auto ID 0
    id_b = vi.add_vector([4, 5, 6]) # auto ID 1
    id_c = vi.add_vector([7, 8, 9], id=42) # custom ID 42

    neighbors, distances = vi.query([1, 2, 3], k=3)

    # batch add vectors
    batch_ids = vi.add_vectors([[10, 11, 12], [13, 14, 15]], ids=[100, 101])
    
    # multiple vectors by their ID
    vecs = vi.index.get_vectors([0, 1, 42])
    print("Vectors with IDs 0, 1, 42:\n", vecs)

    # checking if the ID exsists
    print("Does ID 42 exist?", 42 in vi)
    print("Does ID 999 exist?", 999 in vi)
    
    # get the distance between two vectors
    dist = vi.index.get_distance([1, 2, 3], [4, 5, 6])
    print("dist between the two vectors", dist)

    # mark id as deleted
    vi.index.mark_deleted(42)
    print("ID 42 Deleted?", 42 in vi)

    # serialize index to bytes
    index_bytes = bytes(vi.index)
    print("Serialized index byte:", len(index_bytes))







