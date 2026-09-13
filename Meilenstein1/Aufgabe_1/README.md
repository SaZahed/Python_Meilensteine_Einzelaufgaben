# Aufgabe 1 - Applikation: Einkaufswagen

Diese Dokumentation beschreibt die Zielsetzung der Anwendung "Einkaufswagensystem", die Hauptfunktionen, die Programmstruktur und technische Details wie Fehlerbehandlung und farbliche Gestaltung der Benutzeroberfläche. 

## Inhaltsverzeichnis
1. [Ziel der Anwendung](#ziel-der-anwendung-warenkorb)
2. [Übersicht](#übersicht)
4. [Funktionen des Systems](#funktionen-des-systems)
   - [Artikel einsehen](#artikel-einsehen)
   - [Artikel zum Warenkorb hinzufügen](#artikel-zum-warenkorb-hinzufügen)
   - [Artikel aus dem Warenkorb entfernen](#artikel-aus-dem-warenkorb-entfernen)
   - [Warenkorb anzeigen](#warenkorb-anzeigen)
   - [Warenkorb leeren](#warenkorb-leeren)
   - [Zur Kasse gehen ](#zur-kasse-gehen)
   - [Beenden](#beenden)
6. [Programmstruktur](#programmstruktur)
7. [Exceptions](#exceptions)
8. [Gestaltung der CUI](#gestaltung-der-cui)
    - [Sonderzeichen](#sonderzeichen)
    - [ANSI Escape Codes](#ansi-escape-codes)
    


## Ziel der Anwendung Warenkorb
In dieser Aufgabe geht es um die Realisierung eines Einkaufswagensystems. Das Programm ermöglicht es dem Nutzer Produkte aus dem Haushaltsproduktkatalog (Artikelliste) in seinem virtuellen Einkaufswagen bzw. Warenkorb zu legen. Nutzer können Artikel hinzufügen, entfernen, den Warenkorb anzeigen lassen oder leeren. Außerdem können Sie einen Einkaufsprozess tätigen, der die Möglichkeit bietet, einen Rabattcode zu verwenden. Das Programm wurde Objekt orientierten entwickelt, da ich mit diesem Programmierparadigma vertraut bin.

## Übersicht
Das Programm beginnt mit einem Startmenü, welches folgende Optionen anbietet:
  1.  Artikel einsehen: zeigt die Liste der verfügbaren Artikel
  2.  Artikel zum Warenkorb hinzufügen: ermöglicht das Hinzufügen von Artikeln zum Warenkorb
  3.  Artikel aus dem Warenkorb entfernen: entfernt Artikel aus dem Warenkorb, sofern sich welche im            Warenkorb befinden
  4.  Warenkorb anzeigen lassen: zeigt den Inhalt und die Gesamtsumme
  5.  Warenkorb entleeren leeren: leert den gesamten Inhalt des Warenkorbs
  6.  zur Kasse gehen: führt den Einkauf durch und bietet die Möglichkeit einen Rabattcode anzuwenden, um       50% Rabatt zu erhalten
  7.  Beenden: das Programm kann komplett beendet werden


Folgendes Aktivitätsdiagramm veranschaulicht den Ablauf des Programms:
![Aktivitätsdiagramm Final](https://github.com/user-attachments/assets/014e9d0c-0d7d-44d5-bc7f-723e2ac23fab)


Hinweis: Im Aktivitätsdiagramm wurde lediglich die Exception berücksichtigt, die auftritt, wenn der Benutzer keine gültige Option zwischen 1 und 7 wählt. In diesem Fall wird der Benutzer automatisch zurück zum Hauptmenü geführt.

## Funktionen des Systems
In dieser Dokumentation beziehe ich mich auf die einzelnen Optionen und deren Ablauf. Im Quellcode sind jedoch über den Methoden in der ShoppingVerwaltungs-Klasse ausführliche Docstrings enthalten. Diese beschreiben den Code sowie den Ablauf der jeweiligen Methode im Detail, einschließlich der Parameter und Funktionsweise.
## Artikel einsehen
Beim einsehen der Artikel sieht man die Artikelliste mit den jeweiligen Details Beschreibung, Preis, ArtikelId und Bestand.
Die Artikelliste ist festgelegt und besteht aus 6 definierten Artikeln. 

## Artikel zum Warenkorb hinzufügen
Wenn man einen Artikel zum Warenkorb hinzufügen möchte, wird als erstes die Artikelliste gedruckt, da man anschließend das Produkt über die ArtikelId hinzufügen muss. Es wird als erstes nach der ArtikelId gefragt und dann nach der Menge, sprich wie viel Stück man in seinem Warenkorb hinzufügen möchte.

## Artikel aus dem Warenkorb entfernen
Der Nutzer kann Artikel als Teilmenge oder komplett aus dem Warenkorb entfernen, dafür muss er die Beschreibung des Produkts eingeben. Die Methode artikel_entfernen() ruft die Methode finde_index() auf, um den Index des Artikels zu ermitteln und diesen aus dem Warenkorb zu entfernen. Somit wird im "Hintergrund" über dem Namen der Index ermittelt und dann an der jeweiligen Stelle der Liste entfernt.

## Warenkorb anzeigen
Mit dieser Option wird der aktuelle Warenkorb und die Gesamtsumme auf der Konsole angezeigt. Die Gesamtkosten werden in der extrahierten Methode gesamtkosten_berechnen() errechnet und wird 2x im Code aufgerufen: wenn man den Warenkorb anzeigen möchte und beim Bezahlvorgang.

## Warenkorb leeren
Wenn der Nutzer den kompletten Warenkorb leeren will kann er die Option 5 wählen oder bei Option 3 die gesamte Menge die sich im Warenkorb befindet auswählen.  

## Zur Kasse gehen
Wenn man zur Kasse geht, werden die Artikel, die sich im Warenkorb befinden gekauft und ein Beleg wird ausgedruckt. Anschließend wird das Programm nicht wie in Option 7 beendet, sondern läuft weiter, sodass der nächste Kunde direkt mit den verbleibenden Beständen einkaufen gehen kann. Der Nutzer hat die Möglichkeit, einen Rabattcode einzugeben. Bei Eingabe des Codes „xMAS50“ wird der Gesamtpreis um 50 % reduziert. Falls kein Rabattcode eingegeben wird, wird der Preis ohne Rabatt berechnet. Nach der Anwendung des Rabattes wird der Endbetrag entsprechend angepasst.
Beim anwenden des Rabattes wird ein zusätzlicher Print gedruckt "Endbetrag nach dem Abzug durch den Rabatt:". Dieser erscheint beim Kauf ohne Rabatt nicht.
Wenn der Nutzer versucht, mit einem leeren Warenkorb zur Kasse zu gehen, wird er darauf hingewiesen, dass dieser Vorgang nicht möglich ist. Zusätzlich erhält er eine Nachricht, die ihn darauf aufmerksam macht, dass er sich gerne weiterhin im Shop umsehen kann, um Produkte zu finden. Dabei wird auch ein Hinweis zum Rabattcode angezeigt, falls er diesen später verwenden möchte. Außerdem erscheint ein Hinweis, wenn man seinen Warenkorb anzeigen lässt und er leer ist.
Die Option, zur Kasse zu gehen, war nicht Teil der Aufgabenstellung. Ich habe sie jedoch als sinnvoll empfunden und daher in das Programm integriert.

## Beenden
Falls der Nutzer die Anwendung vollständig beenden möchte, kann dies durch die Auswahl der Option 7 erfolgen. Nach der Auswahl wird eine Abschiedsnachricht angezeigt und das Programm wird "sauber" beendet, ohne dass weitere Eingaben erforderlich sind.

## Programmstruktur
Folgende Klassen sind beim entwickeln des Programms entstanden: 
- Warenkorb, die die Liste der Einträge enthält
- Artikel, welche die Attributen eines Artikels im Konstruktor hat
- ShoppingVerwaltung, welche die Methoden enthält, die das System steuern und somit die Logikklasse ist
- und die Main Klasse namens cui(Console User Interface), von der das Programm gestartet wird und die       Benutzereingaben über die Konsole verarbeitet werden (Benutzeroberfläche).

## Exceptions
Das Programm enthält Fehlerbehandlungen für Nutzereingabefehler. Besonders bei der Eingabe von Mengen und ArtikelIds wird durch Bedingungen sichergestellt, dass nur gültige Eingaben akzeptiert werden:
   
   - Ist die gewünschte Menge größer als der verfügbare Bestand oder die Menge im Warenkorb?
   - Ist die Menge negativ oder 0?

Beim Eintretten diese Fälle kriegt der Nutzer eine rote Nachricht auf die Konsole gedruckt, dass die Eingabe ungültig ist. Schließlich wird man wieder zum Startmenü weitergeleitet. 
Das Startmenü ist mit einem try except block umfasst, damit unerwartete Fehler bei Nutzereingaben verhindert werden.
Es gibt insgesamt zwei relevante ValueError-Exceptions:

   - Eine bei der die Eingabe der ArtikelId und der Menge (beides sollten Ganzzahlen sein, bei                 einem String wird die Exception gefangen und man landet wieder beim Startmenü).
   - Eine bei der Eingabe der Menge für das Entfernen von Artikeln, die ebenfalls nur Ganzzahlen sein          dürfen.

Die Eingabe der Artikelbeschreibung (artikel_entfernen()) erfolgt als String. Da Zahlen als Strings eingegeben werden können, ist an dieser Stelle keine zusätzliche Fehlerbehandlung erforderlich, solange die Eingabe mit den vorhandenen Beschreibungen verglichen wird.

## Gestaltung der CUI
## Sonderzeichen
Für die Gestaltung der Benutzeroberfläche in der Konsole habe ich einfache Sonderzeichen wie Sternchen (*) und Bindestriche (-) verwendet. Diese dienen dazu, die einzelnen Abschnitte klar voneinander zu trennen und die Navigation durch das Menü zu erleichtern. 
Um zu verdeutlichen wie ich Gebrauch von den Sonderzeichen gemacht habe ist hier ist ein Bild, welches die Konsolausgabe zeigt, wenn man Artikel gekauft hat: 
![SS von Konsolausgabe Sonderzeichen](https://github.com/user-attachments/assets/c679b7c8-0f87-4ee7-848d-25c63a192dbf)


## ANSI Escape Codes
Ursprünglich wollte ich nur die Exceptiontexte rot einfärben, aber nachdem ich gelernt habe, wie man Textausgaben in der Konsole einfärben kann, habe ich ANSI Escape Codes gezielt an weiteren Stellen eingesetzt. Dadurch wollte ich die Benutzeroberfläche optisch ansprechender gestalten und gleichzeitig die Navigation sowie das Verständnis für die Ausgaben erleichtern. Die folgende Tabelle zeigt die verwendeten Farben und deren Einsatzbereiche:

| **Farbe**        | **Code**               | **Anwendung**          |
|-------------------|------------------------|-------------------------|
| **Rot**          | `\033[31m TEXT \033[0m`| Fehlermeldungen         |
| **Lila/Pink**    | `\033[35m TEXT \033[0m`| Überschrift *Unser Angebot* |
| **Grün**         | `\033[32m TEXT \033[0m`| Erfolgreiches Leeren des Warenkorbs, erfolgreiche Aktivierung des Rabattcodes und Kennzeichung, dass Einkaufsprozess erfolgreich war|
                                                
Hier sind paar Beispiele für die farbigen Konsolenausgaben:
Mithilfe von ANSI Escape Codes konnte ich die Fehlermeldung wie z.B. bei Eingabe einer negativen Menge, in rot auf die Konsole ausdrucken lassen. 
![Screenshot (646)](https://github.com/user-attachments/assets/1fcd4395-18f1-4aa9-8b2c-53cd4fb61f70)

Beim ausdrucken der Artikelliste ist die Überschrift "Unser Angebot" lila/pink.
![Screenshot (643)](https://github.com/user-attachments/assets/8b4b2645-6622-45a5-ac03-e6e00dd93c05)

Nach jedem Einkauf wird eine Zeile mit Sternchen gedrukt, diese ist in grün gefärbt und kennzeichnet, dass man quasi einen Kunden abgearbeitet hat.

![Screenshot (644)](https://github.com/user-attachments/assets/1ec3b1a0-86af-4820-baa4-f00b6c486fb2)

Ebenso wird nach einem erfolgreichen leeren des Warenkorbs ein print in grün gedruckt.
![Screenshot (645)](https://github.com/user-attachments/assets/b48c8eb4-bfd2-4d49-b046-2942eb6b5a0e)


