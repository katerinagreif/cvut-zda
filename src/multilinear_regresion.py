import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

# 1. Vytvoření umělého datasetu
data = {
    'reklama': [10, 15, 20, 25, 30, 35, 40, 45, 50, 55],
    'cena':    [90, 85, 80, 78, 75, 74, 72, 70, 69, 68],
    'prodej':  [30, 35, 40, 45, 53, 58, 62, 65, 70, 75]
}

df = pd.DataFrame(data)

# 2. Definice závislé a nezávislých proměnných
X = df[['reklama', 'cena']]
X = sm.add_constant(X)  # přidání interceptu
Y = df['prodej']

# 3. Odhad modelu
model = sm.OLS(Y, X).fit()

# 4. Výpis výsledků
print(model.summary())

# 5. Vizualizace (pro 2D pouze základní vztah mezi prodejem a reklamou)
plt.scatter(df['reklama'], df['prodej'], label='Data')
plt.plot(df['reklama'], model.predict(X), color='red', label='Regresní přímka')
plt.xlabel('Reklamní rozpočet')
plt.ylabel('Prodej')
plt.title('Vícenásobná lineární regrese')
plt.legend()
plt.grid(True)
plt.show()
