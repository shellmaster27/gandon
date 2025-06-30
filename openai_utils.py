# Hilfsfunktionen für die OpenAI API

import config
from openai import OpenAI

# Initialisiere den OpenAI-Client
# Stellt sicher, dass der API-Schlüssel nicht der Platzhalter ist
client = None
if config.OPENAI_API_KEY and config.OPENAI_API_KEY != "DEIN_OPENAI_API_SCHLÜSSEL_HIER":
    try:
        client = OpenAI(api_key=config.OPENAI_API_KEY)
        print("OpenAI Client erfolgreich initialisiert.")
    except Exception as e:
        print(f"FEHLER bei der Initialisierung des OpenAI Clients: {e}")
        client = None # Stelle sicher, dass der Client None ist, wenn die Initialisierung fehlschlägt
else:
    print("WARNUNG: OpenAI API-Schlüssel fehlt oder ist der Platzhalter in config.py. OpenAI-Funktionen sind deaktiviert.")

def get_openai_completion(prompt: str, model: str = "gpt-4.1") -> str:
    """Erhält eine Textvervollständigung von OpenAI.

    Args:
        prompt: Der Eingabetext für das Modell.
        model: Das zu verwendende OpenAI-Modell (Standard: gpt-4.1).

    Returns:
        Die generierte Textvervollständigung oder eine Fehlermeldung.
    """
    if not client:
        return "FEHLER: OpenAI Client nicht initialisiert. Bitte API-Schlüssel in config.py prüfen."

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Du bist ein hilfreicher Assistent für IT-Supporter."},
                {"role": "user", "content": prompt}
            ]
        )
        # Extrahiere die Antwort aus der komplexen Struktur
        if response.choices:
            return response.choices[0].message.content.strip()
        else:
            return "FEHLER: Keine Antwort von OpenAI erhalten."

    except Exception as e:
        print(f"FEHLER bei der OpenAI API-Anfrage: {e}")
        # Gib eine aussagekräftige Fehlermeldung zurück
        if "authentication" in str(e).lower():
            return "FEHLER: OpenAI API-Schlüssel ist ungültig oder fehlt."
        elif "rate limit" in str(e).lower():
            return "FEHLER: OpenAI Rate Limit erreicht. Bitte später erneut versuchen."
        else:
            return f"FEHLER bei der Kommunikation mit OpenAI: {e}"

# --- Funktion für RAG (Retrieval-Augmented Generation) ---
def answer_question_with_context(question: str, context_documents: list, model: str = "gpt-4.1") -> str:
    """Beantwortet eine Frage basierend auf bereitgestelltem Kontext aus Dokumenten.

    Args:
        question: Die Frage des Benutzers.
        context_documents: Eine Liste von Textausschnitten aus relevanten Dokumenten.
        model: Das zu verwendende OpenAI-Modell.

    Returns:
        Die generierte Antwort oder eine Fehlermeldung.
    """
    if not client:
        return "FEHLER: OpenAI Client nicht initialisiert. Bitte API-Schlüssel in config.py prüfen."

    if not context_documents:
        # Wenn kein Kontext gefunden wurde, versuche die Frage direkt zu beantworten
        # oder gib eine entsprechende Meldung zurück.
        # Hier versuchen wir eine direkte Antwort:
        print("Kein Kontext gefunden, versuche direkte Antwort von OpenAI...")
        return get_openai_completion(f"Beantworte die folgende IT-Support-Frage: {question}")

    # Baue den Prompt mit Kontext zusammen
    context_text = "\n\n".join(context_documents)
    prompt = f"""Beantworte die folgende Frage ausschließlich basierend auf dem bereitgestellten Kontext.
Wenn die Antwort nicht im Kontext enthalten ist, sage "Die Antwort ist in den mir bekannten Dokumenten nicht enthalten.".
Sei präzise und gib nur die Antwort auf die Frage.

Kontext:
---
{context_text}
---

Frage: {question}

Antwort:"""

    return get_openai_completion(prompt, model)

# --- Funktion zum Entwerfen von E-Mails ---
def draft_email(recipient: str, subject: str, points: str, tone: str = "professionell", model: str = "gpt-4.1") -> str:
    """Entwirft eine E-Mail basierend auf Stichpunkten.

    Args:
        recipient: Der Empfänger der E-Mail.
        subject: Der Betreff der E-Mail.
        points: Die wichtigsten Punkte, die in der E-Mail enthalten sein sollen.
        tone: Der gewünschte Ton der E-Mail (z.B. professionell, freundlich).
        model: Das zu verwendende OpenAI-Modell.

    Returns:
        Der E-Mail-Entwurf oder eine Fehlermeldung.
    """
    if not client:
        return "FEHLER: OpenAI Client nicht initialisiert. Bitte API-Schlüssel in config.py prüfen."

    prompt = f"""Entwirf eine E-Mail an {recipient} mit dem Betreff "{subject}".
Die E-Mail soll im Ton "{tone}" sein und die folgenden Punkte behandeln:
{points}

Beginne direkt mit der Anrede und schließe mit einer passenden Grußformel und Absender (z.B. "Mit freundlichen Grüßen, Ihr IT-Support").

E-Mail-Entwurf:"""

    return get_openai_completion(prompt, model)


# Beispielaufrufe (nur zum Testen)
if __name__ == "__main__":
    if client:
        # Test 1: Einfache Vervollständigung
        # print("\n--- Test: Einfache Vervollständigung ---")
        # simple_prompt = "Was ist der Unterschied zwischen TCP und UDP?"
        # print(f"Frage: {simple_prompt}")
        # print(f"Antwort: {get_openai_completion(simple_prompt)}")

        # Test 2: Frage mit Kontext (RAG)
        print("\n--- Test: Frage mit Kontext (RAG) ---")
        test_question = "Wie richte ich einen neuen Drucker unter Windows 11 ein?"
        test_context = [
            "Anleitung: Druckerinstallation Windows 11. Schritt 1: Gehen Sie zu Einstellungen > Bluetooth & Geräte > Drucker & Scanner.",
            "Schritt 2: Klicken Sie auf \"Gerät hinzufügen\". Windows sucht nach verfügbaren Druckern.",
            "Schritt 3: Wählen Sie Ihren Drucker aus der Liste aus und klicken Sie auf \"Gerät hinzufügen\". Wenn Ihr Drucker nicht angezeigt wird, klicken Sie auf \"Der gewünschte Drucker ist nicht aufgeführt\" und folgen Sie den Anweisungen, um ihn manuell hinzuzufügen, z.B. über TCP/IP.",
            "Troubleshooting: Wenn der Drucker nicht erkannt wird, prüfen Sie die Netzwerkverbindung und ob der Drucker eingeschaltet ist."
        ]
        print(f"Frage: {test_question}")
        print(f"Kontext: {test_context}")
        print(f"Antwort: {answer_question_with_context(test_question, test_context)}")

        # Test 3: E-Mail Entwurf
        print("\n--- Test: E-Mail Entwurf ---")
        email_points = "- Bestätigung des gelösten Problems (Ticket #12345)\n- Kurze Erklärung der Ursache (Netzwerkkabel war locker)\n- Hinweis auf erneute Kontaktaufnahme bei weiteren Problemen"
        print(f"Punkte für E-Mail: {email_points}")
        print(f"Entwurf:\n{draft_email(recipient='Herr Müller', subject='Ihr IT-Problem wurde gelöst (Ticket #12345)', points=email_points)}")
    else:
        print("OpenAI Client nicht initialisiert. Tests können nicht durchgeführt werden. Bitte API-Schlüssel in config.py prüfen.")
