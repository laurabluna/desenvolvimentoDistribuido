from sklearn.tree import DecisionTreeClassifier
import joblib

# Base de sintomas fictícia
# Ordem: [colica, fadiga, nausea, sangramento, dor_costas, vomito, dor_barriga, dor_cabeca]
X = [
    [1, 0, 0, 0, 0, 0, 0, 0],  # TPM leve
    [1, 1, 1, 1, 1, 0, 0, 0],  # TPM forte
    [1, 1, 1, 1, 1, 1, 1, 1],  # Endometriose grave
    [0, 0, 0, 0, 0, 0, 0, 0],  # Sem sintomas
    [0, 1, 1, 0, 0, 1, 1, 1],  # Gripe digestiva
]

y = [
    "TPM leve",
    "TPM moderada",
    "Possível endometriose",
    "Sem sintomas",
    "Provável virose"
]


modelo = DecisionTreeClassifier()
modelo.fit(X, y)

joblib.dump(modelo, "modelo.pkl")
print("Modelo treinado e salvo com sucesso!")
