import numpy as np
from voyager import Index, Space

# Create an empty Index object that can store vectors
index = Index(Space.Euclidean, num_dimensions=5)
id_a = index.add_item([1, 2, 3, 4, 5])
id_b = index.add_item([6, 7, 8, 9, 10])

print(id_a) # => 0
print(id_b) # => 1
