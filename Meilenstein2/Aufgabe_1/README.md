# Aufgabe 1 – Filmdatenanalyse mit IMDB
Diese Dokumentation beschreibt den vollständigen Prozess der Datenaufbereitung, Analyse und Modellbildung mit dem Ziel, ein Vorhersagemodell zu entwickeln. Angefangen bei der Auswahl und Bereinigung der Daten über die Extraktion relevanter Features bis hin zur Implementierung eines XGBoost-Modells, legt die Dokumentation Schritt für Schritt den Ablauf dar. Zusätzlich werden Visualisierungen eingesetzt, um die Bedeutung einzelner Features und die Modellleistung zu verdeutlichen.

## Inhaltsverzeichnis
1. [Ziel der Anwendung](#ziel-der-anwendung)
2. [Übersicht](#übersicht)
3. [Sampleaufbereitung](#sampleaufbereitung)
   - [Dateien einlesen](#dateien-einlesen)
   - [Verknüpfen der Datensätze:](#verknüpfen-der-datensätze)
   - [Reduzierung der Datenmenge:](#reduzierung-der-datenmenge)
   - [Zuordnung der director und writer Namen:](#zuordnung-der-director-und-writer-namen)
   - [Speichern des finalen Datensatzes:](#speichern-des-finalen-datensatzes)
4. [Datenexploration](#datenexploration)
   - [Importe](#importe)
   - [Irrelevanten Spalten](#irrelevanten-spalten)
   - [Nullwerte](#nullwerte)
   - [Label Encoding](#label-encoding)
   - [Tatsächlich fehlende Werte](#tatsächlich-fehlende-werte)
   - [One hot encoding](#one-hot-encoding)
   - [Ausreisser](#ausreisser)
5. [Extraktion der Variablen](#extraktion-der-variablen)
6. [Statistiken und Visualisierungen](#statistiken-und-visualisierungen)
7. [Modellbildung](#modellbildung)
8. [Modellevaluation](#modellevaluation)
    


## Ziel der Anwendung
Das Ziel dieser Aufgabe ist es ein Modell zu entwickeln, das die IMDB-Bewertung (Sterne-Rating von 0 bis 10) eines Films vorhersagen kann. Dies erfordert einen Prozess in mehreren Schritten.

## Übersicht
Insgesamt sind beim Entwickeln 3(+1) Klassen entstanden:
   - Sampleaufbereitungsklasse: hier passiert das Zusammenführen der verschiedenen tsv Dateien, um eine CSV Datei
     vorzubereiten, die als Basis Datei für die Analyse verwendet wird
   - Datenexplorationsklasse: in dieser Klasse befindet sich der meiste Quellcode, da hier sowohl die                   Datenbereinigung als auch die Extraktion der Variablen und auch die Visualisierungen durchgeführt  
     werden. Zugegebenermaßen ist diese Klasse recht umfangreich, da viele Statistiken erstellt wurden, um viele Faktoren zu betrachtet, die für den Erfolg des Filmes beitragen können. Außerdem helfen die Statistiken mit den Datensatz vertrauter zu werden.
   - Xgboostklasse: die finale Modellbildung beginnt in dieser Klasse. Sie beinhaltet das Skalieren                ausgwählter Features, den Xgboost Regrossor, das Trennen des Test- und Trainingssets, die                     tatsächliche Vorhersage und die Auflistung der Features nach Wichtigkeit für das Modell.
   - RandomForestRegressorklasse: sie wurde verwendet, um den Gedankengang des Projekts nachzuvollziehen und erste Modellbildungsversuche durchzuführen. Das finale Modell ist jedoch die XGBoost-Klasse, da sie den besten und offiziell verwendeten R²-Score liefert und somit die Grundlage für die abschließende Bewertung darstellt.

Zusammengefasst als Tabelle:

| **Klasse**               | **Beschreibung**                                                                                   |
|--------------------------|---------------------------------------------------------------------------------------------------|
| Sampleaufbereitungsklasse | Vorbereitung der Basis-CSV durch Merging der .tsv-Dateien.                                       |
| Datenexplorationsklasse   | Datenbereinigung, Variablenextraktion, Statistiken und Visualisierungen.                         |
| XGBoostklasse             | Modellbildung mit Feature-Skalierung, XGBoost-Training und Feature-Wichtigkeit.                 |
| RandomForestRegressor     | Erste Modellbildungsversuche zur Nachvollziehbarkeit des Gedankengangs. Dient als Vergleich, liefert jedoch nicht die gleiche Modellqualität wie das XGBoost-Modell. |


## Sampleaufbereitung
Dieser Abschnitt beschreibt den Prozess des Einlesens, Verknüpfens und Bearbeitens der verschiedenen Datensätze, um eine Basis CSV Datei mit einem reduzierten Datensatz zu erstellen, der für die Analyse verwendet werden kann. Die einzelnen tvs Dateien, die ich für mein Projekt nutze sind von der offiziellen IMDb Seite und können unter folgendem Link aufgerufen werden: 
https://datasets.imdbws.com/ 

## Dateien einlesen
Zunächst werden vier verschiedene tsv Dateien eingelesen.
1. title.basics.tsv.gz
Diese Datei enthält folgende grundlegende Informationen zu Filmen und Serien: 
- const: Eindeutige alphanumerische ID für Personen.
- titleType: Art des Titels (z. B. Film, Kurzfilm, Serie, Episode).
- primaryTitle: Geläufiger Titel, häufig genutzt in der Vermarktung.
- originalTitle: Originaltitel in der Originalsprache.
- isAdult: Gibt an, ob der Titel für Erwachsene ist (0 = Nein, 1 = Ja).
- startYear: Erscheinungsjahr; bei Serien das Startjahr.
- endYear: Endjahr für Serien (für andere Titeltypen \N).
- runtimeMinutes: Laufzeit des Titels in Minuten.
- genres: Bis zu drei Genres, die mit Kommata getrennt sind

2. title.ratings.tsv.gz enthält 3 Attributen:
- tconst: Alphanumerische, eindeutige ID des Titels.
- averageRating: Gewichteter Durchschnitt aller individuellen Nutzerbewertungen.
- numVotes: Anzahl der abgegebenen Bewertungen für den Titel.

3. title.crew.tsv.gz sie besteht aus:
- tconst: Alphanumerische, eindeutige ID des Titels.
- directors: Array von nconst-Werten, die die Regisseur(e) des Titels darstellen.
- writers: Array von nconst-Werten, die die Drehbuchautor(en) des Titels darstellen.

4. name.basics.tsv.gz mit:
- nconst: Alphanumerische, eindeutige ID der Person.
- primaryName: Name, unter dem die Person am häufigsten aufgeführt wird.
- birthYear: Geburtsjahr im Format YYYY.
- deathYear: Sterbejahr im Format YYYY, falls zutreffend; ansonsten \N.
- primaryProfession: Array mit bis zu drei Hauptberufen der Person.
- knownForTitles: Array von tconst-Werten, die Titel darstellen, für die die Person bekannt ist.

Ich habe mich bewusst dagegen entschieden, die Dateien title.principals.tsv.gz und title.akas.tsv.gz in meinen Datensatz zu integrieren. Der Grund dafür ist, dass die Datenmenge bei jedem weiteren zusammenführen kleiner wurde, welches die Analyse beeinträchtigt hätte. Zusätzlich war die Verarbeitung des erweiterten Datensatzes zu überlastend für meinen Laptop. An dieser Stelle möchte ich anmerken, dass ich es etwas ungünstig fand, dass die originalen tsv Dateien keine Informationen bezüglich des Budget oder Umsatzes der Filme zu Verfügung stellen. Zu Beginn meines Projektes habe ich mit einem anderen Dataset gearbeitet, welches diese Information beinhaltete, jedoch waren diese Informationen nicht zuverlässig genug und der Datensatz auch zu klein.

## Verknüpfen der Datensätze:
Da die einzelnen DataFrames mit eindeutigen Schlüsseln arbeiten, war das Mergen (zusammenführen) der Dateien möglich. Durch das Zusammenführen der Dateien entstehen vollständige Datensätze, die sowohl grundlegende Informationen zu den Filmen als auch Bewertungen und Besetzungs Informationen enthalten und eine Grundlage für den Meilenstein 2 bieten.
In unserem Repository habe ich die meisten tsv Dateien pushen können, jedoch war die name.basics.tsv Datei zu groß, um sie zu pushen.
![Screenshot (716)](https://github.com/user-attachments/assets/e8b2e044-97be-4b5d-b2f4-4ae126df454b)


## Reduzierung der Datenmenge:
Die Aufgabe bezieht sich auf einer Analyse von Filmdaten, doch der Datensatz enthält sowohl Daten für Filme als auch Serien. Den zusammengeführten Datensatz konnte man über den titleType 'movie' nach Filmen filtern, da nur diese benötigt werden:

print("Ersten Zeilen des kombinierten DataFrames merged_data:\n",merged_data.head())
movies_only = merged_data[merged_data['titleType'] == 'movie']

print(f"Anzahl der Filme im Datensatz: {len(movies_only)}")

Output:


![Screenshot (744)](https://github.com/user-attachments/assets/7dfc1373-28ca-443a-ad00-db086640b1a2)

Nach dem Filtern des Datensatzes nach den titelType bleibt eine reduzierte Anzahl von 323 421 Zeilen übrig. Dies zeigt, dass der ursprüngliche Datensatz durch das Filtern auf Filme erheblich verkleinert wurde.

Für eine repräsentative Stichprobe wurden 100 000 zufällige Filme in die CSV Datei geschreiben, anstatt  nur die ersten 100 000 Zeilen zu verwenden. Eine größere Menge konnte nicht exportiert werden, da dies wieder meinen Laptop überlastet hätte und der Prozess abgebrochen werden musste. Zu Beginn habe ich noch veruscht die title.basics.tsv.gz und title.akas.tsv.gz miteinzubeziehen, aber dies hat meinen Datensatz verkleinert. Vermutlich war dies auf eine hohe Anzahl von Nullwerten in den zusätzlichen Dateien zurückzuführen.

## Zuordnung der director und writer Namen:
Da ohne die name.bascics Datei nur IDs für Regisseure und Drehbuchautoren vorliegen, wird eine Zuordnung dieser IDs zu den tatsächlichen Namen aus der Datei name.basics.tsv.gz vorgenommen. Dies geschieht über eine Funktion, die die IDs in Namen umwandelt. Besonders bei den Statistiken eignen sich die tatsächlichen Namen zu verwenden, ab der Modellbildung jedoch benötigen wir diese Namen nicht mehr.

## Speichern des finalen Datensatzes:
Der bereinigte und reduzierte Datensatz, der jetzt die Namen von Regisseuren und Drehbuchautoren enthält, wird in einer CSV-Datei (reduced_and_merged_data_with_names.csv) gespeichert. Diese Datei kann nun für die Modellierung, Analyse oder weitere Verarbeitung genutzt werden. Wichtig anzumerken, diese Datei bildet die Basis und ist somit 'unbereinigt'.
Wichtig: die Zeile code zum Speichern der Daten ist einkommentiert, da die CSV Datei mit gepusht wurde und schon vorliegt.

## Datenexploration
Die Klasse mit den meisten Zeilen Code beinhaltet sowohl das Bereinigen der Daten, die Visualisierungen als auch die Extraktion von Variablen.
## Importe
Folgende Python-Bibliotheken werden in diesem Skript verwendet:
| Bibliothek                           | Beschreibung                                                      |
|---------------------------------------|-------------------------------------------------------------------|
| `pandas`                              | Für Datenmanipulation und -analyse.                              |
| `numpy`                               | Für mathematische und numerische Operationen.                    |
| `matplotlib` & `seaborn`              | Für Visualisierungen und grafische Darstellungen.                |
| `sklearn.preprocessing.LabelEncoder`  | Für das Label-Encoding von kategorischen Daten.                  |
| `os`                                  | Für Dateipfadoperationen und das Erstellen von Verzeichnissen. Relevant für die Speicherung der Bilder   |


## Irrelevanten Spalten
Nach dem die aufbereitete CSV Datei eingelesen wird, werden die 
 Spalten bzw. Attributen 'endYear'(ist immer Null),'isAdult' (nicht relevant), 'originalTitle' (primaryTitle genügd), 'titleType'(wurde schon im voraus nach Filmen gefiltert) entfernt.  

## Nullwerte
Zu nächst ein Mal: das zusammengesetzte Dataset hat Nullwerte mit '\N' makiert, welches von pandas nicht als Nullwerte erkennbar ist, somnit mussten die Nullwerte zu NaN-Werte konvertiert werden.
Das Dataset hat grundsätzlich viele Zellen mit Nullwerten, daher wurde abgewogen an welchen Stellen das Löschen notwendig ist und wo man Zellen sinnvoll füllen kann. In folgendem Bild sieht man die ersten 5 Zeilen des Datasets und kann erkennen, dass Nullwerte vorliegen (hier sind noch die irrelevanten Spalten zu sehen).

movies = pd.read_csv("reduced_and_merged_data_with_names.csv")

print(movies.head())
![Screenshot (746)](https://github.com/user-attachments/assets/91ec596d-4207-4f42-85d7-4268d83af4bd)



Tatsächlich hilft es dem Modell, wenn es mehr Datensätze gibt, aus diesem Grund hat sich das Auffüllen fehlender Werte mit den Mittelwerten der Attribute als Lösung ergeben.
Nullwerte in den Spalten 'startYear' und 'runtimeMinutes' werden mit dem Mittelwert ersetzt, davor mussten diese jedoch in in nummerische Variablen umgewandelt werden. Auf folgendem Bild sieht man was für Datentypen die Spalten haben. 

movies.info()

Output:

![Screenshot (745)](https://github.com/user-attachments/assets/22fdc616-320f-4db9-a64a-89f1ddd5c430)



Fehlende Werte in den Spalten directors und writers werden mit einem Platzhalter ('nm0000000') gefüllt. Das dient als "Unbekannt" Kennzeichnung. Besonders die 'writer' Spalte hat viele Nullwerte aufgezeigt, daher wäre es ein großer Verlust an Daten wenn man alle Zeilen bzw. Filme löschen würde wo der Writer null ist.

## Label Encoding
Die Spalten 'directors' und 'writers' im Film-Datensatz enthalten jeweils eine Liste von IDs, die den Regisseuren und Drehbuchautoren zugeordnet sind. Diese IDs sind in ihrem ursprünglichen Format als objects hinterlegt und müssen für die weitere Analyse in numerische Werte umgewandelt werden. Dazu wird das Verfahren des Label-Encodings verwendet.
Das Label-Encoding wird angewendet, um jedem einzigartigen Wert in den Spalten 'directors' und 'writers' eine numerische Kennung zuzuweisen, wie die ID nur, dass es keine Buchstaben enthält. Dies ist notwendig, da maschinelles Lernen in der Regel mit numerischen Werten arbeitet, während die ursprünglichen Werte (IDs der Regisseure und Drehbuchautoren) als Strings bzw. objects vorliegen.
Die eindeutigen encodeden IDs sind nun eine feste numerische Kennung, die im Modell als Feature genutzt werden kann.
Der LabelEncoder von Scikit-Learn wird verwendet, um die IDs der Regisseure und Drehbuchautoren zu encodieren.
Die fit_transform-Methode von LabelEncoder wird für jede Spalte ausgeführt, um die IDs in numerische Werte umzuwandeln und gleichzeitig eine neue Spalte für die codierten Werte zu erstellen.

print("So sieht der Datensatz mit dem label-encoding von den nconst aus:\n",movies_cleaned[['directors', 'director_encoded', 'writers', 'writer_encoded']].head())

Output:

![Screenshot (750)](https://github.com/user-attachments/assets/32b05447-ead2-4ef2-a012-1e00351f94be)

## Tatsächlich fehlende Werte
Nach dem Ersetzen der Nullwerte für Attribute bei dennen man die Werrte mit einem sinnvollen Mittelwert füllen kann, blieb nur noch die Genre Spalte, die auf Nullwerte hingewiesen hat:

print("Fehlt irgendein Wert im Datensatz?", movies_cleaned.isna().sum().values.any())
print("Summe der fehlenden Werte:\n",movies_cleaned.isna().sum()) 


![Screenshot (747)](https://github.com/user-attachments/assets/0870c717-45c3-4a04-b935-38692e78deb0)


Bei der Attribute 'genres' kann man die fehlenden Zellen nicht sinnvoll füllen, somit wurden Zeilen mit fehlenden Genres gelöscht aus dem Datensatz. Dannach liegen keine Nullwerte mehr vor und der Datensatz wurde um 3430 Zeilen reduziert :

![Screenshot (748)](https://github.com/user-attachments/assets/a5dc0e52-7b7a-48f9-80c5-67692a53776a)


## One hot encoding
Die Spalte "genres" wird durch Kommata getrennt. Diese liegen im ursprünglichen Dataset als object vor, doch wie erwähnt wird beim Modell nur mit nummerischen Werten gearbeitet. Die Genres werden somit in numerische Werte umzuwandeln, damit sie als Features genutzt werden können. Genres wie 'News', 'Adult' oder 'Talkshow' haben die Statistiken verzehrt und sind generell ungewöhnlich. Aus diesem Grund wurden die Genre gefiltert und auch dafür war die nummerische Darstellung notwendig. Die Genres wurden somit One hot encoded.
Zu Beginn wurde eine Liste von relevanten Genres erstellt, die für die Analyse berücksichtigt werden sollten. Insgesamt sind es viele Genres, sodass viele Filme miteinbezogen werden konnten.
Die Genres werden für jeden Film als 1 oder 2 dargestellt. Jedes relevante Genre hat nun eine eigene Spalte, die im DataFrame erstellt wurde. In jeder Zeile wird überprüft, ob er das jeweilige Genre enthält und in der entsprechenden Spalte wird eine 1 für "Vorhanden/True" oder eine 0 für "Nicht vorhanden/False" gesetzt. Leider hat der Datensatz dadurch ernorm viele Spalten dazu bekommen, aber eine andere Lösung habe ich nicht gefunden.

print("Die Spalten, die existieren:\n",movies_cleaned.columns)

output: 

Die Spalten, die existieren:
 Index(['tconst', 'primaryTitle', 'startYear', 'runtimeMinutes', 'genres', 'averageRating', 'numVotes', 'directors', 'writers', 'directorNames', 'writerNames', 'director_encoded', 'writer_encoded', 'Action', 'Adventure', 'Drama', 'Horror', 'Fantasy', 'Mystery', 'Animation', 'Thriller', 'Comedy', 'Romance', 'Crime',
       'Musical', 'Sci-Fi', 'Sport', 'Family', 'Documentary', 'Biography', 'Western', 'History', 'Film-Noir', 'Music', 'War', 'Outlier', 'rating_category', 'runtime_category', 'decade', 'director_popularity', 'director_film_count', 'writer_film_count', 'director_popularity_by_votes', 'movies_with_this_genre_voted'],
      dtype='object')

Dies hat auch meine Konsolenausgabe beeinflusst, sie geht  jetzt sehr in die Breite, aus diesem Grund möchte ich den Output des One hot encoding Prozesses an der CSV Datei zeigen:

![Screenshot (749)](https://github.com/user-attachments/assets/d65ce5de-ae4d-4415-8edc-525e15efe986)


Auch hier kann man nicht alle Spalten erkennen, aber betrachtet man den Film aus der 3 Zeile:
es ist der Film '3 A.M. 3D' mit dem Genre 'Horror'. Man kann erkennen, dass in der Zeile 3 die Spalte Horror eine 1 aufzeigt und der Rest eine 0, da nur dieses Genre zutrifft.

Durch das Einführen der One hot encoding Tabelle liegen die Genre als nummerischen Wert vor. Es wurden nach dem Filtern 857 Zeilen gelöscht. Hier noch mal der Output nach dem Genre gelöscht wurden:

print("Anzahl der Zeilen und Spalten nach dem Filtern von Genres (und vor dem filtern von numVotes):", movies_cleaned.shape) 

Output:
Anzahl der Zeilen und Spalten nach dem Filtern von Genres (und vor dem filtern von numVotes): (95719, 35)

## Ausreisser 
Filme mit weniger als 500 Bewertungen werden aus dem Datensatz entfernt, da meiner Meinung nach nur Filme mit einer ausreichenden Anzahl an Bewertungen in die Modellbildung einfließen sollen.
Filme mit zu wenigen Bewertungen (weniger als 500) könnten verzerrte Ratings aufweisen, die keine zuverlässige Grundlage für die Analyse bieten. Alles was drüber ist empfinde ich als nicht ungewöhnlich und habe deshalb dies bezüglich nur diese eine Bedingung. 
Wenn mehr Einträge vorliegen würden, hätte man die Untergrenze höher setzen oder weiter beschränken können, jedoch würden sehr viele Daten verloren gehen, wenn die Grenze noch höher wäre und das liefert wiederum eine schlechtere Vorhersage.

movies_cleaned = movies_cleaned[movies_cleaned["numVotes"] > 500]
print("Anzahl der Zeilen und Spalten nach dem Filtern von numVotes:", movies_cleaned.shape) 

Output:
Anzahl der Zeilen und Spalten nach dem Filtern von numVotes: (19797, 35)

--> Man erkennt, dass der Datensatz um ca 75 000 Einträgen reduziert wurde, welches diegrößte Reduzierung im Rahmen der Bereinigung darstellt.

Als nächstes habe wurden die Ausreisser für nummerischen Spalten nämlich für averageRating, runtimeMinutes und startYear analysiert. Diese wurde unter Verwendung des IQR-Verfahrens durchgeführt. Es basiert auf den Quartilen (Q1 und Q3) und berechnet den Interquartilsabstand, der verwendet wird, um Ausreisser zu identifizieren.

![Screenshot (751)](https://github.com/user-attachments/assets/94f2e9fc-f16d-49f3-915e-7cdaae68fa47)

Sowohl schlechte Bewertungen als auch sehr gute Bewertung sind nicht umbedingt ungewöhnlich (beides gehört dazu), deshalb wurden die Ausreisser nicht entfernt.

Die runtimeMinutes Aussreisser:

![Screenshot (752)](https://github.com/user-attachments/assets/a7226d65-361a-4924-b48a-5b15c65cb6a4)

Hier gilt dasselbe, kurze als auch lange Filme sollten mit in die Analyse einbezogen werden, weil sie nicht ungewöhnlich sind.

StartYear hat interessanet Werte aufgewiesen:
![Screenshot (753)](https://github.com/user-attachments/assets/2efad05e-02a1-44e8-bef4-0084cb127b80)


Tatsächlich gab es Filme im Datensatz, die nach 2024 erschienen sind:

newest_movies = movies_cleaned[movies_cleaned['startYear'] > 2024]
count_of_newest_movies = newest_movies.shape[0]

print(f"Anzahl der Filme, die nach 2024 erscheinen: {count_of_newest_movies}") 
print("\n", newest_movies.head())


![Screenshot (754)](https://github.com/user-attachments/assets/f64db545-3193-46ba-ae0d-ca7d31aa6e4e)

Die meiner Meinung nach sinnvolle Lösung ist es, alle Filme, die vor 1940 erschienen sind zu entfernen, weil diese veraltete Bewertungsmuster aufweisen können und Filme, die nach 2024 erschienen sind zu entfernen, weil sie möglicherweise zu neu sind, um valide Bewertungen zu haben.

output des ganzes:
![Screenshot (756)](https://github.com/user-attachments/assets/e71aa2b2-8e0f-4025-b4ed-f7560b10963f)


Der Datensatz hat nur noch 19 252 Zeilen und die Bereinigung ist fertig. 

## Extraktion der Variablen
In diesem Schritt werden verschiedene neue Merkmale (Features) im Film-Datensatz extrahiert, die als Grundlage für maschinelles Lernen dienen werden. Sie bieten zusätzliche Perspektiven und Klassifikationen basierend auf den existierenden Daten.
Insgesamt sind 7 'extra Spalten' entstanden, davon können jedoch nur 4 für das Modell verwendet werden, da 2 der Spalten von der Zielvariable 'averageRating' abgeleitet sind. Würden man diese mit einbeziehen würde ein sehr guter R²-Score vorliegen, da in diesen Kategorien 'director_popularity' und 'rating_category' bereits Informationen aus der Zielvariable enthalten und somit das Ergebnis verfälschen würden. Ähnliches gilt auch für 'Outlier': die Markierung der Ausreißer erfolgt anhand von ungewöhnlich hohen oder niedrigen Bewertungen, was bedeutet, dass diese Spalte Informationen enthält, die eng mit der Zielvariable verknüpft sind.

| **Feature Name**                        | **Beschreibung**                                                                                       |
|-----------------------------------------|-------------------------------------------------------------------------------------------------------|
| `rating_category`                       | Klassifikation der Filme basierend auf der Durchschnittsbewertung: 1 = sehr gut, 2 = Gut, 3 = durchschnittlich |
| `runtime_category`                      | Klassifikation der Filme basierend auf der Laufzeit: 89  (alles unter 90 Minuten), 90 (90-120 Minuten), 120 Minuten (alles über 120 Minuten) |
| `decade`                                | Das Jahrzehnt, in dem der Film veröffentlicht wurde (z. B. 1990, 2000, 2010).                           |
| `director_popularity`                   | Bewertung die ein Regisseurs in diesem Datensatz im durchschnitt bekommt (abgeleitet aus `averageRating`).               |
| `director_film_count`                   | Anzahl der Filme, die ein Regisseur im Datensatz hat.                                                  |
| `writer_film_count`                     | Anzahl der Filme, die ein Drehbuchautor (Writer) im Datensatz hat.                                     |
| `director_popularity_by_votes`          | Die Popularität eines Regisseurs basierend auf der Gesamtzahl der Stimmen für seine Filme im Datensatz.            |
| `movies_with_this_genre_voted`          | Die durchschnittliche Popularität eines Genres basierend auf der Anzahl der Votes für Filme in diesem Genre. |
| `Outlier`                               | Markierung von Ausreißern im Datensatz, da ich sie nicht löschen wollte (1 = Ausreißer, 0 = kein Ausreißer).                            |

Hinweis: nach der Extraktiond der Variablen haben wir das endgültige Dataset mit dem wir in den naechsten Schritten arbeiten werden.
Die Zeile in der die CSV Datei (final_correct_encoded_dataset_after_cleaning_with_categorizations.csv) erstellt wird ist auch hier einkommentiert, da sie schon vorliegt.
## Statistiken und Visualisierungen
Insgesamt sind bei der Datenexploration 20 Grafiken entsanden. Die Statistiken zeigen interessante Muster, Korrelationen und Trends in Bezug auf Filme, deren Bewertungen auf.

Zusammenfassend habe ich mich mit diesen Faktoren beschäftigt:
- Welche Filme und Genres erhalten die besten Bewertungen?
- Welche Regisseure und Drehbuchautoren sind am meisten vertreten?
- Welche Genres sind am häufigsten vertreten?
- Wie hängt die Länge eines Films mit seiner Bewertung zusammen?
- Welche Trends zeigen sich bei der Anzahl der Filme und Bewertungen über die Jahre hinweg?
- Gibt es auffällige Korrelationen zwischen numerischen Variablen und der Zielvariable?

In meiner Analyse fiel der Einfluss der Bollywood-Industrie besonders stark auf, da viele Filme aus diesem Bereich im Datensatz enthalten waren. Allgemein zeigt sich die Tendenz, dass längere Filme im Durchschnitt höhere Bewertungen (Ratings) erzielen. Auch bestimmte Genres stachen in ihrer Beliebtheit und Bewertung hervor.

Interessant war zudem die Beobachtung, dass die Anzahl der abgegebenen Stimmen (numVotes) besonders kurz vor und Anfang der 2000er Jahre sehr hoch war, während diese ab 2015 etwas abnahm. 
![votes_pro_jahr](https://github.com/user-attachments/assets/b35844d3-1658-4cf0-8b4f-fe92ac8a6533)

Gleichzeitig konnte ich feststellen, dass im Laufe der Jahre immer mehr Filme veröffentlicht wurden, wobei 2018 das Jahr mit den meisten Veröffentlichungen darstellt.
Die durchschnittliche Filmlänge lag bei unter 100 Minuten, wobei die meisten Filme in die Kategorie von etwa 90 Minuten fielen (Filme die zwischen 90-120 Minuten lang sind). Dennoch gibt es einen auffälligen Trend zu längeren Filmen: Es existieren mehr Filme mit einer Laufzeit von über 120 Minuten als solche, die kürzer als 89 Minuten sind.

![veroeffentlichte_filme_pro_jahr](https://github.com/user-attachments/assets/5fe60a0f-f5a4-4ad6-9b76-d20ea6e2e70c)

Es würde den Rahmen der Dokumentation sprengen wenn ich alle Grafiken erklären würde, ausserdem sind viele auch selbsterklärend anhand des Titels. Genauere Beschreibungen befinden sich in den Doc Strings im Quellcode. Doch Einige sind, besonders wenn man den Fokus auf die Zielvariable 'average_rating' legt, interessant geanuer zu betrachten.

Beispielsweise kann man anahnd der durschnittlichen Berwertungen pro Jahr erkennen, dass ältere Filme tendenziell bessere Bewertungen haben:


print("In diesen Jahren haben Nutzer im durschnitt folgende Bewertungen verteilt",movies_cleaned.groupby('startYear')['averageRating'].mean().sort_values(ascending=False))

output:
![Screenshot (759)](https://github.com/user-attachments/assets/44ef00c7-8ebb-4ab6-8d17-b053e712d184)



Korrelationsmatrix (zielvariable)

![korrelationsmatrix_zielvariable](https://github.com/user-attachments/assets/1b6cd7ce-5efe-459c-9feb-9ed29bc5389a)

Dies ist die Korrelationsmatrix, die die Korrelationen der nummerischen Spalten mit der Zielvariable aufzeigt. Man erkennt, dass die Variablen 'averageRating' und 'director_popularity' logischerweise an erster Stelle stehen, da sie inhaltich die selben Muster wie averageRating aufweisen. Wie erwähnt ist auch die Variable 'rating_category' von 'averageRating' abgeleitet, hat aber eine negative Korrelation. Dies kann man folgendermassen erklären: die rating_category hat die Klassifikation 1,2 und 3, wobei die imdB Scores zwischen 1-10 liegen. Beim score gilt: je höher desto bessser, aber bei der Klassifikation ist es andersrum. 

Weitere Erkenntnise zeigen, dass die Hälfte positiv und die andere Hälfte negativ mit averageRating korreliert. Die Variablen bzw. Features 'runtimeMinutes', 'Drama','runtimeCategory','Documentary' und 'numVotes' haben hier bei recht hohe positive Korrelationen, was ja beduetet, dass sie stark miteinander zusammenhängen. Somit kann man ungefähr festhalten, dass die Genres 'Drame und Documentary' ein Indikator für gut bewertete Filme sind und auch hohe 'numVotes' oder längere Filme auf ein eher hohes Rating deuten kann.
Im Gegensatz dazu zeigen Genres wie 'Action', 'Sci-Fi' oder 'Horror' negative Korrelationen, was darauf hindeutet, dass diese im Durchschnitt vergleichsweise schlechter bewertet sind. Es sollte jedoch berücksichtigt werden, dass diese Genres möglicherweise weniger häufig vertreten sind als beispielsweise 'Documentary', was überraschenderweise zu einer negativen Korrelation führen könnte."

![korrelationsmatrix_gesamt](https://github.com/user-attachments/assets/5c78ecb5-34b6-4e74-9ab6-56344c8abe33)

Das sind die Korrelationen der nummerischen Werte insgesamt. 
Hier wurden die Genre nicht mit einbezogen, weil dies die Grafik überladen würde. Insgesamt sieht man dass positive Relationen logischerweise zwischen den 'ursprünglichen' Spalten und den abgeleiteten kategorisierten Spalten gibt.
Aber auch z.B zwischen 'startYear' dem Erscheinungsjahr und 'runtimeMinutes' gibt es eine positive Korrelartion, welches Abhängigkeiten wie 'Neuere Filme sind im schnitt länger/kürzer als ältere' erklären könnte. Ebenso herrscht eine recht hohe positive Korrelation zwischen 'startYear' und 'director_encoded', welches Trend zeigen kann, wie aktiv bestimmte Director in bestimmten Jahren waren.

Folgende Visualisierung zeigt die durschnittliche Verteilung der Bewertungen, wo von man ableiten kann, dass die meisten Filme ein rating von ca. 6,5 haben:
![verteilung_der_bewertung](https://github.com/user-attachments/assets/6372f9ba-d4fc-41f2-9de1-6df5c469dc0d)


## Modellbildung
Im nächsten Schritt wurde der bereinigte und kategorisierte Datensatz weiter verarbeitet, um ein Modell zu erstellen, das Vorhersagen trifft. Dafür wurde der XGBoost Regressor verwendet, der aufgrund seiner Performance und Flexibilität für diese Aufgabe gut geeignet ist. Zuvor habe ich mit den Modellen 'linear Regressor' und 'random Forest' gearbeitet (siehe RandomForestRegressor Klasse) Diese haben jedoch schlechtere Werte geliefert. Aus diesem Grund kam ich nach längerer Recherche auf das Xgbooster Modell, welches komplexere Datensätze besser verarbeiten soll.
In der RandomForestRegression Klasse erkennt man den Ansatz den ich vor der Verwendung des Xgboost Modells hatte. Das Modell liefert einen R²-Score von 0.4020365251848522.

1. Vorbereitung des Datensatzes:
   - Spaltenauswahl: Nicht relevante oder nicht nummerische Spalten wie tconst, directors, writers,            directorNames, writerNames, genres, Outlier, decade und runtime_category wurden entfernt. Die Spalten 'Outlier','decade','runtime_category', die zuvor 
     extra erstellt wurden, um die Rohinformationen zu kategorisieren, wurden nun doch entfernt, da:

      Outlier: nur zur Makierung von Ausreißern diente und im Modell eventuell zu viel Input bezüglich          averageRating gibt, denn der R²-Score ist mit Outlier noch höher (ca bei 51)
      decade: die Informationen aus startYear sind ausreichend und das Einbeziehen macht den R²-Score schlechter 
      runtime_category: diese Spalte erwies sich als weniger wichtig. Die Skalierung der runtimeMinutes liefert bereits ausreichende Informationen, weshalb diese zusätzliche Kategorisierung überflüssig war.

   - Skalierung der numerischen Werte: Mithilfe der Min-Max-Skalierung wurden numerische Features                  (movies_with_this_genre_voted, director_popularity_by_votes, numVotes) in einen Bereich von 0 bis 1            transformiert. Diese Skalierung hilft, die Werte gleichmäßiger zu gewichten und Verzerrungen durch            große Zahlen zu vermeiden. Zusätzlich wurden die skalierten Versionen der Features beibehalten, um sie        als ergänzende Informationen in das Modell einfließen zu lassen. Die ursprünglichen Spalten liefern           Rohinformationen, die ohne sie nicht in die Berechnung einfließen würden. Das verwenden beider Features       hilft dem Modell scheinbar, da der Wert höher ist, wenn beide einbezogen werden.

   - Feature-Interaktionen: Um potenzielle Zusammenhänge zwischen bestimmten Variablen besser zu erfassen,          wurden neue Features erstellt. Ein Beispiel ist die Interaktion zwischen runtimeMinutes und                   scaled_numVotes, die als runtime_and_votes eingeführt wurde. Diese neue Variable hebt Filme hervor, die       sowohl eine lange Laufzeit als auch eine hohe Anzahl von Bewertungen aufweisen. Auch diese extra               Variable hilft dem Modell, da der R²-Score durch sie höher wurde.

2. Train-Test-Split:
Der Datensatz wurde in Trainingsdaten (80%) und Testdaten (20%) aufgeteilt, um das Modell zu trainieren und dessen Leistung objektiv zu bewerten. Diese Gewichtung ist typisch bei maschienneles Lernen.

3. Modellbildung mit XGBoost:
Der XGBoost Regressor wurde verwendet, um die Zielvariable (averageRating) vorherzusagen. Hyperparameter wie max_depth, learning_rate und n_estimators wurden so gewählt, dass eine gute Balance zwischen Modellkomplexität und Vermeidung von Überanpassung erreicht wurde.
Nach dem Training des Modells wurden die Vorhersagen für die Testdaten berechnet.

## Modellevaluation
Root Mean Squared Error (RMSE): Dieser Wert wurde berechnet, um die Genauigkeit des Modells zu messen. Je näher der RMSE an 0 liegt, desto besser ist das Modell.

R²-Score: Zeigt wie gut das Modell insgesamt die Durchschnittsbewertung vorhersagen kann. Ein Wert nahe 1 deutet auf eine gute Vorhersage.

Ein Scatter-Plot zeigt den Vergleich zwischen den tatsächlichen und vorhergesagten Bewertungen. Eine ideale Vorhersage ist durch die rote diagonale Linie repräsentiert. Das Diagramm verdeutlicht, wie nah die Vorhersagen des Modells an den tatsächlichen Werten liegen.

![Evaluation](https://github.com/user-attachments/assets/36a33be1-221c-4ae8-bb71-e59a1c862dbd)

Auf der Konsole lassen sich die ersten 10 Beispiele des Testdatensatz mit dem vom Modell vorhergesagten Rating und dem tatsächlichem Rating drucken lassen:

![Screenshot (761)](https://github.com/user-attachments/assets/7812be17-a743-4d63-8233-ad9ab7b2f966)

Grundsätzlich finde ich die Vorhersage gar nicht schlecht, besonders wenn man bedenkt, dass das Dataset nicht viele numerische Merkmale oder zusätzliche Informationen liefert. Es war jedoch ziemlich herausfordernd, mit den verfügbaren Attributen eine solide Vorhersage zu entwickeln. Wie bereits erwähnt, wären Informationen zu Budget und Umsatz sehr hilfreich gewesen und hätten das Modell sicherlich dabei unterstützt, genauere Vorhersagen zu treffen.

Feature-Bedeutung:
Die Ergebnisse zeigen, welche Variablen den größten Einfluss auf die Modellleistung haben. Die Feature-Bedeutung wurde visuell als Balkendiagramm dargestellt:
Leider ist die Visualisierung etwas ind die Länge gezogen, aber sonst würde man die Beschriftungen nicht ganz erkennen.

![myplot](https://github.com/user-attachments/assets/4d18020d-4f1a-4cc7-827d-da0c20c21629)


Die Grafik zeigt die Merkmale des Datensatzes sowie ihre Bedeutung im Hinblick auf das Modell. Die Bedeutung eines Merkmals gibt an, wie stark es zur Vorhersage beiträgt. Ein höherer Wert bedeutet, dass das Merkmal eine größere Auswirkung auf das Modell hat. Dies bedeutet dass die Genre 'Horror', 'Documentary' und 'Drama' das Modell am meisten beeinflusst und die Features mit eher seltenen Genre wie 'Film-Noir' weniger. Von den weiteren Attributen sind 'scaled_runtime_and_votes' und 'runtimeMinutes', die Features mit höherere Bedeutung.

Erkenntnisse und Optimierungen:
Die Einführung skalierten Features und das Entfernen redundanter Kategorien wie decade und runtime_category haben die Modellleistung verbessert.
Der XGBoost Regressor hat durch seine Fähigkeit, komplexe Zusammenhänge zu erfassen, bessere Ergebnisse erzielt als alternative Modelle. Tatsächlich habe ich auch mit dem GridSearch Verfahren gearbeitet, jedoch stieß ich auf technische Probleme, welches das Programm nicht ausführbar machte: es gab Inkompatibilität mit der installierten Version des Pakets, obwohl diese aktuell war. Nach zahlreichen Versuchen bin ich wieder zum vorherigen Ansatz mit Xgbooster ubd den Hyperparameter gekommen. 
Optimierungen sind immer möglich, aber trotz intensiver Anstrengungen konnte mein Modell-Score nicht über einen R²-Score von 0.42497892345341437 hinaus verbessert werden.
