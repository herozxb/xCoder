import umap
import matplotlib.pyplot as plt
import numpy as np

# Generate 100D data for training
num_samples = 1000
X_train_100d = np.random.uniform(-1, 1, (num_samples, 100))  # Random 100D data

# Instantiate and fit UMAP to reduce from 100D to 2D
umap_model = umap.UMAP(n_components=2, random_state=42)
X_train_2d_umap = umap_model.fit_transform(X_train_100d)

# Plot the 2D UMAP projection
plt.figure(figsize=(6, 6))
plt.scatter(X_train_2d_umap[:, 0], X_train_2d_umap[:, 1], c='blue', alpha=0.5)
plt.xlabel('UMAP 1')
plt.ylabel('UMAP 2')
plt.title('UMAP Projection of 100D Data')
plt.grid(True)
plt.show()

