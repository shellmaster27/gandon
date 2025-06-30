# IT-Support-Helfer: Update zum Dialog-Workflow und Kontextlängenbegrenzung

## Zusammenfassung der Änderungen

Der IT-Support-Helfer wurde verbessert, um zwei Hauptprobleme zu lösen:

1. **Token-Limit-Problem:** Vorher wurde der vollständige Dokumentinhalt an OpenAI gesendet, was bei längeren Dokumenten zum Überschreiten des Token-Limits führte.

2. **Fehlende Dokumentauswahl:** Vorher wurden Suchergebnisse direkt verarbeitet, ohne dass der Nutzer die Möglichkeit hatte, gezielt ein Dokument auszuwählen.

## Technische Details der Änderungen

### 1. Neue Funktionen in `outline_utils.py`

- **`get_document_titles_and_urls(search_results)`**: Extrahiert Titel, IDs und URLs aus Suchergebnissen
- **`get_document_summary(document_id, max_chars)`**: Ruft eine gekürzte Zusammenfassung eines Dokuments ab
- **Erweiterung von `get_document_content()`**: Gibt jetzt auch Titel und URL zurück

### 2. Neuer Dialog-Workflow in `agent.py`

- **Zweistufiger Dialog:**
  - Erste Stufe: Zeigt nur Titel und URLs der gefundenen Dokumente an
  - Zweite Stufe: Nutzer wählt ein Dokument aus und kann eine spezifische Frage stellen
  
- **Dialog-Status-Management:**
  - Neue globale Variable `dialog_state` zur Verfolgung des aktuellen Dialog-Status
  - Mögliche Zustände: "initial", "document_list", "document_selected"
  
- **Neue Funktion `handle_document_selection(user_input)`:**
  - Verarbeitet die Auswahl eines Dokuments durch den Benutzer
  - Extrahiert die Dokumentnummer und ggf. eine spezifische Frage
  - Ruft den Dokumentinhalt mit Begrenzung ab

### 3. Kontextlängenbegrenzung

- **Einfache Zeichenbegrenzung:**
  - Dokumente werden auf maximal 6000 Zeichen begrenzt, bevor sie an OpenAI gesendet werden
  - Dies ist eine einfache Näherung für das Token-Limit

### 4. Anpassungen in `app.py`

- **Synchronisierung des Dialog-Status:**
  - Neuer Session-State-Parameter `dialog_state`
  - Synchronisierung zwischen Streamlit-App und Agent-Modul

## Nutzung und Tests

Der verbesserte Agent bietet jetzt einen intuitiveren Workflow:

1. **Suche starten:** Gib einen Suchbegriff ein (z.B. "Securegateway und VPN" oder "Topal")
2. **Dokumente auswählen:** Du erhältst eine Liste der gefundenen Dokumente mit Titeln und URLs
3. **Detailabfrage:** Wähle ein Dokument durch Eingabe der Nummer (z.B. "2") oder stelle eine spezifische Frage zu einem Dokument (z.B. "2: Wie funktioniert die Installation?")

## Wartung und zukünftige Anpassungen

Für zukünftige Verbesserungen könnten folgende Punkte berücksichtigt werden:

- **Bessere Token-Zählung:** Statt einfacher Zeichenbegrenzung könnte ein echter Token-Counter implementiert werden
- **Intelligentere Textauswahl:** Statt einfacher Kürzung könnten relevantere Teile des Dokuments basierend auf der Anfrage ausgewählt werden
- **Chunking-Strategie:** Lange Dokumente könnten in kleinere Teile aufgeteilt werden, um mehr relevante Informationen zu behalten

## Bekannte Einschränkungen

- Die Zeichenbegrenzung ist eine einfache Näherung und könnte bei bestimmten Dokumenten zu viel oder zu wenig Text abschneiden
- Bei sehr spezifischen Fragen könnte die einfache Kürzung relevante Informationen entfernen
- Die Dokumentauswahl erfordert eine genaue Eingabe der Nummer oder des Formats "Nummer: Frage"
