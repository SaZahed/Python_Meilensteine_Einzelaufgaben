from collections import Counter

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.preprocessing import LabelEncoder

pd.set_option('display.max_columns', None)  # Keine Begrenzung für Spalten
pd.set_option('display.width', 320)       # Maximale Breite für jede Zeile

movies = pd.read_csv("reduced_and_merged_data_with_names.csv")

print(movies.head())
print("Infos zur unbereinigte CSV mit 100 000 Sätzen \n")
movies.info()
print("Form des DataFrames unbereinigt \n",movies.shape) # (100000, 15)

# Entfernen der meiner nach nicht relevanten Spalten:
movies_cleaned = movies.drop(columns=['endYear','isAdult', 'originalTitle', 'titleType'])
print("Form des DataFrames: Anzahl der Zeilen und Spalten \n",movies_cleaned.shape) #  (100000, 11)

# Prüfe, ob der DataFrame leer ist --> teils zu Debugging Zwecken
if movies_cleaned.empty:
    print("Der DataFrame ist leer!")
else:
    print("Info des DataFrames:")
    movies_cleaned.info()


'''
                                    Methode zur Speicherung von Bildern im Images Ornder
 
- Speichert eine Matplotlib-Abbildung im "images" Ordner des Projekts.

- Diese Funktion speichert die gegebene Matplotlib-Abbildung als Bilddatei im Projektverzeichnis 
  unter dem Ordner 'images'. Der Pfad wird automatisch basierend auf dem Kapitel und den 
  gegebenen Parametern für Dateierweiterung und Auflösung erstellt.

- Args:
  fig_id (str): Der Name der Abbildung, unter dem die Datei gespeichert wird.
  tight_layout (bool, optional): Ob die Abbildung mit `tight_layout` gespeichert werden soll. Standard ist True.
  fig_extension (str, optional): Die Dateierweiterung des gespeicherten Bildes -->  "png"
  resolution (int, optional): Die Auflösung (DPI) des gespeicherten Bildes --> 300

- Hinweise: die Methodenaufrufe zum Speichern der Grafiken sind einkommentiert, da sie schon gepeichert wurden
       
'''
PROJECT_ROOT_DIR = "." # aktueller Arbeitsordner
CHAPTER_ID = "visualisierungen_filmdatenanalyse"
IMAGES_PATH = os.path.join(PROJECT_ROOT_DIR, "images", CHAPTER_ID)
os.makedirs(IMAGES_PATH, exist_ok=True)

def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=300):
    path = os.path.join(IMAGES_PATH, fig_id + "." + fig_extension)
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)


"""
                                                    Datenbereinigung und Nullwertbehandlung 

1. Ersetzen von '\\N' mit NaN:
   - die CSV-Datei hat Nullwerte als den String darstellt, deshalb werden diese durch `np.nan` ersetzt

2. Konvertierung 'startYear' und 'runtimeMinutes' in numerische Werte:
   - Die Spalten enthalten teilweise Nullwerte, jedoch moechte ich sie nicht loeschen, da dies meinen Datensatz sehr verkleinern wuerde.
    Statt sie zu loeschen fuege ich die durchschnittsweerte der Attribute ein. Um diese zu berechnen muessen die Attribute zu nummerischen Zahlen 
    konvertiert werden
3. Ersetzen von Nullwerten in den Spalten 'directors' und 'writers':
   - Die Zellen, die fehlende Werte aufweisen ersetze ich mit dem  Platzhalter `'nm0000000'`, um anzugeben, dass keine Daten vorhanden sind (wie "Unknown").

"""
movies_cleaned.replace(r'\\N', np.nan, regex=True, inplace=True)

movies_cleaned['startYear'] = pd.to_numeric(movies_cleaned['startYear'], errors='coerce')
movies_cleaned['runtimeMinutes'] = pd.to_numeric(movies_cleaned['runtimeMinutes'], errors='coerce')

movies_cleaned['directors'].fillna('nm0000000', inplace=True)
movies_cleaned['writers'].fillna('nm0000000', inplace=True)

# Mittelwert Berechnungen ohne NaN-Werte zu berücksichtigen
mean_runtime = movies_cleaned['runtimeMinutes'].mean()
movies_cleaned['runtimeMinutes'].fillna(mean_runtime, inplace=True)
print("Der Mittelwert für runtimeMin:\n", mean_runtime) #  94.36364953416842

mean_startYear = movies_cleaned['startYear'].mean()
movies_cleaned['startYear'].fillna(mean_startYear, inplace=True)
print("Der Mittelwert für startYear:\n", mean_startYear) #  1995.982888117693

"""
                            Label-Encoding für die Spalten 'directors' und 'writers'.

- in ihrem ursprünglichen Format liegen sie als Strings vor
- Das Label-Encoding weist jedem einzigartigen Wert in den Spalten eine numerische Kennung zu, um die Daten fuer maschinelles Lernen vorzubereiten.
- `fit_transform` passt den LabelEncoder an die einzigartigen Werte in den Spalten an und transformiert diese dann direkt in numerische Werte.
"""

director_encoder = LabelEncoder()
writer_encoder = LabelEncoder()

movies_cleaned['director_encoded'] = director_encoder.fit_transform(movies_cleaned['directors'])
movies_cleaned['writer_encoded'] = writer_encoder.fit_transform(movies_cleaned['writers'])
print("So sieht der Datensatz mit dem label-encoding von den nconst aus:\n",movies_cleaned[['directors', 'director_encoded', 'writers', 'writer_encoded']].head())

'''
                                        Fehlende Werte pro Spalte: 
- nun kommt die Bereinigung des Dataset, indem die fehlenden Werte entfernt werden, die wir nicht mit Mittelwerten fuellen koennen
'''
print("Fehlt irgendein Wert im Datensatz?", movies_cleaned.isna().sum().values.any()) #True
print("Summe der fehlenden Werte:\n",movies_cleaned.isna().sum()) #genres: 3430
per_missing = movies_cleaned.isna().sum() * 100 /len(movies_cleaned)
print("Fehlende Werte in Prozentangabe:\n", per_missing)

plt.figure(figsize=(26, 26))
sns.heatmap(movies_cleaned.isna().astype(int), cmap="viridis", cbar=False)
plt.title("Visualisierung der fehlenden Daten")
plt.xlabel("Spalten")
plt.ylabel("Zeilen")
#save_fig("fehlende_werte_heatmap")
plt.show()
plt.close()

# Noch mal als Sauelendiagramm
missing_data = movies_cleaned.isna().sum()
plt.figure(figsize=(26, 26))
missing_data[missing_data > 0].sort_values(ascending=False).plot(kind='bar', color='skyblue')
plt.title("Fehlende Werte pro Spalte")
plt.xlabel("Spalten")
plt.ylabel("Anzahl fehlender Werte")
#save_fig("fehlende_werte_bar")
plt.show()
plt.close()

# da ich nun nicht mehr Infos über Nullwerte brauche, entferne ich diese, damit die Statistiken nicht manipuliert werden
movies_cleaned_copy = movies_cleaned.copy() #Sicherheitskopie erstellen: 100 000 Einträge ohne jegliche Bereinigung
movies_cleaned = movies_cleaned.dropna()
# Kopie vom Dataset ohne Nullwerte
movies_cleaned_copy_without_null = movies_cleaned.copy()

print("Summe der fehlenden Werte nach entfernen von Nullweten:\n",movies_cleaned.isna().sum()) # keine fehlende Werrte mehr, weil bereinigt
print("Anzahl der Zeilen und Spalten  nach dem entfernne von Nullwerten:\n",movies_cleaned.shape) # (96570, 13)

"""
                                        One-Hot-Encoding für die Genre-Spalte des Film-Datensatzes.

In diesem Schritt wird die 'genres'-Spalte, die eine durch Kommata getrennte Liste von Genres enthält, in binaere Werte (1/0) umgewandelt, um die Genres für maschinelles Lernen verwendbar zu machen und Genres zu filtern. 
Der Vorteil: die Anwesenheit jedes einzelnen Genres für einen Film

1. Relevante Genres:
   - Zuerst wird die Liste von relevanten Genres definiert, die für die Analyse beruecksichtigt werden sollen. Die Genres, die nicht in dieser Liste enthalten sind, werden spater aus dem Datensatz entfernt (filter)

2. Funktion `genre_to_one_hot`:
   - sie nimmt die uebergebene Liste von Genres und prueft fuer jedes relevante Genre, ob es in der Liste der Genres des jeweiligen Films enthalten ist.
   - die Rueckgabe ist eine eine Liste von binären Werten, (1 = True, 0 = False))

3. One-Hot-Encoding anwenden:
   - Fuer jeden Film im Datensatz wird die Funktion `genre_to_one_hot` angewendet, um die Genres in binaere Werte zu kodieren. Das Ergebnis ist ein numpy-Array, das für jedes Genre eine 1 oder 0 enthaelt, je nachdem, ob das Genre im Film vorhanden ist.

4. DataFrame für One-Hot-Encoding erstellen:
   - Das Array wird in einen DataFrame umgewandelt, der als neue Spalten fuer jedes relevante Genre die binaeren Werte enthaelt 

5. Zusammenfuegen des One-Hot-Encodings mit dem Original-DataFrame:
   - Der DataFrame mit den One-Hot-Encoded-Genres wird an den urspruenglichen `movies_cleaned` DataFrame angehaengt, sodass der Datensatz nun sowohl die originalen Genres als auch die One-Hot-kodierten Spalten enthaelt.

6. Entfernung von irrelevanten Genres:
   - Filme, die keine der relevanten Genres haben und die Statistiken verzehren wuerden, werden durch den One-Hot-Encoder automatisch mit Nullen kodiert. Diese Filme werden später, falls notwendig, für die Analyse entfernt

"""

relevante_genres = [
    "Action", "Adventure", "Drama", "Horror", "Fantasy", "Mystery",
    "Animation", "Thriller", "Comedy", "Romance", "Crime", "Musical",
    "Sci-Fi", "Sport", "Family", "Documentary", "Biography", "Western",
    "History", "Film-Noir", "Music", "War"
]
def genre_to_one_hot(genres, relevant_genres):
    genre_list = genres.split(',')  # Trenne die Genres an den Kommata (sehr wichtig)
    genre_flags = [genre in genre_list for genre in relevant_genres]
    return genre_flags

one_hot_encoded = np.array([genre_to_one_hot(genres, relevante_genres) for genres in movies_cleaned["genres"]])

one_hot_df = pd.DataFrame(one_hot_encoded, columns=relevante_genres, index=movies_cleaned.index)

# Konvertiere True/False in 1/0 (sonst wöre es boolean)
one_hot_df = one_hot_df.astype(int)

movies_cleaned_encoded = movies_cleaned.join(one_hot_df)

# Filme ohne relevante Genres entfernen
movies_cleaned = movies_cleaned_encoded[movies_cleaned_encoded[relevante_genres].any(axis=1)]
print("Ausgabe Dataset mit gefilterten Genre",movies_cleaned) # (92434, 35)

"""
                                        Bereinigung und Handhabung von Ausreißern im Film-Datensatz:

1. Filtern von Filmen mit geringer Anzahl an Bewertungen:
   - Filme mit weniger als 500 Bewertungen werden aus dem Datensatz entfernt
   - Nur Filme mit ueber 500 numVotes koennen eine zuverlaessige Aussage liefern (wenig gevotete Filme mit uebermaeßig guten Ratings verzehren Statistik)
   - Sicherstellung, dass nur Filme mit ausreichend Bewertungen in die Modellbildung einfließen.

2. Ausreißeranalyse mit dem Interquartilsabstand (IQR):
   - Fuer ausgewaehlte Spalten werden Ausreißer mithilfe des IQR-Verfahrens identifiziert. Dies geschieht in der Funktion `detect_outliers_iqr`, die:
     - Den ersten und dritten Quartil (Q1 und Q3) berechnet
     - Den IQR (Interquartilsabstand) ermittelt.
     - Den unteren und oberen Grenzwert für die Ausreißerbestimmung berechnet 
     - Alle Werte, die unterhalb der unteren oder oberhalb der oberen Grenze liegen, als Ausreißer markiert.
   - Diese Ausreißer werden mit Boxplots und Histogrammen visualisiert
   - Obwohl Ausreißer erkannt werden, werden sie nicht gelöscht, da sie keine ungewoehnlichen Werte darstellen 

3. Markierung von Ausreißern:
   - Eine neue Spalte 'Outlier' wird hinzugefuegt, um die Ausreißer zu kennzeichnen (1 = True, 0 = False).

4. Paarweise Visualisierung der Ausreißer:
   - Eine Paarplot-Visualisierung wird durchgefuehrt, um die Beziehung zwischen den ausgewaehlten numerischen Spalten und den Ausreißern darzustellen. Dies hilft dabei, visuell zu erkennen, wie Ausreißer in verschiedenen Dimensionen verteilt sind.

5. Filme, die nach 2024 veröffentlicht wurden:
   - Filme, die nach 2024 veröffentlicht wurden, koennten zu neu sein, um realistische Bewertungen zu haben. Diese Filme werden entfernt, um Verzerrungen in der Analyse zu vermeiden.

6. Filme, die vor 1940 veröffentlicht wurden:
   - Filme, die vor 1940 veroeffentlicht wurden, koennten problematische Bewertungsmuster aufweisen und werden ebenfalls entfernt

"""

print("Anzahl der Zeilen und Spalten nach dem Filtern von Genres (und vor dem filtern von numVotes):", movies_cleaned.shape) # (95719, 35)

movies_cleaned = movies_cleaned[movies_cleaned["numVotes"] > 500]
print("Anzahl der Zeilen und Spalten nach dem Filtern von numVotes:", movies_cleaned.shape) # (19797, 35)

movies_cleaned_copy_without_null_with_one_hot = movies_cleaned.copy()
def detect_outliers_iqr(data, column):
    Q1 = data[column].quantile(0.25)  # 1. Quartil
    Q3 = data[column].quantile(0.75)  # 3. Quartil
    IQR = Q3 - Q1  # Interquartilsabstand
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
    return outliers, lower_bound, upper_bound

columns_to_analyze = ['averageRating', 'runtimeMinutes', 'startYear'] #numVotes wurden bereiets "gefiltert"

for column in columns_to_analyze:
    print(f"\nUntersuchung von Ausreißern in der Spalte '{column}':")

    # Ausreißer Identifikation
    outliers, lower, upper = detect_outliers_iqr(movies_cleaned, column)
    print(f"Anzahl der Ausreißer in '{column}': {len(outliers)}")
    print(f"Unterer Grenzwert: {lower}, Oberer Grenzwert: {upper}")

    # Ausreißer anzeigen
    if not outliers.empty:
        print(f"Beispiele für Ausreißer in '{column}':\n", outliers.head())
        print(f"Shape von Ausreißer in '{column}':\n", outliers.shape)

    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    sns.boxplot(data=movies_cleaned, x=column, color='skyblue')
    plt.title(f"Boxplot: {column}")

    plt.subplot(1, 2, 2)
    sns.histplot(movies_cleaned[column], kde=True, bins=30, color='skyblue')
    plt.axvline(lower, color='red', linestyle='--', label='Unterer Grenzwert')
    plt.axvline(upper, color='green', linestyle='--', label='Oberer Grenzwert')
    plt.title(f"Histogramm: {column}")
    plt.legend()
    plt.tight_layout()
    #save_fig(f"{column}_outliers")
    plt.show()
    plt.close()
# Ausreißer markieren da ich sie behalten will statt zu loeschen
movies_cleaned['Outlier'] = False
for column in columns_to_analyze:
    outliers, _, _ = detect_outliers_iqr(movies_cleaned, column)
    movies_cleaned.loc[outliers.index, 'Outlier'] = True

# Konvertiere die 'Outlier'-Spalte von True/False in 1/0
movies_cleaned['Outlier'] = movies_cleaned['Outlier'].astype(int)

print("\nAnzahl an Ausreißern, die markiert wurden insgesamt:", movies_cleaned['Outlier'].sum())

sns.pairplot(movies_cleaned, vars=columns_to_analyze, hue='Outlier', palette={True: 'red', False: 'blue'})
plt.suptitle("Paarweise Visualisierung der numerischen Spalten und Ausreißer", y=1.02)
#save_fig("asureisser_gesamt_ueberblick")
plt.show()
plt.close()

newest_movies = movies_cleaned[movies_cleaned['startYear'] > 2024]
count_of_newest_movies = newest_movies.shape[0]

print(f"Anzahl der Filme, die nach 2024 erscheinen: {count_of_newest_movies}") # 3
print("\n", newest_movies.head())
print("Anzahl der Zeilen und Spalten vor dem löschen der Filme, die nach 2024 erscheinen:", movies_cleaned.shape) # 19797, 36)

movies_cleaned = movies_cleaned[movies_cleaned['startYear'] <= 2024]

newest_movies = movies_cleaned[movies_cleaned['startYear'] > 2024]
count_of_newest_movies = newest_movies.shape[0]

print(f"Anzahl der Filme nach 2024 (nach dem Entfernen dieser Filme, zur Ueberpruefung): {count_of_newest_movies}") #0
print("Anzahl der Zeilen und Spalten nach dem Entfernen von Filmen, die nach 2024 erschienen sind:", movies_cleaned.shape) #(19794, 36)

old_movies = movies_cleaned[movies_cleaned['startYear'] < 1940]

old_movies = old_movies.shape[0]

print("Die Anzhal an Filmen, die vor 1940 erschienen sind:", old_movies) #514

movies_cleaned = movies_cleaned[movies_cleaned['startYear'] >= 1940]
print("Anzahl der Zeilen und Spalten nach dem Entfernen von Filmen, die vor 1940 erschienen sind:\n", movies_cleaned.shape) #  (19252, 36)

'''
                                    Extraktion der Variablen
- In diesem Schritt werden neue Merkmale (Features) erstellt, die zum Teil spaeter fuer das maschinelle Lernen genutzt werden
- Es wird auf der Basis von bestehenden Spalten erstellt: somit hat man sowohl die Rohinformation als auch die Kategorisierungen
'''

'''
                                    Klassifikation von Filmen 
- Hier wird eine Klassifikation der Filme auf Grundlage ihrer Durchschnittsbewertung ('averageRating') durchgefuehrt.
- Hinweis: es wird von der Zielvariable averageRating abgeleitet und kann deshalb spaeter nicht als Feature genutzt werden
- Anzahl der Filme pro rating category rating_category (meisten Filme sind mittelmaeßig bewertet):
    3    6217
    2    5639
    1    3853
'''
def rating(rating):
    if rating>=7.0:
        return 1 #sehr gut
    elif rating>=6.0:
        return 2 #gut
    else:
        return 3 #mittelmaeßig

movies_cleaned['rating_category']= movies_cleaned['averageRating'].apply(rating)
print("Das Dataset mit der Spalte rating category:\n",movies_cleaned.head())
print("Anzahl der Filme pro rating category",movies_cleaned['rating_category'].value_counts()) #3=7090,  2= 6524, 1 =4769

'''
                            Klassifikation von Filmen anhand runtime
- Hier wird eine Klassifikation der Filme auf Grundlage ihrer Laufzeit ('runtimeMinutes') durchgefuehrt.
Anzahl der Filme pro runtime category runtime_category (meitens sind Filme zwichen 90-120 min. lang)
90     11447
89      4307
120     3498
                            
'''
def classify_runtime(runtime):
    if runtime >= 120:  # Laufzeit größer oder gleich 120 Minuten --> sehr lang
        return 120
    elif 90 <= runtime < 120:  # Laufzeit zwischen 90 und 119 Minuten --> normal
        return 90
    elif runtime < 90:  # Laufzeit unter 90 Minuten --> eher kurz
        return 89

movies_cleaned['runtime_category'] = movies_cleaned['runtimeMinutes'].apply(classify_runtime)


print("Das Dataset mit der Spalte runtime category:\n",movies_cleaned[['runtimeMinutes', 'runtime_category']].head())
print("Anzahl der Filme pro runtime category",movies_cleaned['runtime_category'].value_counts())

'''
                            Hinzufuegen einer 'Decade' Spalte:
- Diese neue Spalte enthaelt das Jahrzehnt, in dem der Film veroeffentlicht wurde.
- Dies erfolgt durch ganzzahlige Division des Veroeffentlichungsjahrs (startYear) durch 10 und anschließende Multiplikation mit 10.
'''

movies_cleaned['decade'] = (movies_cleaned['startYear'] // 10) * 10
print("Decade Variable hinzugefügt:\n", movies_cleaned.head())


'''     
                Kategorisierung Director popularity (abgeleitet von average_rating)
- Hier wird eine Klassifikation der Director auf Grundlage der durchschnittlichen Bewertungen, die ein Director aud imdb hat('averageRating') durchgefuehrt.
- Hinweis: auch hier wird die Attribute von der Zielvariable averageRating abgeleitet und kann deshalb spaeter nicht als Feature genutzt werden                
'''
director_popularity = movies_cleaned.groupby('director_encoded')['averageRating'].mean()
movies_cleaned['director_popularity'] = movies_cleaned['director_encoded'].map(director_popularity)
'''
                        Zaehlen der Filme pro Director + Writer (mit den codierten IDs):
- In diesem Abschnitt wird gezaehlt, wie viele Filme jeder Director/Writer im Datensatz hat 
- Die Werte zeigen auf wer eventuell aktiver/inaktiver ist
- Die 'startYear' Spalte wird verwendet, um die Anzahl der Filme pro Director zu ermitteln.
- Diese Information wird als neue Spalte bzw. Attribut und spaeter als Feature 'director_film_count' zugewiesen.
'''
director_film_count = movies_cleaned.groupby('director_encoded')['startYear'].count()
movies_cleaned['director_film_count'] = movies_cleaned['director_encoded'].map(director_film_count)

writer_film_count = movies_cleaned.groupby('writer_encoded')['startYear'].count()
movies_cleaned['writer_film_count'] = movies_cleaned['writer_encoded'].map(writer_film_count)

'''
                    Berechnung der Popularitaet eines Directors basierend auf der Anzahl der Stimmen:
- In diesem Schritt wird die Popularitaet eines Directors durch die Anzahl der Stimmen ('numVotes') gemessen.
- Statt des durchschnittlichen Ratings wird hier die Gesamtzahl der Stimmen für die Filme eines Directors verwendet.
- Diese Information wird in der neuen Spalte 'director_popularity_by_votes' gespeichert und kann, da sie 
  jetzt nicht mehr von average_rating abgeleitet ist, als Feature verwendet werden
'''
director_vote_sum = movies_cleaned.groupby('director_encoded')['numVotes'].sum()
movies_cleaned['director_popularity_by_votes'] = movies_cleaned['director_encoded'].map(director_vote_sum)


'''
                                        Genre basierte Popularität (Anzahl der Votes):
- Die Popularitaet eines Genres wird durch die Gesamtzahl der Votes fuer alle Filme dieses Genres gemessen.
- Die Funktion 'get_genre_votes' extrahiert die Genres eines Films, und fuer jedes Genre wird die Gesamtzahl der Votes berechnet.
- In der neuen Spalte 'movies_with_this_genre_voted' wird die durchschnittliche Popularitaet jedes Genres gespeichert
'''
def get_genre_votes(genre):
    genre_list = genre.split(',')
    return genre_list


# Erstellung einer Liste von allen Genres und ihren numVotes
genre_votes = []

for idx, row in movies_cleaned.iterrows():
    genres = row['genres']
    num_votes = row['numVotes']
    genre_list = get_genre_votes(genres)

    for genre in genre_list:
        genre_votes.append((genre, num_votes))

genre_votes_df = pd.DataFrame(genre_votes, columns=['genre', 'numVotes'])

genre_vote_sum = genre_votes_df.groupby('genre')['numVotes'].sum().reset_index()

def get_genre_vote_sum(genre):
    genre_list = genre.split(',')
    genre_vote_values = [genre_vote_sum[genre_vote_sum['genre'] == g]['numVotes'].values[0] for g in genre_list]
    return np.mean(genre_vote_values)

movies_cleaned['movies_with_this_genre_voted'] = movies_cleaned['genres'].apply(get_genre_vote_sum)

'''
                                            Erstellen neuer finalen + bereinigten CSV
- Die neue CSV enthaelt den Datensatz ohne Nullwerte, mit codiereten Writer, Director und Genre und mit den neuen Spalten 
- Sie wurde ebenso gepusht und aus diesem Grund ist die Zeile auskommentiert                                           
'''
#movies_cleaned.to_csv("final_correct_encoded_dataset_after_cleaning_with_categorizations.csv", index=False)


'''
                                    Explorative Datenanalyse
'''
print("Die Spalten, die existieren:\n",movies_cleaned.columns)
print("Erste 5 Zeilen nach dem kompletten Filtern:\n", movies_cleaned[['primaryTitle','startYear','runtimeMinutes','genres','averageRating','numVotes']].head()) #nun habe ich sehr viele Spalten und wähle, deshalb nur die für die Ausgabe relevanten Spalten aus
print("Alle Filmtitel mit der durchschnittlichen Bewertung:\n",movies_cleaned[["primaryTitle","averageRating"]])
print("Nur Filme, dessen Bewertung ueber 6 ist:\n", movies_cleaned["averageRating"] > 6)
print("Anzahl der Duplikate in 'tconst':", movies_cleaned["tconst"].duplicated().sum()) #Duplikate in 'tconst' = 0

print("Durchschnittliche Bewertung pro Genre:\n", movies_cleaned.groupby("genres")["averageRating"].mean())

numerical_data = movies_cleaned.select_dtypes(include=['float64', 'int64'])
print("Nummerischen Daten im Dataset:\n", numerical_data.columns)

'''
            horizontalen Balkendiagramm-Plot: Top 10 Filme und ihr Rating
- erkennbar ist der Einfluss der Bollywoodindustrie            
'''
movies_to_plot = movies_cleaned.sort_values("averageRating", ascending=False).head(10)
print("Top 10 Filme nach Bewertung:\n", movies_to_plot[['primaryTitle','averageRating','numVotes','decade','genres']])

# Plotten der Top 10 Filme
plt.figure(figsize=(20, 20))
plt.barh(movies_to_plot["primaryTitle"], movies_to_plot["averageRating"], color="skyblue")
plt.xlabel("Durchschnittsbewertung")
plt.ylabel("Filmtitel")
plt.title(f"Top 10 Filme nach Bewertung")
plt.gca().invert_yaxis()  # Höchste Bewertungen oben
save_fig("top_10_filme_nach_rating")
plt.show()
plt.close()

'''
Histogramme mit histplot --> wie oft bestimmte Ratings bei allen Filmen vorkommen: 6,5 ist die häufigste Bewertung

'''
sns.histplot(movies_cleaned["averageRating"], kde=True, bins=30, color='skyblue')
plt.title("Verteilung der Bewertungen bzw. dem Rating")
plt.xlabel("Rating")
plt.ylabel("Häufigkeit")
save_fig("verteilung_der_bewertung")
plt.show()
plt.close()


''''
Barplot anhand Top 10 Bewertung nach Genre 
wobei die Genres auf der x-Achse und die durchschnittlichen Bewertungen auf der y-Achse dargestellt sind.
'''
average_ratings = movies_cleaned.groupby('genres')['averageRating'].mean().sort_values(ascending=False)

top_genres = average_ratings.head(10)

plt.figure(figsize=(26, 26))
sns.barplot(x=top_genres.index, y=top_genres.values, hue=top_genres.index, legend=False, palette="viridis")

plt.xlabel("Genre")
plt.ylabel("Durchschnittliches Rating")
plt.title("Top 10 Durchschnittliche Bewertungen nach Genre")

plt.xticks(rotation=45, ha='right')
#save_fig("top_10_genre_rating")
plt.show()
plt.close()


'''
                    Top 10 Genres ermitteln und ihre Häufigkeit (Barplot)
- Drama ist Spitzenfuehrer                    
'''
expanded_genres = movies_cleaned["genres"].str.split(",", expand=True).stack().reset_index(level=1, drop=True)

# Entfernen von führende und nachfolgende Leerzeichen von den Genre-Namen
expanded_genres = expanded_genres.str.strip()

top_genres = expanded_genres.value_counts().head(10)
print("Top 10 Genre und ihre Häufigkeit:\n", top_genres)

# Plotten der Top 10 Genres
top_genres.plot(kind='bar', figsize=(18, 12), color='skyblue')
plt.title("Top 10 Häufigste Genres")
plt.xlabel("Genres")
plt.ylabel("Häufigkeit")
plt.xticks(rotation=55, ha='right')
#save_fig("10_haeufigsten_genres")
plt.show()
plt.close()

'''
            Director und ihre Anzahl an Filme: ermitteln welche Director aktiver und welche weniger dominant
- grundsaetzlich hat kein Director uebermaeßig viele Filme im Dataset: es ist scheinbar gut verteilt            
'''
expanded_directors = movies_cleaned["directorNames"].str.split(",", expand=True).stack().reset_index(level=1, drop=True) #in einer Zelle stehen meists mehrere Names, deshalb split

# Entfernen führender und nachfolgender Leerzeichen von Namen
expanded_directors = expanded_directors.str.strip()

top_directors = expanded_directors.value_counts().head(10)
print("Top 10 Director und ihre Anzahl an Filmen:\n", top_directors)


top_directors.plot(kind='bar', figsize=(20, 10), color='skyblue')
plt.title("Top 10 Regisseure mit den meisten Filmen")
plt.xlabel("Regisseur")
plt.ylabel("Anzahl der Filme")
plt.xticks(rotation=30, ha='right')
#save_fig("aktivsten_10_regisseure")
plt.show()
plt.close()

'''
                    Writer und ihre Anzahl an Filme: ermitteln welche Writer aktiver und welche weniger dominant 
-- Unknown ist auf platz 1, da oft der Writer unbekannt ist
'''
expanded_writers = movies_cleaned["writerNames"].str.split(",", expand=True).stack().reset_index(level=1, drop=True)
expanded_writers = expanded_writers.str.strip()

top_writers = expanded_writers.value_counts().head(10)
print("Top 10 Writers und ihre Anzahl an Filmen:\n", top_writers)

top_writers.plot(kind='bar', figsize=(20, 10), color='skyblue')
plt.title("Top 10 Drehbuchautoren mit den meisten Filmen")
plt.xlabel("Drehbuchautor")
plt.ylabel("Anzahl der Filme")
plt.xticks(rotation=41, ha='right')
#save_fig("aktivsten_10_writer")
plt.show()
plt.close()


print("Durchschnittliches Rating pro Filmdauer:\n", movies_cleaned.groupby('runtimeMinutes', observed=True)['averageRating'].mean()) #laengere Filme scheinbar hoehere Bewertungen

print("Beschreibung der Daten  nur nummmerische:\n",movies_cleaned.describe())

print("Filme, die laenger als 180 Minuten gehen:\n",movies_cleaned[movies_cleaned["runtimeMinutes"] >= 180] ["primaryTitle"]) #149
avg_votes_per_year = movies_cleaned.groupby("startYear")['numVotes'].mean().sort_index(ascending=True)

'''
                                        Zusammenhang zwischen Jahr und denn votes
- erkennbar, dass neuere Filme (ab 2000) mehr numVotes haben, als aeltere                                        
'''
print("Filme aus diesen Jahren, haben im durchschnitt folgende numVotes",avg_votes_per_year)


plt.figure(figsize=(12, 6))
sns.barplot(x=avg_votes_per_year.index, y=avg_votes_per_year.values, palette='viridis')
plt.title('Durchschnittliche Votes pro Jahr')
plt.xlabel('Erscheinungsjahr')
plt.ylabel('Durchschnittliche Anzahl der Votes')

# X-Achse: nur jedes 5. Jahr ausgewaehlt
plt.xticks(ticks=range(0, len(avg_votes_per_year), 5), labels=avg_votes_per_year.index[::5], rotation=45)
plt.tight_layout()
#save_fig("votes_pro_jahr")
plt.show()
plt.close()

'''
        Average Rating for each Director: mithilfe von director_popularity
- die top 10 haben alle aehnliche Popularitaet        
'''
top_directors_popularity = movies_cleaned[['directorNames', 'director_popularity']].drop_duplicates()
top_directors_popularity = top_directors_popularity.sort_values(by='director_popularity', ascending=False).head(10)
print("Top 10 Regisseure nach Popularität:\n", top_directors_popularity)

plt.figure(figsize=(10, 6))
top_directors_popularity.plot(kind='barh', x='directorNames', y='director_popularity', color='purple', legend=False)

plt.title('Top 10 Regisseure nach Popularität', fontsize=16)
plt.xlabel('Durchschnittliche Popularität', fontsize=12)
plt.ylabel('Regisseur', fontsize=12)
plt.gca().invert_yaxis()  # besten Regisseure oben

plt.tight_layout()
#save_fig("director_popularity")
plt.show()
plt.close()

'''
                    laengsten filme und die entsprechende Filmtitel
- alle laenger als 300 min.
- 2 sind sogar laenger als 400 min.                    
'''
top10_len= movies_cleaned.nlargest(10,'runtimeMinutes') [['primaryTitle', 'runtimeMinutes']] \
.set_index('primaryTitle')
print("Top 10 laengster Filme:\n", top10_len)
plt.figure(figsize=(30, 20))
sns.barplot(x='runtimeMinutes', y=top10_len.index, data=top10_len)
plt.xlabel('Filmdauer (in Minuten)')
plt.ylabel('Filmtitel')
plt.title('Top 10 laengsten Filme')
plt.yticks(rotation=0)
#save_fig("10_laengsten_filme")
plt.show()
plt.close()

'''
                                    Verteilung der runtimeMinuets
- im Schnitt unter 100 Minuten                                    
'''
plt.figure(figsize=(12, 6))
runtime = sns.histplot(movies_cleaned['runtimeMinutes'], color="pink", kde=True)
plt.title("Verteilung der Filmlaufzeiten", fontsize=20)
plt.xlabel("Runtime (min)", fontsize=15)
#save_fig("verteilung_der_filmlaufzeit")
plt.show()
plt.close()
'''
                    Anzhal an Filme, die pro Jahr erschienen sind 
- wie man der Grafik entnehmen kann sind 2018 die meisten Filme erschienen (777) und in 1944 die wenigsten (44)                   
'''
print("Anzahl an Filmen, die erschienen sind pro Jahr:\n", movies_cleaned['startYear'].value_counts())
print("2018 sind die meisten Filme erschienen. Es waren so viele Filme::\n", movies_cleaned['startYear'].value_counts().max())
print("1944 sind die wenigsten Filme erschienen. Es waren so wenig Filme:\n", movies_cleaned['startYear'].value_counts().min())

movies_count_per_year = movies_cleaned['startYear'].value_counts().sort_index()

plt.figure(figsize=(12, 6))
sns.barplot(x=movies_count_per_year.index, y=movies_count_per_year.values, palette='viridis')

plt.title('Anzahl an Filmen pro Jahr', fontsize=16)
plt.xlabel('Jahr', fontsize=12)
plt.ylabel('Anzahl der Filme', fontsize=12)
plt.xticks(rotation=90)

plt.tight_layout()
#save_fig("veroeffentlichte_filme_pro_jahr")
plt.show()
plt.close()
'''
                         meistbewertester Film
'''
most_voted_movie = movies_cleaned.loc[movies_cleaned['numVotes'].idxmax()]

# Fight Club mit so vielen Bewertungen: 241 7873
print(f"Meist bewertester Film: {most_voted_movie['primaryTitle']} mit so vielen Bewertungen: {most_voted_movie['numVotes']}")

'''
                        Anzeigen von Top 10 best bewertesten Filme und seine Directors
- Keiner kommt bei den Top 10 Filmen mehr als 1x  vor                        
'''
movie_rating_director = movies_cleaned[["primaryTitle", "averageRating", "numVotes", "directorNames"]]
movie_rating_director = movie_rating_director.sort_values("averageRating", ascending=False).head(10)

top10_len2 = movie_rating_director[['primaryTitle', 'averageRating', 'directorNames']] \
    .set_index('primaryTitle')

print("Die Top 10 bestbewerteten Filme und ihre Directors:\n", top10_len2)

plt.figure(figsize=(20, 12))
sns.barplot(x='averageRating', y=top10_len2.index, data=top10_len2, hue="directorNames", dodge=False)
plt.xlabel('Rating')
plt.ylabel('Filmtitel')
plt.title('Top 10 bestbewerteten Filme und ihre Directors')
#save_fig("top_10_filme_mit_regisseur")
plt.show()
plt.close()


'''
                                Finde durchschnittliche Bewertung je Jahr
- der Konsolenausgabe nach erkennbar, dass aeltere Filme bessere Ratings haben als neue                                
 '''
print("In diesen Jahren haben Nutzer im durschnitt folgende Bewertungen verteilt",movies_cleaned.groupby('startYear')['averageRating'].mean().sort_values(ascending=False))

'''
                                                    Unique Werte in genres finden
'''
movies_cleaned['genres']
list = []
for value in movies_cleaned['genres']:
    value = str(value)
    list.append(value.split(','))

one_d=[]
for item in list:
    for item in item:
        one_d.append(item)

uni_list =[]
for item in one_d:
    if item not in uni_list:
        uni_list.append(item)

'''
                        Wie viele Filme gibt es pro Genre?
'''

# Nur relevante Genres zählen
filtered_genres = [genre for genre in one_d if genre in relevante_genres]

# Zähle die relevanten Genres
print("Filme pro relevantes Genre", Counter(filtered_genres))
'''
                                        Korrelation
Dieser Abschnitt erzeugt eine Heatmap der Korrelationsmatrix und visualisiert, wie stark die numerischen Variablen miteinander korrelieren (wie abhaengig sie von einander sind).
Der Farbverlauf zeigt die Stärke der Korrelationen an:
- Ein Wert nahe 1 bedeutet eine starke positive Korrelation,
- Ein Wert nahe -1 bedeutet eine starke negative Korrelation,
- Ein Wert nahe 0 bedeutet keine Korrelation.

- Da die Genre-Spalten im One-Hot-Encoding habe ich in der gesamten Korrelationsmatrix ausgelassen, da diese die Grafik ueberladen
- Zusaetzlich wird die Korrelation jeder numerischen Variable mit der Zielvariablen 'averageRating' visualisiert. Hierbei wird eine sortierte Barplot-Darstellung verwendet, um die staerkste Korrelation mit der Zielvariable hervorzuheben.
'''
correlations_without_genre = numerical_data.drop(columns=['Action','Adventure','Drama','Horror','Fantasy','Mystery','Animation','Thriller','Comedy','Romance','Crime','Musical','Sci-Fi','Sport'
    ,'Music','War','Family','Documentary','Biography','Western','History','Film-Noir'])

plt.figure(figsize=(12, 8))
sns.heatmap(correlations_without_genre.corr(), annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)

plt.title('Korrelation der numerischen Variablen', fontsize=16)
plt.tight_layout()
#save_fig("korrelationsmatrix_gesamt")
plt.show()
plt.close()

# Korrelation aller Spalten mit der Zielvariablen
correlations_with_target = numerical_data.corr()['averageRating'].sort_values(ascending=False)

# Visualisiere die Korrelation mit der Zielvariablen
plt.figure(figsize=(8, 6))
sns.barplot(x=correlations_with_target.values, y=correlations_with_target.index, palette='coolwarm')
plt.xlabel('Korrelation mit averageRating', fontsize=12)
plt.title('Korrelation mit averageRating', fontsize=16)
plt.tight_layout()
#save_fig("korrelationsmatrix_zielvariable")
plt.show()
plt.close()
