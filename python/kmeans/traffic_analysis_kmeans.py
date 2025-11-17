import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# 1 Carrega dados exportados do Wireshark
dados = pd.read_csv('trafego.csv')

# 2 Seleciona as features numéricas mais relevantes
X = dados[['Packets A → B', 'Packets B → A', 'Bytes A → B', 'Bytes B → A', 'Duration']]

# 3 Normaliza os dados
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 4 Aplica K-Means com 3 clusters
kmeans = KMeans(n_clusters=3, random_state=42)
dados['Cluster'] = kmeans.fit_predict(X_scaled)

# 5 Imprime o resultado
print(dados[['Address A', 'Address B', 'Cluster']].head())

# 6 Visualização
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=dados['Cluster'], cmap='viridis')
plt.xlabel('Packets A → B')
plt.ylabel('Packets B → A')
plt.title('Agrupamento de tráfego com K-Means')
plt.show()
