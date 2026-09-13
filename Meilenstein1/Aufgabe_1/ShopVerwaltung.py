import datetime

from Artikel import Artikel
from Warenkorb import Warenkorb

class ShopVerwaltung:
    """
    Initialisiert die Shop-Verwaltung mit einer Artikelliste und einem leeren Warenkorb.

    Hinweise:
    - Die Artikelliste enthält 6 definierte Artikel mit den Attributen Beschreibung, Preis, Artikel-ID und Bestand.
    - Jeder Kunde startet mit einem leeren Warenkorb.
    """
    def __init__(self):
            self.artikelliste = [
                Artikel("Tasse", 6, 100, 20),
                Artikel("Kissen", 10, 101, 30),
                Artikel("Gardinen", 30, 102, 100),
                Artikel("Besteckset", 20, 103, 80),
                Artikel("Teekanne", 15, 104, 88),
                Artikel("Kuechenmaschiene", 90, 105, 200),
            ]
            self.warenkorb = Warenkorb()

    """
    Zeigt die aktuelle Artikelliste an, einschließlich Beschreibung, ArtikelId Preis und Bestand.

    Hinweise:
    - Die Liste zeigt immer den aktuellen Bestand, da Sie bei Ein/Auslagerungen aktuallisiert wird
    - Die Ausgabe erfolgt auf der Konsole.
    """
    def artikel_anzeigen(self):
        print("\033[35m~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Unser angebot ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~:\033[0m")
        for artikel in self.artikelliste:
                print(
                    f"Beschreibung: {artikel.beschreibung} \n ArtikelID: {artikel.artikelId} \n Preis: {artikel.preis}€ \n Bestand: {artikel.bestand} \n")

    """
    Fuegt eine bestimmte Menge eines Artikels in den Warenkorb hinzu.

    Parameter:
        - Nutzer muss die ArtikelId (int) des Artikels eingeben, der hinzugefuegt werden soll.
        - Nutzer die Menge (int) des Artikels, die hinzugefuegt werden soll eingeben.
    
    Ablauf:
        1. Als erstes wird die Methode `finde_artikel` fuer die Existenzueberpruefung aufgerufen
        2. Validierung der Nutzereingabe:
           - ArtikelId muss gueltig sein
           - Menge darf nicht groeßer als der verfuegbare Bestand sein.
           - Menge darf nicht negativ oder null sein.
        3. Wenn der Artikel bereits im Warenkorb ist:
           - Wird kein neuer Eintrag geschrieben, sondern die Menge und die Kosten aktualisiert
        4. Wenn der Artikel nicht im Warenkorb ist:
           - Wird neuer Eintrag geschrieben 
    
    Hinweise:
        - Bestandsaenderungen werden sofort vorgenommen.
    """
    def artikel_hinzufuegen(self, artikelId, menge):
       artikel = self.finde_artikel(artikelId)
       if artikel is None:
           print(f"\033[31mDer Artikel mit der ID {artikelId} existiert nicht!\033[0m")
           return
       elif menge > artikel.bestand:
           print(f"\033[31mHoppla: Es sind nur {artikel.bestand} Stueck verfuegbar!! Wir werden bald neue Ware für Sie einlagern.\033[0m")
           return
       elif menge <=0:
           print(f"\033[31m Die Menge darf nicht negativ oder null sein!\033[0m")
           return
       #wenn man selbes produkt noch mal hinzufuegt
       for eintrag in self.warenkorb.eintraege:
           if eintrag['artikelId'] == artikel.artikelId:
               eintrag['menge'] = eintrag['menge'] + menge
               eintrag['kosten'] = eintrag['menge'] * artikel.preis
               artikel.bestand -= menge
               print(
                   f"{menge}x {artikel.beschreibung} wurde hinzugefuegt. Insgesamt nun {eintrag['menge']}x im Warenkorb. Ihre Kosten fuer diesen Eintrag: { eintrag['kosten']}€.")
               return

      #wenn der artikel noch nicht im warenkorb ist
       kosten = artikel.preis * menge
       self.warenkorb.eintraege.append({
           "beschreibung": artikel.beschreibung,
           "artikelId": artikel.artikelId,
           "menge": menge,
           "kosten": kosten,
       })
       artikel.bestand -= menge
       print(f"{menge}x {artikel.beschreibung} wurde in den Warenkorb hinzugefuegt. Ihre Kosten für diesen Eintrag: {kosten}€.")

    """
    Sucht einen Artikel in der Artikelliste anhand der Artikel-ID. Diese Methode benoetigt man beim Verwalten des 
    Warenkorbs und bei Bestandsaenderungen, wenn man den Warenkorb leert.

    Parameter:
        - die artikelId (int) vom gesuchten Artikel
    
    Rückgabewert:
        - Gibt den gefundenen Artikel als Artikel Objekt zurueck.
        - Falls kein Artikel gefunden wurde wird None zurueckgegeben
    """
    def finde_artikel(self, artikelId):
        for artikel in self.artikelliste:
            if artikel.artikelId == artikelId:
                return artikel
        return None

    """
    Sucht den Index eines Artikels im Warenkorb anhand der Artikelbeschreibung.
    Parameter:
        - Beschreibung (str) des Artikels, der gesucht wird.
    
    Rueckgabewert:
        - int: Der Index des Artikels im Warenkorb, falls gefunden.
        - None: Wenn kein Artikel mit der angegebenen Beschreibung gefunden wird.
    
    Hinweise:
        - Suche ignoriert Groß- und Kleinschreibung (lower Case)
        - Durch enumerate iteriert man ueber die Liste, sodass 2 Werte zureckgegeben werden
    """
    def finde_index(self, beschreibung):
        for index, artikel in enumerate(self.warenkorb.eintraege):
            if artikel['beschreibung'].lower() == beschreibung.lower():
                return index
        return None

    """
    Entfernt eine bestimmte Menge eines Artikels aus dem Warenkorb.
    Ablauf:
    1. Ruft `finde_index()` auf, um den Index des Artikels im Warenkorb anhand der Beschreibung zu finden.
    2. Validiert die gewuenschte Menge:
       - ueberprueft, ob die Menge kleiner der vorhandenen Anzahl im Warenkorb ist.
       - Menge muss positiv sein
    3. Aktualisiert den Warenkorb:
       - Falls die Menge gleich der vorhandenen Menge ist: entfernt den gesamten Artikel-Eintrag.
       - Andernfalls: Anpassung des Bestands und Kosten
    4. Bestandsverwaltung:
       - Sucht den Artikel in der Artikelliste anhand der `artikelId` (zurueckgegeben von `finde_artikel()`).
       - Bucht die entfernte Menge wieder zum Bestand hinzu, weil man Sie entfernt hat.

    Parameter:
    - `beschreibung`(str): Die Beschreibung des Artikels, der entfernt werden soll.
    - `menge`(int): Die Menge des Artikels, die entfernt werden soll.

    Hinweise:
    - Gibt Fehlermeldungen aus, falls die Beschreibung nicht gefunden wird oder die Menge ungueltig ist.
    """
    def artikel_entfernen(self, beschreibung, menge):
        index = self.finde_index(beschreibung)
        if index is not None:
            eintrag = self.warenkorb.eintraege[index] #eintrag speichert wo im warenkorb unser artikel ist

            if menge > eintrag["menge"]:
                print(f"\033[31mSie koennen nicht mehr Artikel entfernen, als im Warenkorb vorhanden sind(Es sind nur {eintrag['menge']} Stueck im Warenkorb drinnen)!!!\033[0m")
                return
            elif menge <=0:
                print(f"\033[31mDie Menge darf nicht negative sein oder 0 sein!!\033[0m")
                return

            artikel = self.finde_artikel(eintrag["artikelId"])
            if artikel:
                artikel.bestand += menge
                print(f"{menge}x {beschreibung} zurückgebucht. Neuer Bestand: {artikel.bestand}")

            if menge == eintrag["menge"]:
                self.warenkorb.eintraege.pop(index) #Komplett entfernen
            else:
                eintrag["menge"] = eintrag["menge"] - menge  #nur gewuenschte Menge entfernen
                eintrag["kosten"] = eintrag["menge"] * artikel.preis
                print(
                    f"{menge}x {beschreibung} aus dem Warenkorb entfernt. Nun haben Sie nur noch: {eintrag['menge']} Stueck im Warenkorb drin.")
        else:
            print(f"\033[31mDer Artikel '{beschreibung}' wurde nicht gefunden!\033[0m")

    """ 
    Eigene Methode, die die Gesamtkosten berechnet. 
    Die Methode wurde aus den Methoden warenkorb_anzeigen()
    und bezahlen() extrahiert, da der selbe Code doppelt vorkam.
    
    Ablauf:
        1. itteration ueber Eintraege im Warenkorb
        2. Drucken des Warenkorbs
        3. Summierung der Kosten pro Eintrag, sodass man Gesamtkosten erhaelt  
    Rueckgabewert:
        - es wird die Variable gesamtkosten (int) mit dem Einkaufswert zurueckgegeben    
    
    """
    def gesamtkosten_berechnen(self):
        gesamtkosten = 0
        for eintrag in self.warenkorb.eintraege:
            print(
                f"Artikel: {eintrag['beschreibung']} \n"
                f"ArtikelId: {eintrag['artikelId']} \n"
                f"Anzahl: {eintrag['menge']} \n"
                f"Kosten fuer den Eintrag: {eintrag['kosten']}€ \n"
            )
            gesamtkosten += eintrag['kosten']

        return gesamtkosten

    """
    Zeigt die aktuellen Inhalte des Warenkorbs an, einschließlich Artikelbeschreibung, Artikel-ID, Menge und Kosten pro Eintrag.

    Hinweise:
        - Zeigt die Gesamtkosten aller Eintraege im Warenkorb.
        - Gibt eine Meldung aus, wenn der Warenkorb leer ist.
    """
    def warenkorb_anzeigen(self):
        if not self.warenkorb.eintraege:
            print("Ihr Warenkorb ist leer. \n Schauen Sie sich gerne unseren Produktkatalog an, Sie werden sicherlich etwas passendes finden.. \n Mit unserem Cod 'xMAS50' erhalten Sie sogar 50% Rabatt auf Ihren Gesamteinkauf")
            return
        gesamtkosten = self.gesamtkosten_berechnen()
        print(f"----------------------------------- < Ihre Gesamtkosten: {gesamtkosten}€ > -------------------------------------------------------------------------")

    """
    Leert den Warenkorb und bucht die Artikelmengen zurueck in den Bestand.

    Ablauf:
        1. Durchlaeuft alle Eintraege im Warenkorb.
        2. Findet die entsprechenden Artikel ueber die Id in der Artikelliste (`finde_artikel`) und bucht die Mengen zurueck.
        3. Entfernt alle Eintraege aus dem Warenkorb.

    Hinweise:
        - Gibt eine Bestaetigungsmeldung aus, nachdem der Warenkorb erfolgreich geleert wurde.
        - Zeigt fuer jeden Artikel an, wie viel in den Bestand zurueckgebucht wurde.
    """

    def warenkorb_leeren(self):
        print("Ihr Warenkorb wird geleert...")
        for eintrag in self.warenkorb.eintraege:
            artikel = self.finde_artikel(eintrag["artikelId"])
            if artikel:
                artikel.bestand = artikel.bestand + eintrag['menge']
                print(f"{artikel.beschreibung} wurde {eintrag['menge']} X zum Bestand zurueckgetan")

        self.warenkorb.eintraege.clear()
        print("\033[32m............................ Ihr Warenkkorb wurde erfolgreich entlerrt ............................................................\033[0m")

    """
    Schließt den Einkaufsprozess ab, berechnet die Gesamtkosten und durckt einen Kassenbon aus.

    Parameter:
        - rabatt (str): Ein Rabattcode, der optional auf den Gesamtbetrag angewendet werden kann ("xMAS50" für 50 %).

    Ablauf:
        1. Berechnet die Gesamtkosten des Warenkorbs
        2. Ueberprueft den Rabattcode:
           - Wenn er richtig eingegeben wurde, dann wird die Gesamtsumme halbiert (50%)
           - Wenn eine andere Eingabe getaetigt wurde, dann zahlt man den vollen Betrag
        3. Gibt einen Kassenbon aus, einschließlich:
           - die Gesamtkosten und wenn der Rabatt angwendet wurde den Endbetrag mit Abzug an.
           - Datum und Uhrzeit des Kaufs.
           - Artikel, Mengen und Kosten im Warenkorb.
        4. Leert den Warenkorb nach Abschluss des Kaufs.

    Hinweise:
        - Wenn man bei der Abfrage nach einem Rabattcode etwas anderes als xMAS50 eingibt, geht man zum bezhalen ohne 50%
        - Startet nach dem Kauf mit einem leeren Warenkorb für den nächsten Kunden.
    """

    def bezahlen(self,rabatt):
        aktivierung = False # wenn man keinen Rabattcode verwendet soll der pint mit "Endbetrag nach Abzug.." nicht erscheinen
        gesamtkosten = self.gesamtkosten_berechnen()
        if rabatt == "xMAS50":
            gesamtkosten = gesamtkosten / 2 #50% Rabatt
            aktivierung = True
            print("\033[32mGlueckwunsch! Der Rabattcode wurde akzeptiert. Sie muessen nur die Haelfte zahlen.\033[0m")

        print("Vielen Dank für Ihren Einkauf :) Ihr Kassenbon:")
        self.warenkorb_anzeigen()
        now = datetime.datetime.now()
        if aktivierung:
            print(f"----------------------------------- < Endbetrag nach dem Abzug durch den Rabatt: {gesamtkosten:.2f}€ > ------------------------------------------")

        print("------------------------------------< Datum und Uhrzeit:", now.strftime("%d.%m.%Y %H:%M:%S"), " > -----------------------------------------------------------")
        self.warenkorb.eintraege.clear()
        print("\033[32m***********************************************************************************************************************************************************************\033[0m")
