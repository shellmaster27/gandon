# Chat-Historie Dokumentation

## Übersicht

Der IT-Support-Helfer wurde um eine **Chat-Historie-Funktion** erweitert, die es ermöglicht, mehrere separate Konversationen zu führen, zwischen ihnen zu wechseln und sie zu verwalten. Diese Funktion macht den Helfer noch benutzerfreundlicher und ermöglicht es, verschiedene Support-Themen getrennt zu behandeln.

## Funktionen der Chat-Historie

Die Chat-Historie bietet folgende Funktionen:

1. **Mehrere Chats verwalten**: Erstellen und zwischen verschiedenen Chats wechseln
2. **Automatische Benennung**: Chats werden automatisch nach der ersten Frage benannt
3. **Umbenennen**: Chats können jederzeit umbenannt werden
4. **Löschen**: Nicht mehr benötigte Chats können gelöscht werden
5. **Exportieren**: Chats können in verschiedenen Formaten (Text, JSON, HTML) exportiert werden
6. **Aufklappbare Liste**: Die Chat-Liste kann ein- und ausgeblendet werden

## Nutzung der Chat-Historie

### Die Chat-Liste anzeigen/ausblenden

- Klicke auf den Button "📝 Chat-Liste anzeigen" in der Seitenleiste, um die Liste der Chats anzuzeigen
- Klicke auf "📝 Chat-Liste ausblenden", um die Liste wieder zu verbergen

### Einen neuen Chat starten

1. Öffne die Chat-Liste (falls nicht bereits sichtbar)
2. Klicke auf den Button "➕ Neuer Chat"
3. Ein neuer, leerer Chat wird erstellt und automatisch geöffnet

### Zwischen Chats wechseln

1. Öffne die Chat-Liste
2. Klicke auf den Titel des Chats, zu dem du wechseln möchtest
3. Der ausgewählte Chat wird geladen und angezeigt
4. Der aktuelle Chat ist mit "👈" markiert

### Einen Chat umbenennen

1. Öffne die Chat-Liste
2. Klicke auf das Stift-Symbol "✏️" neben dem Chat, den du umbenennen möchtest
3. Gib den neuen Namen ein
4. Klicke auf "✓" zum Speichern oder "✗" zum Abbrechen

### Einen Chat löschen

1. Öffne die Chat-Liste
2. Klicke auf das Papierkorb-Symbol "🗑️" neben dem Chat, den du löschen möchtest
3. Der Chat wird sofort gelöscht (ohne Bestätigung)
4. Wenn du den aktuellen Chat löschst, wird automatisch ein neuer Chat erstellt

### Einen Chat exportieren

1. Wähle in der Seitenleiste unter "Chat exportieren" das gewünschte Format aus:
   - Text (.txt): Einfaches Textformat
   - JSON (.json): Strukturiertes Datenformat
   - HTML (.html): Formatierte Webseite
2. Klicke auf "💾 Exportieren"
3. Klicke auf "📥 Download", um die Datei herunterzuladen

## Technische Details

- Die Chats werden in einer lokalen SQLite-Datenbank gespeichert
- Die Datenbank befindet sich im Installationsverzeichnis des IT-Support-Helfers
- Es werden standardmäßig die letzten 5 Chats in der Liste angezeigt
- Alle Chats bleiben in der Datenbank, bis sie explizit gelöscht werden

## Tipps für die optimale Nutzung

1. **Thematische Trennung**: Nutze separate Chats für unterschiedliche Themen oder Kunden
2. **Regelmäßiges Aufräumen**: Lösche nicht mehr benötigte Chats, um die Liste übersichtlich zu halten
3. **Aussagekräftige Namen**: Benenne Chats um, wenn die automatische Benennung nicht aussagekräftig genug ist
4. **Exportieren wichtiger Chats**: Exportiere wichtige Support-Gespräche zur Dokumentation

## Häufige Fragen

**F: Werden die Chats automatisch gespeichert?**  
A: Ja, alle Nachrichten werden automatisch in der Datenbank gespeichert.

**F: Kann ich mehr als 5 Chats speichern?**  
A: Ja, es werden immer nur die 5 neuesten Chats angezeigt, aber alle bleiben gespeichert.

**F: Werden die Chats zwischen verschiedenen Nutzern geteilt?**  
A: Nein, die Chats sind lokal auf dem Server gespeichert und werden von allen Nutzern geteilt.

**F: Kann ich einen gelöschten Chat wiederherstellen?**  
A: Nein, gelöschte Chats können nicht wiederhergestellt werden.
