#
# IDS simples para detecção de ataques DDoS usando classificador Random Forest
# Dataset: CICIDS2017 (Friday-WorkingHours-Afternoon-DDos)
# Fonte: https://www.unb.ca/cic/datasets/ids-2017.html
# 
# Autor: Jadson Santos - jadson.santos@ufrn.br
#
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# 1 - Carrega uma amostra do dataset CICIDS2017
# Use um dos arquivos CSV disponíveis no site da UNB
arquivo = "Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"
dados = pd.read_csv(arquivo)
dados.columns = dados.columns.str.strip()  # remove espaços extras dos nomes das colunas

print(dados.columns.tolist())

print("Colunas disponíveis:", len(dados.columns))
print("Exemplo de dados:\n", dados.head())

# 2- Pré-processamento básico
# Remove colunas irrelevantes ou com valores não numéricos
dados = dados.dropna()
dados = dados.replace([np.inf, -np.inf], np.nan).dropna()

# Seleciona algumas features numéricas comuns
features = ['Flow Duration', 'Total Fwd Packets', 'Total Backward Packets',
             'Total Length of Fwd Packets', 'Total Length of Bwd Packets',
             'Flow IAT Mean', 'Fwd IAT Total', 'Bwd IAT Total',
             'Fwd Packets/s', 'Bwd Packets/s']

X = dados[features]

# 3 - Rótulos: converte ataques específicos em binário (0=Normal, 1=Ataque)
y = dados['Label'].apply(lambda x: 0 if x == 'BENIGN' else 1)

# 4 - Normaliza as features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 5 - Divide treino/teste
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42, stratify=y)

# 6 - Treina modelo de ML usando classificação Random Forest
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# 7 - Avaliação
y_pred = modelo.predict(X_test)
print("\n=== Relatório de desempenho ===")
print(classification_report(y_test, y_pred, target_names=["Normal", "Ataque"]))

# 8 - Matriz de confusão
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=["Normal", "Ataque"], yticklabels=["Normal", "Ataque"])
plt.title("Matriz de Confusão - IDS com ML (CICIDS2017)")
plt.xlabel("Previsto")
plt.ylabel("Real")
plt.show()

# 9 - Criar um nova amostra (simulação)
nova = pd.DataFrame([{
    'Flow Duration': 10000,
    'Total Fwd Packets': 400,
    'Total Backward Packets': 20,
    'Total Length of Fwd Packets': 120000,
    'Total Length of Bwd Packets': 3000,
    'Flow IAT Mean': 5,
    'Fwd IAT Total': 1000,
    'Bwd IAT Total': 200,
    'Fwd Packets/s': 400,
    'Bwd Packets/s': 10
}])

nova_scaled = scaler.transform(nova)
resultado = modelo.predict(nova_scaled)[0]

print("\nNova conexão classificada como:", "ATAQUE 🚨" if resultado == 1 else "NORMAL ✅")
