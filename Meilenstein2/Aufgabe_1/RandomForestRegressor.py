import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler

rfg = RandomForestRegressor(n_estimators=100, random_state=42)

#lr = LinearRegression() # mit linearer Regression wert von noch schlechter

movies_for_model = pd.read_csv("final_correct_encoded_dataset_after_cleaning_with_categorizations.csv")

movies_for_model = movies_for_model.drop(columns=['tconst', 'directors', 'writers','directorNames', 'writerNames', 'genres','Outlier','decade','runtime_category'])


'''
                    Filme mit vielen Bewertungen haben oft viel größere Zahlen als Filme mit wenigen Bewertungen.
- Der Logarithmus schrumpft die großen Zahlen, damit sie nicht  extrem sind.
'''
movies_for_model['log_numVotes'] = np.log1p(movies_for_model['numVotes'])

scaler = MinMaxScaler()

# Skalierung der Werte auf den Bereich [0, 1]
movies_for_model['scaled_genre_vote_popularity'] = scaler.fit_transform(movies_for_model[['movies_with_this_genre_voted']])

# Überprüfen der skalierten Werte
print(movies_for_model[['movies_with_this_genre_voted', 'scaled_genre_vote_popularity']].head())
movies_for_model['runtime_and_votes'] = movies_for_model['runtimeMinutes'] * movies_for_model['log_numVotes']


X = movies_for_model.drop(columns=['averageRating','rating_category', 'director_popularity','primaryTitle'])
y = movies_for_model['averageRating']

# Aufteilen der Daten in Training (80%) und Test (20%)
X_train,X_test,y_train,y_test =train_test_split(X,y,test_size=0.2,random_state=42) # damit immer selbe stichprobe
print("Größe der 80%",len(X_train))
print("Größe der 20%",len(X_test))

rfg.fit(X_train, y_train)
#lr.fit(X_train, y_train)

rfg.predict(X_test)
#lr.predict(X_test)

importances = rfg.feature_importances_
feature_names = X.columns
sorted_indices = np.argsort(importances)[::-1]

print("Feature-Bedeutung:")
for idx in sorted_indices:
    print(f"{feature_names[idx]}: {importances[idx]:.4f}")

print("So sieht unser Y test aus",y_test) #die werte sollen ähnlihc wie predict sein

print("Vergleicht die vorhergesagten Werte mit y ", rfg.score(X_test, y_test))
#print("Vergleicht die vorhergesagten Werte mit y (lineare Regression)", lr.score(X_test, y_test))


y_pred = rfg.predict(X_test)

def plot_predictions(y_test, y_pred):
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], '--k', color='red')
    plt.title("Tatsächliche Werte vs. Vorhergesagte Werte")
    plt.xlabel("Tatsächliche Werte")
    plt.ylabel("Vorhergesagte Werte")
    #plt.show()


# Bar-Chart für Feature-Wichtigkeit
plt.figure(figsize=(10, 6))
plt.barh(feature_names[sorted_indices], importances[sorted_indices], color="skyblue")
plt.xlabel("Wichtigkeit")
plt.title("Feature-Bedeutung (Feature Importance)")
plt.gca().invert_yaxis()  # Wichtigste Features oben
plt.show()
plt.close()

plot_predictions(y_test, y_pred)

'''
Diese Klasse dient als erster Versuch der Modellbildung unter Verwendung des RandomForestRegressors und in einkommentierter Version Linear Regression. 
Der RandomForestRegressor wurde mit dem Ziel verwendet, ein grundlegendes Verständnis für das Modell und die Feature-Wichtigkeit zu entwickeln. 
Allerdings stellt dieses Modell nur einen ersten Schritt darund das XGBoost-Modell wird als die endgueltige und optimierte Loesung betrachtet.

Einige wichtige Punkte:
- Dieses Modell dient der Validierung von Vorhersagen und der Berechnung von Feature-Wichtigkeiten, jedoch wird der endgueltige R²-Score durch die Nutzung von XGBoost  verbessert.
  Dieses Modell liefert einen Score von 0.4020365251848522

'''
