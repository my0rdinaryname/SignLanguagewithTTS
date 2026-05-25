import pickle
import numpy as np

data_org = pickle.load(open('data.pickle', 'rb'))
data_list = data_org['data']

# quick summary
from collections import Counter
shapes = []
for i, item in enumerate(data_list):
    try:
        arr = np.asarray(item)
        shapes.append(arr.shape)
    except Exception as e:
        shapes.append(('error', str(e)))

print("Total items:", len(data_list))
print("Unique shapes and counts:", Counter(shapes))

# print first few shapes and an example problematic index
for i, s in enumerate(shapes[:20]):
    print(i, s)

# show indices where shape != most_common_shape
most_common_shape = Counter(shapes).most_common(1)[0][0]
bad_indices = [i for i,s in enumerate(shapes) if s != most_common_shape]
print("Example bad indices (first 10):", bad_indices[:10])

