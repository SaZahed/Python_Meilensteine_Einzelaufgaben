import pandas as pd

# Dateien einlesen
title_basics = pd.read_csv("title.basics.tsv.gz", compression='gzip', sep="\t", low_memory=False)
title_ratings = pd.read_csv("title.ratings.tsv.gz", compression='gzip',sep="\t", low_memory=False)
title_crew = pd.read_csv("title.crew.tsv.gz", compression='gzip',sep="\t", low_memory=False)
name_basics = pd.read_csv("name.basics.tsv.gz", compression='gzip',sep="\t", low_memory=False)

print(title_basics.head())
print(title_ratings.head())
print(title_crew.head())

# Tabellen miteinander verknüpfen bzw. mergen
merged_data = pd.merge(title_basics, title_ratings, on="tconst", how="inner")
merged_data = pd.merge(merged_data, title_crew, on="tconst", how="inner")

# Ergebnisse prüfen
print("Die Anzahl an Zeilen und Spalten beim Dataset mit Basics, Rating und Crew Infos: \n",merged_data.shape)
print("Ersten Zeilen des kombinierten DataFrames reduced_merged_data:\n",merged_data.head())

# wir betrachten nur Filme, deshalb brauchen wir den Rest nicht
movies_only = merged_data[merged_data['titleType'] == 'movie']

# Einträge, die übrig bleiben nach dem Filtern von nur Filmen
print(f"Anzahl der Filme im Datensatz: {len(movies_only)}")

# DataFrame reduzieren: alles  über 100 000 ist kann mein Laptop nicht aushalten +  der datensatz wird kleiner bei höheren zahlen
reduced_merged_data = movies_only.sample(n=100000, random_state=42) # random damit wir einen mix aus den datensatz haben (nicht nur obersten 100 K)

name_dict = pd.Series(name_basics['primaryName'].values, index=name_basics['nconst']).to_dict()

"""
                Konvertiert eine durch Kommas getrennte Liste von IDs in die entsprechenden Namen.

- Diese Funktion nimmt eine durch Kommas getrennte Zeichenkette von IDs der Director und Writer 
  und sucht für jede ID den entsprechenden Namen aus einem Dictionary (`name_dict`).
- Falls eine ID nicht im Dictionary gefunden wird, wird 'Unknown' zurückgegeben.

- Args:
  id_string (str): die durch Kommas getrennte Zeichenkette von IDs.
  name_dict (dict): Ein Dictionary fuer die Zuordnung der IDS und Namen

- Returns:
  str: Eine durch Kommas getrennte Liste von Namen, die den IDs entsprechen. 
       Unbekannte IDs werden durch 'Unknown' ersetzt.

"""
def map_ids_to_names(id_string, name_dict):
    ids = id_string.split(",")  # Falls es mehrere Regisseure/Drehbuchautoren gibt
    names = [name_dict.get(id.strip(), 'Unknown') for id in ids] #Nullwerte werden mit Unknown ersetzt
    return ", ".join(names)

# Director-Namen hinzufügen
reduced_merged_data['directorNames'] = reduced_merged_data['directors'].apply(lambda x: map_ids_to_names(x, name_dict))

# Writer-Namen hinzufügen
reduced_merged_data['writerNames'] = reduced_merged_data['writers'].apply(lambda x: map_ids_to_names(x, name_dict))

# Ergebnisse prüfen
print("Die ersten 5 Zeilen des reduzierten Datasets mit Regisseur- und Drehbuchautoren-Namen:\n", reduced_merged_data[['tconst', 'primaryTitle', 'directorNames', 'writerNames']].head())

'''
Die CSV Datei ist mit gepusht, deshalb ist die Zeile zum reinschreiben in die CSV einkommentiert
'''
#reduced_merged_data.to_csv("reduced_and_merged_data_with_names.csv", index=False)