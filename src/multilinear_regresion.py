import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np

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


### Kvadratický model
df['reklama_sq'] = df['reklama']**2
X_quad = sm.add_constant(df[['reklama', 'reklama_sq', 'cena']])
model_quad = sm.OLS(df['prodej'], X_quad).fit()
print("📘 Kvadratický model:")
print(model_quad.summary())

### Log-lineární model
df['log_prodej'] = np.log(df['prodej'])
X_loglin = sm.add_constant(df[['reklama', 'cena']])
model_loglin = sm.OLS(df['log_prodej'], X_loglin).fit()
print("\n📘 Log-lineární model:")
print(model_loglin.summary())

###  Log-log model
df['log_reklama'] = np.log(df['reklama'])
df['log_cena'] = np.log(df['cena'])
X_loglog = sm.add_constant(df[['log_reklama', 'log_cena']])
model_loglog = sm.OLS(df['log_prodej'], X_loglog).fit()
print("\n📘 Log-log model:")
print(model_loglog.summary())

# Predikce
df['quad_pred'] = model_quad.predict(X_quad)
df['loglin_pred'] = np.exp(model_loglin.predict(X_loglin))  # převod zpět z log
df['loglog_pred'] = np.exp(model_loglog.predict(X_loglog))  # převod zpět z log


# Vizualizace
fig, axs = plt.subplots(1, 3, figsize=(18, 5))

# Kvadratický model
axs[0].scatter(df['reklama'], df['prodej'], label='Data')
axs[0].plot(df['reklama'], df['quad_pred'], color='red', label='Kvadratický fit')
axs[0].set_title("Kvadratický model")
axs[0].set_xlabel("Reklama")
axs[0].set_ylabel("Prodej")
axs[0].legend()
axs[0].grid(True)

# Log-lineární model
axs[1].scatter(df['reklama'], df['prodej'], label='Data')
axs[1].plot(df['reklama'], df['loglin_pred'], color='green', label='Log-lineární fit')
axs[1].set_title("Log-lineární model")
axs[1].set_xlabel("Reklama")
axs[1].set_ylabel("Prodej")
axs[1].legend()
axs[1].grid(True)

# Log-log model
axs[2].scatter(df['reklama'], df['prodej'], label='Data')
axs[2].plot(df['reklama'], df['loglog_pred'], color='purple', label='Log-log fit')
axs[2].set_title("Log-log model")
axs[2].set_xlabel("Reklama")
axs[2].set_ylabel("Prodej")
axs[2].legend()
axs[2].grid(True)

plt.tight_layout()
plt.show()
