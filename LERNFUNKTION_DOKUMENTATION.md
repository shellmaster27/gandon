# Dokumentation: Lernfunktion des IT-Support-Helfers

## Übersicht

Der IT-Support-Helfer wurde um eine **Lernfunktion** erweitert, die es ihm ermöglicht, aus früheren Support-Fällen zu lernen und bei ähnlichen Anfragen relevante Lösungen vorzuschlagen. Diese Funktion macht den Helfer mit der Zeit immer wertvoller, da er kontinuierlich aus den dokumentierten Fällen lernt.

## Wie funktioniert die Lernfunktion?

Die Lernfunktion basiert auf drei Hauptkomponenten:

1. **Falldokumentation**: Über den Befehl `/document` können Support-Mitarbeiter abgeschlossene Fälle dokumentieren.
2. **Vektordatenbank**: Die dokumentierten Fälle werden in einer lokalen Vektordatenbank (ChromaDB) gespeichert.
3. **Ähnlichkeitssuche**: Bei neuen Anfragen sucht der Helfer automatisch nach ähnlichen früheren Fällen und schlägt passende Lösungen vor.

## Schritt-für-Schritt Anleitung

### 1. Einen Fall dokumentieren

Nach Abschluss eines Support-Falls:

1. Geben Sie `/document` in das Chat-Eingabefeld ein und drücken Sie Enter.
2. Füllen Sie das erscheinende Formular mit den folgenden Informationen aus:
   - **Welcher Kunde hatte das Problem?** (z.B. "Meta10 AG")
   - **Was genau war das Problem des Kunden?** (detaillierte Beschreibung)
   - **Was war die Lösung für das Problem?** (detaillierte Beschreibung)
   - **War der Kunde während des Supports schwierig oder verärgert?** (Stimmung beschreiben)
   - **Tritt dieses Problem bei diesem Kunden häufiger auf?** (Ja/Nein)
3. Klicken Sie auf "Antworten speichern".
4. Der Fall wird automatisch in der Vektordatenbank gespeichert und steht für zukünftige Anfragen zur Verfügung.

### 2. Von der Lernfunktion profitieren

Bei jeder neuen Anfrage:

1. Stellen Sie eine Frage oder beschreiben Sie ein Problem im Chat-Eingabefeld.
2. Der Helfer sucht automatisch nach ähnlichen früheren Fällen in der Vektordatenbank.
3. Wenn ähnliche Fälle gefunden werden, fügt der Helfer diese Information seiner Antwort hinzu:
   - **Kundeninformation**: Bei welchem Kunden trat ein ähnliches Problem auf
   - **Relevanz**: Wie ähnlich ist der frühere Fall (in Prozent)
   - **Problem und Lösung**: Beschreibung des früheren Falls und der erfolgreichen Lösung

### 3. Die Fallbasis-Statistik einsehen

In der Seitenleiste rechts finden Sie:

- Die aktuelle Anzahl der gespeicherten Support-Fälle
- Einen Hinweis, ob der Helfer bereits aus früheren Fällen lernen kann
- Erinnerungen zur Nutzung der Befehle `/document` und `/docs`

## Beispiele

### Beispiel 1: Dokumentation eines Falls

1. Eingabe: `/document`
2. Formular ausfüllen:
   - Kunde: Meta10 AG
   - Problem: Excel-Datei mit Makros wird blockiert
   - Lösung: Makros in den Vertrauenseinstellungen zugelassen und Datei in vertrauenswürdigen Speicherort verschoben
   - Stimmung: Neutral
   - Wiederkehrendes Problem: Ja
3. Nach dem Speichern bestätigt der Helfer die erfolgreiche Dokumentation.

### Beispiel 2: Ähnliche Fälle finden

1. Eingabe: "Ein Benutzer bei uns kann keine Excel-Makros ausführen"
2. Der Helfer antwortet mit seiner normalen Antwort und fügt zusätzlich einen Hinweis hinzu:

```
**Ähnlicher Fall gefunden:** Bei Kunde *Meta10 AG* hatten wir ein ähnliches Problem (78% Übereinstimmung).

**Problem:** Excel-Datei mit Makros wird blockiert

**Lösung:** Makros in den Vertrauenseinstellungen zugelassen und Datei in vertrauenswürdigen Speicherort verschoben
```

## Technische Details (für Administratoren)

- Die Fallbasis wird in einem Ordner `case_memory_db` im Installationsverzeichnis des IT-Support-Helfers gespeichert.
- Es wird ChromaDB als lokale Vektordatenbank verwendet (keine Cloud-Abhängigkeit).
- Die Ähnlichkeitssuche basiert auf semantischer Ähnlichkeit, nicht nur auf Stichwortübereinstimmungen.
- Die Relevanz wird als Prozentwert angegeben (0-100%), wobei höhere Werte eine größere Ähnlichkeit bedeuten.

## Tipps für optimale Ergebnisse

1. **Detaillierte Beschreibungen**: Je detaillierter die Probleme und Lösungen beschrieben werden, desto besser kann der Helfer ähnliche Fälle finden.
2. **Konsistente Kundennamen**: Verwenden Sie immer die gleichen Kundennamen (z.B. "Meta10 AG" statt manchmal "Meta10" oder "Meta 10").
3. **Regelmäßige Dokumentation**: Je mehr Fälle dokumentiert werden, desto wertvoller wird die Lernfunktion.
4. **Spezifische Anfragen**: Bei der Suche nach ähnlichen Fällen helfen spezifische Anfragen mehr als allgemeine.

## Häufige Fragen

**F: Werden die Falldaten in die Cloud hochgeladen?**  
A: Nein, alle Daten werden lokal in einer Vektordatenbank im Installationsverzeichnis gespeichert.

**F: Kann ich Fälle löschen oder bearbeiten?**  
A: In der aktuellen Version ist das direkte Löschen oder Bearbeiten von Fällen nicht implementiert. Bei Bedarf kann ein Administrator die Datenbank zurücksetzen.

**F: Wie viele Fälle können gespeichert werden?**  
A: Die Anzahl der Fälle ist praktisch unbegrenzt, aber die Suchgeschwindigkeit kann bei sehr vielen Fällen (mehrere Tausend) langsamer werden.

**F: Werden die Fälle mit der Zeit "vergessen"?**  
A: Nein, einmal gespeicherte Fälle bleiben in der Datenbank, bis sie manuell gelöscht werden.
