# Import knihoven
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score

# 1. Generování syntetických dat
X, y_true = make_blobs(n_samples=300, centers=3, cluster_std=0.60, random_state=0)

# Vizualizace dat před segmentací
plt.figure(figsize=(6, 4))
plt.scatter(X[:, 0], X[:, 1], s=50)
plt.title("Syntetická data - před segmentací")
plt.show()

# 2. Fitování k-means modelu
kmeans3 = KMeans(n_clusters=3, n_init=10, random_state=0)
kmeans3.fit(X)
score3 = silhouette_score(X, kmeans3.labels_)
y_kmeans3 = kmeans3.predict(X)
print(f"k=3: Inertia={kmeans3.inertia_:.2f}, Silhouette Score={score3:.2f}")

# Pro k=5
kmeans5 = KMeans(n_clusters=5, random_state=0).fit(X)
score5 = silhouette_score(X, kmeans5.labels_)
y_kmeans5 = kmeans5.predict(X)
print(f"k=5: Inertia={kmeans5.inertia_:.2f}, Silhouette Score={score5:.2f}")

# 3. Vizualizace segmentovaných dat
def vizualisation (X, y_kmeans,kmeans):
    """ Vizualizace k-means výsledků."""
    plt.figure(figsize=(6, 4))
    plt.scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, cmap='viridis')

    # Zobrazení centroidů
    centers = kmeans3.cluster_centers_
    plt.scatter(centers[:, 0], centers[:, 1], c='red', s=200, alpha=0.75, marker='X', label='Centroidy')
    plt.title("Segmentace pomocí k-means")
    plt.legend()
    plt.show()

    # 4. Výpis klíčových atributů modelu
    print(f"Centroidy:\n{centers}")
    print(f"Inertia (suma čtverců vzdáleností): {kmeans.inertia_}")
    print(f"První 10 přiřazení clusterů:\n{y_kmeans3[:10]}")


vizualisation(X, y_kmeans3,kmeans3)
vizualisation(X, y_kmeans5,kmeans5)


### Elbow method
# Příprava proměnných
inertia_values = []
k_values = range(1, 11)

# Výpočet inercie pro různá k
for k in k_values:
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=0)
    kmeans.fit(X)
    inertia_values.append(kmeans.inertia_)

# Vykreslení Elbow grafu
plt.figure(figsize=(8, 5))
plt.plot(k_values, inertia_values, 'bo-')
plt.xlabel('Počet clusterů (k)')
plt.ylabel('Inertia')
plt.title('Elbow Method: Volba optimálního počtu clusterů')
plt.grid(True)
plt.show()

## Silhoulette score
# Příprava proměnných
silhouette_scores = []
k_values = range(2, 11)  # Začínáme od k=2 (pro k=1 nemá smysl silhouette score)

# Výpočet silhouette score pro různá k
for k in k_values:
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=0)
    labels = kmeans.fit_predict(X)
    score = silhouette_score(X, labels)
    silhouette_scores.append(score)

# Vykreslení Silhouette grafu
plt.figure(figsize=(8, 5))
plt.plot(k_values, silhouette_scores, 'bo-')
plt.xlabel('Počet clusterů (k)')
plt.ylabel('Průměrné silhouette score')
plt.title('Silhouette Analysis: Volba optimálního počtu clusterů')
plt.grid(True)
plt.show()