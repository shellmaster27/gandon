# IT-Support-Helfer: Update zum /docs-Präfix und Dialog-Workflow

## Zusammenfassung der Änderungen

Der IT-Support-Helfer wurde weiter verbessert, um die Benutzerführung zu optimieren und Verwirrung zu vermeiden:

1. **Neues `/docs`-Präfix:** Outline-Dokumentsuchen werden jetzt ausschließlich durch das Präfix `/docs` ausgelöst
2. **Klare Trennung:** Allgemeine Fragen und Dokumentsuchen sind jetzt eindeutig getrennt
3. **Verbesserte Nutzerführung:** Klare Hinweise zur Verwendung des `/docs`-Präfix

## Technische Details der Änderungen

### 1. Neue Intent-Erkennung in `agent.py`

- **Spezifische Erkennung für `/docs`-Anfragen:**
  ```python
  is_docs_search = user_input.lower().startswith("/docs")
  ```

- **Unterschiedliche Verarbeitung je nach Intent:**
  - `/docs`-Anfragen: Suche in Outline-Dokumenten
  - Allgemeine Fragen: Direkte Beantwortung durch OpenAI ohne Outline-Kontext

### 2. Verbesserter Dialog-Workflow

- **Klare Trennung der Modi:**
  - Dokumentsuche: Nur mit `/docs [Suchbegriff]`
  - Dokumentauswahl: Einfache Zahlen (z.B. "2" oder "2: Wie funktioniert...")
  - Allgemeine Fragen: Werden direkt an OpenAI weitergeleitet

- **Hilfreiche Hinweise:**
  - Bei allgemeinen Fragen, die wie Dokumentsuchen aussehen, wird auf das `/docs`-Format hingewiesen
  - Nach Dokumentantworten wird auf die Möglichkeit einer neuen Suche hingewiesen

### 3. Verbesserte Fehlerbehandlung

- **Spezifische Fehlermeldungen:**
  - Bei leerem Suchbegriff nach `/docs`
  - Bei ungültigen Dokumentnummern
  - Bei Fehlern in der Dokumentauswahl

## Nutzung und Tests

Der verbesserte Agent bietet jetzt einen klareren Workflow:

1. **Dokumentsuche starten:** Verwende `/docs [Suchbegriff]` (z.B. `/docs Topal` oder `/docs VPN Anleitung`)
2. **Dokument auswählen:** Gib die Nummer des gewünschten Dokuments ein (z.B. "2" oder "2: Wie funktioniert...")
3. **Allgemeine Fragen stellen:** Stelle Fragen ohne `/docs`-Präfix für direkte Antworten von OpenAI

## Wartung und zukünftige Anpassungen

Für zukünftige Verbesserungen könnten folgende Punkte berücksichtigt werden:

- **Erweiterte Präfix-Befehle:** Weitere Befehle wie `/email` für E-Mail-Entwürfe oder `/server` für Serverabfragen
- **Verbesserte Suche:** Optimierung der Suchlogik in Outline für bessere Ergebnisse
- **Kontextübergreifende Fragen:** Möglichkeit, Fragen über mehrere Dokumente hinweg zu beantworten

## Bekannte Einschränkungen

- Das `/docs`-Präfix muss exakt so eingegeben werden (Groß-/Kleinschreibung spielt keine Rolle)
- Bei der Dokumentauswahl muss die Nummer als Zahl eingegeben werden
- Die Zeichenbegrenzung für Dokumentinhalte ist weiterhin aktiv, um das Token-Limit nicht zu überschreiten
