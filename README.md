# Bauanleitung für deinen IT-Support-Helfer 🤖

Hallo! Hier ist die Bauanleitung für den IT-Support-Helfer, den wir zusammen gebaut haben. Stell dir das wie die Anleitung für ein cooles Lego-Modell vor!

## Was kann der Helfer? (Das fertige Lego-Modell)

Dein IT-Helfer ist wie ein kleiner Roboter, der deinen IT-Supportern helfen kann. Er kann:

1.  **Fragen beantworten:** Er kann versuchen, Fragen zu eurer Technik zu beantworten, indem er (bald!) in euren Outline-Dokumenten nachschaut.
2.  **Kunden-Infos finden:** Er kennt eine Liste von Kunden und den dazugehörigen Servern (momentan noch eine feste Liste, später vielleicht direkt aus Dynamics).
3.  **E-Mails schreiben:** Er kann helfen, professionelle E-Mails an Kunden zu formulieren.
4.  **Neugierig sein:** Nach jeder Antwort stellt er ein paar Fragen, um mehr über das Problem und die Lösung zu erfahren.

## Die Bausteine (Die Python-Dateien)

Unser Roboter besteht aus mehreren Teilen, genau wie ein Lego-Set aus verschiedenen Steinen und Modulen:

*   **`config.py` (Die Batterie-Box & Einstellungen):** Hier stehen wichtige Einstellungen drin, vor allem die geheimen Schlüssel (API-Keys), die der Roboter braucht, um mit OpenAI (dem Gehirn) und Outline (der Wissens-Kiste) zu sprechen. Hier ist auch die feste Liste mit den Kunden-Server-Infos.
*   **`outline_utils.py` (Der Greifarm für Outline):** Dieses Teil ist dafür zuständig, mit Outline zu sprechen. Es enthält die Funktion, um in den Outline-Dokumenten nach Informationen zu suchen. Momentan braucht er noch den passenden Schlüssel (`OUTLINE_API_KEY` in `config.py`), um richtig zugreifen zu können.
*   **`openai_utils.py` (Die Verbindung zum Gehirn):** Dieses Teil verbindet unseren Roboter mit dem schlauen OpenAI-Gehirn. Es schickt die Fragen und Aufgaben an OpenAI und holt die Antworten ab. Es enthält auch die Logik, um Fragen mit Hilfe von gefundenen Dokumenten (RAG) zu beantworten und E-Mails zu entwerfen.
*   **`agent.py` (Die Hauptsteuerung):** Das ist das Herzstück des Roboters. Es nimmt deine Eingaben entgegen, überlegt, was zu tun ist (Frage beantworten? E-Mail schreiben?), benutzt den Greifarm (`outline_utils`) und die Gehirn-Verbindung (`openai_utils`), und gibt dir die Antwort. Es stellt auch die neugierigen Folgefragen.
*   **`app.py` (Das Cockpit / Die Fernsteuerung):** Das ist die schicke Oberfläche, die du im Browser siehst. Sie benutzt "Streamlit", um den Chat so ähnlich wie bei ChatGPT aussehen zu lassen und die Bedienung einfach zu machen.

## Aufbau (Bevor du loslegst)

1.  **Werkzeuge (Python & Co.):** Auf dem Computer, auf dem der Helfer laufen soll, muss Python installiert sein. Außerdem braucht er die speziellen Werkzeuge (Python-Bibliotheken), die wir installiert haben (`openai`, `langchain`, `streamlit`, `requests` usw.). Wenn du den Helfer auf deinem eigenen Computer nutzen willst, musst du diese eventuell noch installieren. Ein Befehl dafür wäre (im Terminal/Kommandozeile):
    `pip install openai langchain langchain-openai streamlit requests`
2.  **Dateien:** Du brauchst alle Python-Dateien (`.py`) im selben Ordner.

## Konfiguration (Die Schlüssel einsetzen)

Das ist **super wichtig**, damit der Helfer richtig funktioniert:

1.  Öffne die Datei `config.py` mit einem Texteditor.
2.  **OpenAI API-Schlüssel:** Ersetze den Text `DEIN_OPENAI_API_SCHLÜSSEL_HIER` durch deinen echten OpenAI API-Schlüssel. Pass gut darauf auf, er ist geheim!
3.  **Outline API-Schlüssel:** Sobald du ihn hast, ersetze `DEIN_OUTLINE_API_SCHLÜSSEL_HIER` durch deinen echten Outline API-Schlüssel.
4.  **Outline URL (Optional):** Wenn eure Outline-Instanz eine andere Adresse hat als `https://app.getoutline.com/api`, musst du die `OUTLINE_API_URL` anpassen.
5.  **Kunden-Server-Liste:** Du kannst die `STATIC_CUSTOMER_SERVER_MAP` in `config.py` bearbeiten, um die feste Liste der Kunden und Server anzupassen.
6.  Speichere die `config.py`-Datei.

## Den Helfer starten (Den Roboter einschalten)

1.  Öffne ein Terminal oder eine Kommandozeile.
2.  Wechsle in den Ordner, in dem alle Python-Dateien des Helfers liegen (z.B. `cd /pfad/zum/it_support_agent`).
3.  Gib den Befehl ein: `streamlit run app.py`
4.  Im Terminal erscheint eine Adresse (normalerweise etwas wie `http://localhost:8501`). Öffne diese Adresse in deinem Webbrowser.

Jetzt solltest du das Cockpit sehen und mit dem Helfer chatten können!

## Den Helfer benutzen (Mit dem Roboter spielen)

*   **Chatten:** Gib deine Fragen oder Aufgaben einfach in das Eingabefeld unten ein und drücke Enter.
*   **Wissensfragen:** Stelle Fragen zu eurer Technik. Sobald der Outline-Schlüssel drin ist, versucht der Helfer, in euren Dokumenten nach Antworten zu suchen.
*   **Kunden-Server-Info:** Frage z.B. "Welcher Server gehört zu Beispielkunde GmbH?". Der Helfer schaut in der Liste in `config.py` nach.
*   **E-Mail-Entwurf:** Schreibe z.B.: `Entwirf eine E-Mail Betreff: Problem gelöst Empfänger: kunde@xyz.com mit den Punkten: - Ticket #5678 abgeschlossen - Ursache war Neustart des Routers - Bei Fragen melden`
*   **Folgefragen:** Nach einer erfolgreichen Antwort stellt der Helfer dir ein paar Fragen. Beantworte sie im Formular und klicke auf "Antworten speichern".

## Wie funktioniert die Outline-Suche?

Wenn du eine Wissensfrage stellst:
1.  Der `agent.py` schickt deine Frage an `outline_utils.py`.
2.  `outline_utils.py` benutzt deinen Outline API-Schlüssel, um die Suchfunktion von Outline aufzurufen.
3.  Outline schickt eine Liste mit passenden Dokumenten (oder Textausschnitten) zurück.
4.  `agent.py` nimmt die besten Treffer und schickt sie zusammen mit deiner ursprünglichen Frage an `openai_utils.py`.
5.  `openai_utils.py` bittet das OpenAI-Gehirn, deine Frage *nur* basierend auf diesen Dokumenten-Ausschnitten zu beantworten.
6.  Du bekommst die Antwort!

## Nächste Schritte & Ideen (Mehr Lego-Steine!)

*   **Outline-Schlüssel:** Füge den Outline API-Schlüssel hinzu, um die Kernfunktion freizuschalten!
*   **Dynamics CRM:** Später könnten wir den Helfer direkt mit Dynamics verbinden, damit er Kunden- und Server-Infos automatisch abruft.
*   **Bessere Erkennung:** Man könnte die Erkennung, was der Benutzer will (E-Mail, Frage etc.), verbessern, vielleicht auch mit Hilfe von OpenAI.
*   **Fehler:** Die Fehlerbehandlung könnte noch verbessert werden.
*   **Lernen:** Die Antworten auf die Folgefragen werden momentan nur im Terminal ausgegeben. Man könnte sie in einer Datei oder Datenbank speichern, um später daraus zu lernen oder Statistiken zu erstellen.

Ich hoffe, diese Anleitung hilft dir! Viel Spaß mit deinem IT-Support-Helfer! 😊




## Umzug auf deinen Windows-Server (Schritt-für-Schritt)

Okay, jetzt bringen wir unseren IT-Helfer auf deinen Windows-Server! Das ist wie unser Lego-Modell von einem Tisch auf einen anderen zu stellen und sicherzugehen, dass alle Teile wieder richtig sitzen.

**Vorbereitung (Was du brauchst):**

*   **Alle Agenten-Dateien:** Stelle sicher, dass du alle Dateien, die wir erstellt haben, zusammen in einem Ordner hast. Das sind:
    *   `app.py`
    *   `agent.py`
    *   `openai_utils.py`
    *   `outline_utils.py`
    *   `config.py` (mit deinen API-Schlüsseln und der korrekten Outline-URL!)
    *   `requirements.txt` (Die Einkaufsliste für die Python-Pakete)
    *   `README.md` (Diese Anleitung hier)
*   **Internetzugang auf dem Server:** Für die Installation von Python und den Paketen, und später damit der Agent mit OpenAI und Outline sprechen kann.

**Schritt 1: Python auf deinem Windows-Server installieren**

1.  **Download:** Gehe zur offiziellen Python-Webseite: [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
2.  **Installer wählen:** Lade dir den neuesten stabilen Python-Installer für Windows herunter (meistens eine `.exe`-Datei).
3.  **Installation:** Führe den Installer aus. **Ganz wichtig:** Setze während der Installation das Häkchen bei **"Add Python to PATH"** (oder "Python zu Umgebungsvariablen hinzufügen"). Das macht es viel einfacher, Python später in der Kommandozeile aufzurufen.
    *   Du kannst die Standard-Installationseinstellungen meistens übernehmen.
4.  **Überprüfen:** Öffne nach der Installation eine neue Kommandozeile (suche nach `cmd` oder `PowerShell` im Startmenü) und gib ein:
    ```bash
    python --version
    ```
    Und auch:
    ```bash
    pip --version
    ```
    Wenn beides eine Versionsnummer anzeigt, hat die Installation geklappt!

**Schritt 2: Die Agenten-Dateien auf den Server kopieren**

1.  Erstelle einen neuen Ordner auf deinem Windows-Server, wo der IT-Helfer wohnen soll. Zum Beispiel: `C:\IT_Support_Agent`
2.  Kopiere alle Agenten-Dateien (die `.py`-Dateien, `config.py`, `requirements.txt`, `README.md`) in diesen Ordner.

**Schritt 3: Eine virtuelle Umgebung erstellen (Empfohlen)**

Das ist wie eine eigene kleine Werkstatt nur für unseren Helfer, damit er nicht mit anderen Python-Projekten auf dem Server durcheinanderkommt.

1.  Öffne eine Kommandozeile.
2.  Wechsle in den Ordner, in den du die Agenten-Dateien kopiert hast:
    ```bash
    cd C:\IT_Support_Agent
    ```
3.  Erstelle die virtuelle Umgebung (nennen wir sie `venv`):
    ```bash
    python -m venv venv
    ```
4.  Aktiviere die virtuelle Umgebung:
    ```bash
    .\venv\Scripts\activate
    ```
    Du solltest jetzt am Anfang deiner Kommandozeilen-Eingabe `(venv)` sehen. Das zeigt, dass die virtuelle Werkstatt aktiv ist.

**Schritt 4: Die benötigten Python-Pakete installieren**

Jetzt benutzen wir unsere Einkaufsliste (`requirements.txt`), um alle speziellen Lego-Steine zu holen.

1.  Stelle sicher, dass deine virtuelle Umgebung aktiv ist (siehe Schritt 3).
2.  Gib in der Kommandozeile ein:
    ```bash
    pip install -r requirements.txt
    ```
    Das lädt jetzt alle Pakete herunter und installiert sie in deiner virtuellen Werkstatt. Das kann ein paar Minuten dauern.

**Schritt 5: Konfiguration überprüfen**

Doppelt hält besser! Öffne die `config.py`-Datei auf dem Server (z.B. mit Notepad oder einem anderen Texteditor) und stelle sicher, dass:
*   Dein `OPENAI_API_KEY` korrekt eingetragen ist.
*   Dein `OUTLINE_API_KEY` korrekt eingetragen ist.
*   Die `OUTLINE_API_URL` auf `https://docs.meta10.app/api` (oder eure spezifische URL) zeigt.

**Schritt 6: Den IT-Helfer starten!**

Jetzt wird es spannend!

1.  Stelle sicher, dass deine virtuelle Umgebung noch aktiv ist (sonst mit `.\venv\Scripts\activate` wieder aktivieren).
2.  Gib in der Kommandozeile ein:
    ```bash
    streamlit run app.py
    ```
3.  Streamlit startet jetzt den Server. In der Kommandozeile siehst du wahrscheinlich Ausgaben, darunter eine **Local URL** (meist `http://localhost:8501`) und eine **Network URL** (eine IP-Adresse mit Port `8501`).
4.  Öffne einen Webbrowser **auf dem Windows-Server selbst** und gib die `http://localhost:8501` Adresse ein. Du solltest das Cockpit des IT-Helfers sehen!

**Schritt 7: Zugriff von anderen Computern (Firewall)**

Wenn du von anderen Computern im Netzwerk auf den IT-Helfer zugreifen möchtest (über die Network URL, die Streamlit anzeigt):

1.  Du musst eventuell eine **Ausnahmeregel in der Windows-Firewall** auf dem Server erstellen, um eingehende Verbindungen auf dem Port `8501` (oder welchen Port Streamlit auch immer verwendet) zu erlauben.
2.  Suche in Windows nach "Windows Defender Firewall mit erweiterter Sicherheit".
3.  Gehe zu "Eingehende Regeln" -> "Neue Regel...".
4.  Wähle "Port", dann "TCP" und gib den spezifischen lokalen Port an (z.B. `8501`).
5.  Wähle "Verbindung zulassen".
6.  Wähle, für welche Netzwerkprofile die Regel gelten soll (Domäne, Privat, Öffentlich – sei hier vorsichtig, besonders mit Öffentlich).
7.  Gib der Regel einen Namen (z.B. "Streamlit IT Agent").

**Wichtige Hinweise für den Betrieb auf dem Server:**

*   **Kommandozeile offen lassen:** Das Kommandozeilenfenster, in dem du `streamlit run app.py` gestartet hast, muss offen bleiben, solange der Helfer laufen soll. Wenn du es schließt, stoppt auch der Helfer.
*   **Fehlersuche:** Wenn etwas nicht klappt, schau dir die Ausgaben in der Kommandozeile an. Dort stehen oft hilfreiche Fehlermeldungen.
*   **Outline-Schlüssel:** Wenn die Outline-Suche immer noch nicht geht, liegt es sehr wahrscheinlich am API-Schlüssel oder dessen Berechtigungen in eurer Outline-Instanz (`https://docs.meta10.app`).

Das war's! Jetzt sollte dein IT-Helfer auf deinem Windows-Server laufen. Viel Erfolg beim Umzug! Wenn Fragen auftauchen, sag Bescheid. 😊

