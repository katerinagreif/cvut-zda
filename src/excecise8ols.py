import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import scipy
import scipy.stats as stats
from statsmodels.stats.diagnostic import linear_reset

# change rendering
matplotlib.use('TkAgg')

# let's get some data

data = {
    'reklama': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    'prodej':  [25, 30, 45, 50, 55, 60, 65, 75, 80, 90]
}
df = pd.DataFrame(data)
print(df)
# create regression

X = df['reklama']
Y = df['prodej']

X = sm.add_constant(X)  # adds a constant
model = sm.OLS(Y, X).fit()

# get results
print(model.summary())

# get graph
plt.scatter(df['reklama'], df['prodej'], label='Data')
plt.plot(df['reklama'], model.predict(X), color='red', label='Regresní přímka')
plt.xlabel('Reklamní rozpočet')
plt.ylabel('Prodej')
plt.title('OLS regrese: reklama vs. prodej')
plt.legend()
plt.show()
plt.savefig("olsLecture8.png")

# Rezidua
residuals = model.resid

# Histogram + hustota
sns.histplot(residuals, kde=True)
plt.title("Histogram reziduí")
plt.xlabel("Rezidua")
plt.show()

# Q-Q plot
sm.qqplot(residuals, line='s')
plt.title("Q-Q plot reziduí")
plt.show()

# Rezidua vs. predikce
fitted_vals = model.fittedvalues
plt.scatter(fitted_vals, residuals)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel("Predikované hodnoty")
plt.ylabel("Rezidua")
plt.title("Rezidua vs. predikce")
plt.grid(True)
plt.show()


# hledani t statistiky

print(scipy.stats.t.sf(23.048, 8))

# Rezidua vs predikované hodnoty
plt.scatter(model.fittedvalues, model.resid)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Predikované hodnoty')
plt.ylabel('Rezidua')
plt.title('Rezidua vs. predikce')
plt.grid(True)
plt.show()

# rezidua vs vysvetlující proměnná
plt.scatter(df['reklama'], model.resid)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Reklamní rozpočet')
plt.ylabel('Rezidua')
plt.title('Rezidua vs. proměnná reklama')
plt.grid(True)
plt.show()

# Ramsey reset
reset_test = linear_reset(model, power=2, use_f=True)
print(reset_test)

# Homoscedasticita

plt.scatter(model.fittedvalues, model.resid)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Predikované hodnoty')
plt.ylabel('Rezidua')
plt.title('Rezidua vs. predikce')
plt.grid(True)
plt.show()