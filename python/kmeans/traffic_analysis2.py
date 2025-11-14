
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN
import matplotlib.pyplot as plt

# =============================
# 1. Importa CSV (Wireshark ou tshark)
# =============================
dados = pd.read_csv('trafego.csv')


# Seleção de colunas (exemplo comum em Wireshark Statistics → Conversations)
features = [
    "Packets A → B",
    "Packets B → A",
    "Bytes A → B",
    "Bytes B → A",
    "Duration"
]

dados = dados[features]

# =============================
# 2. Normalização
# =============================
scaler = StandardScaler()
X = scaler.fit_transform(dados)


# =============================
# 4. DBSCAN (detecção de outliers)
# =============================
dbscan = DBSCAN(eps=0.6, min_samples=5)
dados["dbscan_cluster"] = dbscan.fit_predict(X)


# DBSCAN usa cluster -1 para outliers
dados["is_outlier"] = dados["dbscan_cluster"] == -1

# =============================
# 5. Mostra os 10 primeiros
# =============================
print("\n=== RESULTADOS ===")
print(dados)

print("\nTotal de outliers detectados:", dados["is_outlier"].sum())

# =============================
# 6. Gráfico simples 2D (K-Means vs DBSCAN)
# =============================
plt.figure(figsize=(8, 6))
plt.scatter(X[:,0], X[:,1], c=dados["dbscan_cluster"])
plt.title("DBSCAN - Detecção de Outliers")
plt.xlabel(features[0])
plt.ylabel(features[1])
plt.show()