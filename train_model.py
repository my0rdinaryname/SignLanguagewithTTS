import pickle
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

data_org = pickle.load(open('data.pickle', 'rb'))
raw = data_org['data']
labels = np.asarray(data_org['labels'])

target_len = 42
processed = []
proc_labels = []
problem_items = []

for i, item in enumerate(raw):
    try:
        arr = np.asarray(item).ravel()  # flatten any shape into 1D
    except Exception as e:
        problem_items.append((i, "convert_error", str(e)))
        continue

    L = arr.shape[0]
    if L == target_len:
        vec = arr
    elif L == 2 * target_len:
        try:
            vec = arr.reshape(2, target_len).mean(axis=0)
        except Exception as e:
            problem_items.append((i, "reshape_error", str(e)))
            continue
    elif L > target_len:
        vec = arr[:target_len]
        problem_items.append((i, "truncated_from", L))
    elif L < target_len:
        pad = np.zeros(target_len - L, dtype=arr.dtype)
        vec = np.concatenate([arr, pad])
        problem_items.append((i, "padded_from", L))
    else:
        vec = arr  # last resort

    # ensure numeric type and length
    vec = np.asarray(vec, dtype=np.float32).ravel()
    if vec.shape[0] != target_len:
        problem_items.append((i, "len_mismatch_after_proc", vec.shape[0]))
        continue

    processed.append(vec)
    proc_labels.append(labels[i])

print("Processed:", len(processed), "Kept labels:", len(proc_labels))
print("Problem items (examples):", problem_items[:10])

X = np.asarray(processed)
y = np.asarray(proc_labels)

print("X shape:", X.shape, "y shape:", y.shape)

# Now train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
score = accuracy_score(y_test, y_pred)
print(f'Accuracy: {score * 100:.2f}%')

f = open('rf_model.pickle', 'wb')
pickle.dump(model, f)
f.close()