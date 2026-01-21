from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np

# Generate 100D data for training
num_samples = 1000
X_train_100d = np.random.uniform(-1, 1, (num_samples, 100))  # Random 100D data

# Instantiate and fit PCA to reduce from 100D to 2D
pca = PCA(n_components=2)
X_train_2d = pca.fit_transform(X_train_100d)

# Plot the 2D projection of the 100D data
plt.figure(figsize=(6, 6))
plt.scatter(X_train_2d[:, 0], X_train_2d[:, 1], c='blue', alpha=0.5)
plt.xlabel('PCA 1')
plt.ylabel('PCA 2')
plt.title('PCA Projection of 100D Data')
plt.grid(True)
plt.show()

