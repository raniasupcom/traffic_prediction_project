import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Generate synthetic data
X = np.random.randint(0, 200, 1000).reshape(-1, 1)
y = np.where(X < 50, 0, np.where(X < 150, 1, 2)).flatten()

# Simple model
model = Sequential([
    Dense(10, activation='relu', input_shape=(1,)),
    Dense(3, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(X, y, epochs=10)
model.save('traffic_model.h5')
