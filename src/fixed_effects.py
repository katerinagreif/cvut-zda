import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from linearmodels.panel import PanelOLS

# Simulovaná data
data = {
    "firma": ["A", "A", "B", "B", "C", "C"],
    "rok": [2020, 2021, 2020, 2021, 2020, 2021],
    "trzby": [100, 120, 90, 95, 130, 135],
    "marketing": [10, 15, 8, 10, 12, 14]
}

df = pd.DataFrame(data)

# Vykreslení jednoho grafu pro každou firmu
firms = df["firma"].unique()

for firm in firms:
    subset = df[df["firma"] == firm]
    plt.figure()
    plt.plot(subset["marketing"], subset["trzby"], marker='o', color="orange")

    # Označení jednotlivých bodů rokem
    for i in range(len(subset)):
        plt.text(subset["marketing"].iloc[i], subset["trzby"].iloc[i], f"{subset['rok'].iloc[i]}")

    plt.title(f"Firma {firm}: Tržby vs. Marketing")
    plt.xlabel("Marketingové výdaje")
    plt.ylabel("Tržby")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

df = pd.DataFrame(data)


# ================================================
# POOLING MODEL (klasický OLS přes všechna data)
# ================================================
X_pooled = sm.add_constant(df["marketing"])
model_pooled = sm.OLS(df["trzby"], X_pooled).fit()
df["pooled_pred"] = model_pooled.predict(X_pooled)

print("=== Pooled OLS ===")
print(model_pooled.summary())

# ================================================
# FIXED EFFECTS MODEL (PanelOLS + EntityEffects)
# ================================================
# Model s fixními efekty firem s + EntityEffects, které odhaduje každé firmě vlastní intercepty
# Předpokládá shodný koeficient
# Pro modelování pomocí PanelOLS potřebujeme vícerozměrný index
df_panel = df.set_index(["firma", "rok"])
model_fe = PanelOLS.from_formula("trzby ~ 1 + marketing + EntityEffects", data=df_panel)
results_fe = model_fe.fit()
df_panel["fe_pred"] = results_fe.predict().fitted_values
df["fe_pred"] = df_panel["fe_pred"].values

print("\n=== Fixed Effects ===")
print(results_fe.summary)


# ================================================
# INDIVIDUÁLNÍ OLS REGRESE (firma po firmě)
# ================================================
print("\n=== Individuální OLS modely ===")
df["indiv_pred"] = np.nan
for firm in df["firma"].unique():
    subset = df[df["firma"] == firm]
    X = sm.add_constant(subset["marketing"])
    y = subset["trzby"]
    model_indiv = sm.OLS(y, X).fit()
    pred = model_indiv.predict(X)
    df.loc[subset.index, "indiv_pred"] = pred

    print(f"\n--- Firma {firm} ---")
    print(model_indiv.summary())



# =========================
# 5. VIZUALIZACE
# =========================

colors = {"A": "tab:blue", "B": "tab:green", "C": "tab:orange"}

# A. POOLING model
plt.figure()
for firm in df["firma"].unique():
    subset = df[df["firma"] == firm]
    plt.scatter(subset["marketing"], subset["trzby"], label=f"Firma {firm}", color=colors[firm])
plt.plot(df["marketing"], df["pooled_pred"], color="black", label="Pooled OLS")
plt.title("Pooled OLS: Společná přímka pro všechny firmy")
plt.xlabel("Marketing")
plt.ylabel("Tržby")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# B. FIXED EFFECTS predikce
plt.figure()
for firm in df["firma"].unique():
    subset = df[df["firma"] == firm]
    plt.plot(subset["marketing"], subset["fe_pred"], linestyle="--", color=colors[firm], label=f"{firm} – FE predikce")
    plt.scatter(subset["marketing"], subset["trzby"], color=colors[firm])
plt.title("Fixed Effects: Vlastní intercepty, společný sklon")
plt.xlabel("Marketing")
plt.ylabel("Tržby")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# C. Individuální modely
plt.figure()
for firm in df["firma"].unique():
    subset = df[df["firma"] == firm]
    plt.plot(subset["marketing"], subset["indiv_pred"], linestyle="-", label=f"{firm} – Individuální OLS", color=colors[firm])
    plt.scatter(subset["marketing"], subset["trzby"], color=colors[firm])
plt.title("Individuální OLS: Každá firma má vlastní model")
plt.xlabel("Marketing")
plt.ylabel("Tržby")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# D. Srovnání predikcí v čase
for firm in df["firma"].unique():
    subset = df[df["firma"] == firm]
    plt.figure()
    plt.plot(subset["rok"], subset["trzby"], marker='o', label="Skutečné tržby", color="black")
    plt.plot(subset["rok"], subset["pooled_pred"], marker='x', linestyle='--', label="Pooled OLS", color="gray")
    plt.plot(subset["rok"], subset["fe_pred"], marker='x', linestyle='--', label="Fixed Effects", color="blue")
    plt.plot(subset["rok"], subset["indiv_pred"], marker='x', linestyle='--', label="Individuální OLS", color="green")
    plt.title(f"{firm}: Skutečné vs. predikované tržby (v čase)")
    plt.xlabel("Rok")
    plt.ylabel("Tržby")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    


## REalný příklad na českých datech
# https://csu.gov.cz/produkty/zam_cr
# Načtení dat
df = pd.read_csv("../data/panel_data_unemployment.csv")

# Nastavení panelového indexu
df = df.set_index(["region", "year"])

# Převod typu
df["unemployment_rate"] = pd.to_numeric(df["unemployment_rate"], errors="coerce")

# Umělá nezávislá proměnná (např. ekonomický index)
np.random.seed(42)
df["eco_index"] = np.random.normal(loc=100, scale=10, size=len(df))

# Estimace Fixed Effects modelu (včetně konstanty a fixních efektů)
model = PanelOLS.from_formula("unemployment_rate ~ 1 + eco_index + EntityEffects", data=df)
results = model.fit()

# Výstup
print(results.summary)
