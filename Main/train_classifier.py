import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

# Load data from pickle file
with open('./data.pickle', 'rb') as f:
    data_dict = pickle.load(f)

# Extract data and labels
data = data_dict['data']
labels = np.asarray(data_dict['labels'])

# Find the maximum length of the sequences
max_length = max(len(seq) for seq in data)

# Pad sequences to ensure consistent shape
padded_data = np.zeros((len(data), max_length))
for i, seq in enumerate(data):
    padded_data[i, :len(seq)] = seq

# Split data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(padded_data, labels, test_size=0.2, shuffle=True, stratify=labels)

# Initialize and train the RandomForestClassifier
model = RandomForestClassifier()
model.fit(x_train, y_train)

# Make predictions on the test set
y_predict = model.predict(x_test)

# Calculate the accuracy score
score = accuracy_score(y_predict, y_test)
print(f'{score * 100:.2f}% of samples were classified correctly!')

# Save the trained model to a pickle file
with open('model.p', 'wb') as f:
    pickle.dump({'model': model}, f)
