import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

movies_for_model = pd.read_csv("final_correct_encoded_dataset_after_cleaning_with_categorizations.csv")

movies_for_model = movies_for_model.drop(columns=['tconst', 'directors', 'writers','directorNames', 'writerNames', 'genres','Outlier','decade','runtime_category'])

'''
Die Min-Max-Skalierung wird verwendet, um die Werte von in einen Bereich von 0 bis 1 zu transformieren.
Dies verhindert Verzerrungen durch sehr große Zahlen und erleichtert die Verarbeitung durch das Modell.
'''
scaler = MinMaxScaler()
movies_for_model['scaled_genre_vote_popularity'] = scaler.fit_transform(movies_for_model[['movies_with_this_genre_voted']])

movies_for_model['scaled_director_popularity_by_votes'] = scaler.fit_transform(movies_for_model[['director_popularity_by_votes']])

# Output der Skalierung
print(movies_for_model[['director_popularity_by_votes', 'scaled_director_popularity_by_votes']].head())

movies_for_model['scaled_numVotes'] = scaler.fit_transform(movies_for_model[['numVotes']])

'''
Der Gedanke dahinter ist: Filme mit einer laengeren Dauer und gleichzeitig einer hohen Anzahl an
Bewertungen weisen moeglicherweise andere Muster im Rating auf.
'''
movies_for_model['runtime_and_votes'] = movies_for_model['runtimeMinutes'] * movies_for_model['scaled_numVotes']
movies_for_model['scaled_runtime_and_votes'] = scaler.fit_transform(movies_for_model[['runtime_and_votes']])

'''
XGBoost Regressor wird verwendet, um die Vorhersage der durchschnittlichen Bewertungen zu optimieren (andere Modelle geben schlechtere werte raus)
Verschiedene Hyperparameter wie max_depth und n_estimators steuern die Komplexität und Anzahl der Bäume im Modell
'''

# Feature-Auswahl (X) und Zielvariable (y)
X = movies_for_model.drop(columns=['averageRating', 'rating_category', 'director_popularity','primaryTitle'])  # alle Features ausser Zielvariable + welche, dei davon abgeleitet sind/nicht nummerisch sind
y = movies_for_model['averageRating']

# Train-Test Split (80% Training, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#  XGBoost Regressor für bessere Leistung
xg_reg = xgb.XGBRegressor(objective='reg:squarederror',
                          colsample_bytree=0.3,
                          learning_rate=0.1,
                          max_depth=5,
                          alpha=10,
                          n_estimators=100)

# geben dem modell zeugs zum training
xg_reg.fit(X_train, y_train)

# Vorhersagen
y_pred = xg_reg.predict(X_test)

# Berechne den Root Mean Squared Error (RMSE)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("RMSE:", rmse) #je näher an 0 desto besser

# R²-Score
r2_score = xg_reg.score(X_test, y_test)
print("R²-Score auf Testdaten:", r2_score)

# Feature-Bedeutung
importances = xg_reg.feature_importances_
feature_names = X.columns
sorted_indices = np.argsort(importances)[::-1]


# Drucke nur die ersten 10 Beispiele, damit man Leistung vergeleichen kann
print("Ersten 10 Beispiele von Y test und den Vorhersagen:")
for actual, predicted in zip(y_test.values[:10], y_pred[:10]):
    print(f"Tatsächlicher Wert: {actual:.2f}, Vorhergesagt: {predicted:.2f}")



print("Feature-Bedeutung:")
for idx in sorted_indices:
    print(f"{feature_names[idx]}: {importances[idx]:.4f}")

plt.figure(figsize=(20, 15))
plt.barh(feature_names[sorted_indices], importances[sorted_indices], color="skyblue")
plt.xlabel("Wichtigkeit")
plt.title("Feature-Bedeutung (Feature Importance)")
plt.gca().invert_yaxis()  # Wichtigste Features oben
plt.show()
plt.close()

# Scatter Plot für Tatsächliche Werte vs. Vorhergesagte Werte
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], '--k', color='red', label="Ideal")
plt.title("Tatsächliche Werte vs. Vorhergesagte Werte")
plt.xlabel("Tatsächliche Werte")
plt.ylabel("Vorhergesagte Werte")
plt.legend()
plt.show()
plt.close()





'''
Das Skalieren und entfernen der Klassifikationen 'decade','runtime_category' haben den Wert verbessert 
'''