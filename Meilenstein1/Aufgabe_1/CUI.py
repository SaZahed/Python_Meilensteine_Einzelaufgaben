from ShopVerwaltung import ShopVerwaltung

def run():
    shop = ShopVerwaltung()  # Instanz wie damals beim eshop erstellt, damit man Methodenaufrufe machen kann

    while True:  # Schleife beginnt hier damit ausfuehrung nacheinander erfolgt
        print("----------------------------- Willkommen in unserem Shop für Haushaltsprodukte ------------------------------------------------------ \n Bitte wählen Sie eine Option aus:")
        print("--------------------------------------------------------------------------------------------------------------------------------------")
        print("1 - Artikel ansehen")
        print("2 - Artikel zum Warenkorb hinzufügen")
        print("3 - Artikel vom Warenkorb entfernen")
        print("4 - Warenkorb anzeigen")
        print("5 - Warenkorb leeren")
        print("6 - Zur Kasse gehen")
        print("7 - Beenden")
        print("--------------------------------------------------------------------------------------------------------------------------------------")


        eingabe = input()
        try:
            match eingabe:
                case "1":
                    shop.artikel_anzeigen()
                case "2":
                    shop.artikel_anzeigen()  #braucht man für ID, die man eingibt
                    try:
                        artikelId = int(input("Bitte waehlen Sie eine ArtikelId aus, um ein Produkt in Ihrem Warenkorb hinzuzufuegen \n"))
                        menge = int(input("Bitte waehlen Sie eine Menge \n"))
                        shop.artikel_hinzufuegen(artikelId, menge)
                    except ValueError:
                        print("\033[31mUngueltige Eingabe! Bitte geben Sie eine gueltige Artikel-ID und Menge als Zahlen ein.\033[0m")
                case "3":
                    print("----------------------------  IHR AKTUELLER WARENKORB ------------------------------------------")
                    if not shop.warenkorb.eintraege:
                        print(
                            "\033[31m Ihr Warenkorb ist leer, deshalb koennen Sie keine Artikel aus Ihrem Warenkorb entfernen.\033[0m")
                    else:
                        shop.warenkorb_anzeigen()
                        # hier keine exception, weil Zahl ebenso als String gelesen wird und andere Fehlermeldung erscheint
                        beschreibung = input("Welchen Artikel moechten Sie aus Ihrem Warenkorb entfernen? Geben Sie dafür die Beschreibung des Artikels an.\n")

                        try:
                            menge = int(input("Wie viel Stueck moechten Sie entfernen? \n"))
                            shop.artikel_entfernen(beschreibung, menge)
                        except ValueError:
                            print(
                                "\033[31mUngueltige Eingabe! Bitte geben Sie Menge als Zahlen ein.\033[0m")

                case "4":
                    print("----------------------------  IHR AKTUELLER WARENKORB ------------------------------------------") #ist etwas doppelt, aber wenn ich es in Methode packe, dann kommt print auch beim kassenbon
                    shop.warenkorb_anzeigen()
                case "5":
                    if not shop.warenkorb.eintraege:
                        print("\033[31m Ihr Warenkorb ist bereits leer.\033[0m")
                    else:
                        shop.warenkorb_leeren()
                case "6":
                    if not shop.warenkorb.eintraege:
                        print("\033[31m Ihr Warenkorb ist leer, deshalb koennen Sie nicht zur Kasse gehen! \n Schauen Sie sich gerne unseren Produktkatalog an, Sie werden sicherlich etwas passendes finden.. \n Und mit unserem Code: xMAS50 erhalten Sie sogar 50% Rabatt auf Ihren Gesamteinkauf\033[0m")
                    else:
                        rabatt = input("Haben Sie einen Rabattcode den Sie anwenden möchten? Wenn Ja geben Sie ihn bitte ein und wenn nicht geben Sie bitte N ein. \n")
                        shop.bezahlen(rabatt)
                case "7":
                    print("Bye bye und bis zum naechsten Mal")
                    break
                case _:
                    print("\033[31m Ungueltige Eingabe! Bitte waehlen Sie nur Zahlen zwischen 1 und 7.\033[0m")
        except Exception as e: # falls im loop ein grundlegender Fehler auftreten sollte
            print(f"\033[31m Ein unerwarteter Fehler ist eingetroffen {e}.\033[0m")

run()