# Wiederherstellung des IT-Support-Helfers: Dokumentation

## Übersicht

Diese Dokumentation beschreibt die Wiederherstellung des ursprünglichen IT-Support-Helfers mit verbesserten Outline-Integrationsfunktionen. Nach Problemen mit dem Multi-Agent-Ansatz wurde entschieden, zur bewährten Einzelagenten-Architektur zurückzukehren.

## Durchgeführte Änderungen

1. **Wiederherstellung der ursprünglichen Codebasis**
   - Zurückkehr zur bewährten Einzelagenten-Architektur
   - Beibehaltung aller Verbesserungen für die Outline-Integration

2. **API-Schlüssel-Konfiguration**
   - Integration des neuen OpenAI API-Schlüssels für verbesserte Zuverlässigkeit
   - Beibehaltung des funktionierenden Outline API-Schlüssels

3. **Modell-Aktualisierung**
   - Umstellung von GPT-3.5 Turbo auf GPT-4.1 für verbesserte Antwortqualität
   - Anpassung aller relevanten Funktionen in openai_utils.py

4. **Outline-Integration**
   - Vollständige Dokumenteninhaltsextraktion
   - Zweistufiger Dialog für Dokumentsuche und -auswahl
   - Anzeige von Dokument-URLs für direkten Zugriff

## Funktionen des IT-Support-Helfers

1. **Dokumentsuche mit `/docs`**
   - Suche in Outline-Dokumenten mit dem Präfix `/docs`
   - Zweistufiger Dialog für die Auswahl spezifischer Dokumente
   - Extraktion und Anzeige des vollständigen Dokumentinhalts

2. **Allgemeine Konversation**
   - Beantwortung allgemeiner Fragen mit OpenAI GPT-4.1
   - Kontextbezogene Antworten basierend auf gefundenen Dokumenten

3. **E-Mail-Entwürfe**
   - Unterstützung bei der Formulierung von E-Mails
   - Berücksichtigung firmenspezifischer Begriffe und Kontext

4. **Falldokumentation**
   - Formular zur Dokumentation von Supportfällen über den Befehl `/document`

## Nutzungshinweise

1. **Dokumentsuche**
   - Verwende `/docs [Suchbegriff]` für die Suche in Outline-Dokumenten
   - Wähle ein Dokument aus der Liste durch Eingabe der Nummer
   - Stelle spezifische Fragen zu einem Dokument mit `[Nummer]: [Frage]`

2. **Allgemeine Fragen**
   - Stelle Fragen ohne Präfix für allgemeine Antworten
   - Der Helfer nutzt OpenAI GPT-4.1 für Antworten, wenn keine passenden Dokumente gefunden werden

3. **E-Mail-Entwürfe**
   - Beschreibe den gewünschten E-Mail-Inhalt
   - Der Helfer erstellt einen Entwurf basierend auf deinen Angaben

## Fehlerbehebung

Bei Problemen mit dem IT-Support-Helfer:

1. **Outline-Verbindungsprobleme**
   - Überprüfe, ob der Outline API-Schlüssel in `config.py` korrekt ist
   - Stelle sicher, dass die Outline-Instanz erreichbar ist

2. **OpenAI-Verbindungsprobleme**
   - Überprüfe, ob der OpenAI API-Schlüssel in `config.py` korrekt ist
   - Bei Rate-Limit-Fehlern warte einige Minuten und versuche es erneut
   - Stelle sicher, dass das GPT-4.1 Modell für deinen API-Schlüssel verfügbar ist

3. **Allgemeine Probleme**
   - Starte die App neu mit `cd /home/ubuntu/it_support_agent && streamlit run app.py`
   - Überprüfe die Logs in `streamlit.log` für detaillierte Fehlerinformationen
