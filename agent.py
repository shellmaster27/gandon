# Hauptlogik für den IT-Support-Agenten

import config
import outline_utils
import openai_utils
import case_memory
import knowledge_base

# Globale Variable, um den letzten Kontext zu speichern (optional, für Follow-up)
last_interaction_details = {
    "query": None,
    "response": None,
    "context_used": None,
    "found_documents": None,  # Speichert gefundene Dokumente für den zweistufigen Dialog
    "dialog_state": "initial"  # Mögliche Zustände: "initial", "document_list", "document_selected"
}

def process_query(user_input: str) -> str:
    """Verarbeitet eine Benutzereingabe, entscheidet über den Workflow und gibt eine Antwort zurück.

    Args:
        user_input: Die Eingabe des Benutzers.

    Returns:
        Die Antwort des Agenten.
    """
    global last_interaction_details
    
    # Prüfen auf firmenspezifisches Wissen
    specific_knowledge = knowledge_base.find_matching_knowledge(user_input)
    if specific_knowledge:
        print(f"Bearbeite firmenspezifisches Problem: {specific_knowledge['title']}...")

        response = f"**{specific_knowledge['title']}**\n\n"
        response += "**Mögliche Lösungen:**\n\n"
        response += "\n".join(specific_knowledge['solutions'])
        return response

    # Prüfen, ob wir uns im Dialog-Workflow befinden
    if last_interaction_details["dialog_state"] == "document_list":
        # Benutzer hat eine Dokumentauswahl getroffen
        return handle_document_selection(user_input)
    
    # Ansonsten neue Anfrage starten
    last_interaction_details = {
        "query": user_input, 
        "response": None, 
        "context_used": None,
        "found_documents": None,
        "dialog_state": "initial"
    }

    # --- 1. Intent Recognition ---
    is_email_request = "entwirf eine e-mail" in user_input.lower() or "schreib eine mail" in user_input.lower()
    is_customer_server_query = "welcher server" in user_input.lower() and ("kunde" in user_input.lower() or "customer" in user_input.lower())
    is_docs_search = user_input.lower().startswith("/docs")
    
    # Rest of the existing logic...
    # [Previous code for handling different intents remains the same]
    
    # Ansonsten neue Anfrage starten
    last_interaction_details = {
        "query": user_input, 
        "response": None, 
        "context_used": None,
        "found_documents": None,
        "dialog_state": "initial"
    }

    # --- 1. Intent Recognition (Sehr einfach gehalten) ---
    # Entscheiden, ob es eine Frage für die Wissensdatenbank, eine E-Mail-Anfrage oder etwas anderes ist.
    # Hier könnte man komplexere Logik oder ein LLM für die Intent-Erkennung einsetzen.
    is_email_request = "entwirf eine e-mail" in user_input.lower() or "schreib eine mail" in user_input.lower()
    is_customer_server_query = "welcher server" in user_input.lower() and ("kunde" in user_input.lower() or "customer" in user_input.lower())
    
    # Neue Logik: Prüfen, ob es eine Dokumentsuche mit /docs Präfix ist
    is_docs_search = user_input.lower().startswith("/docs")
    
    # Prüfen, ob ähnliche Fälle aus der Fallbasis gefunden werden können
    case_suggestion = None
    if not is_email_request and not is_customer_server_query and not is_docs_search and not user_input.lower().startswith("/"):
        # Versuche, ähnliche Fälle zu finden
        case_suggestion = case_memory.get_case_suggestion(user_input)

    # --- 2. Workflow basierend auf Intent ---
    if is_email_request:
        # TODO: E-Mail-Parameter extrahieren (Empfänger, Betreff, Punkte)
        # Dies ist eine vereinfachte Annahme, dass der Input alle Infos enthält.
        # In der Praxis bräuchte man eine robustere Extraktion.
        print("Bearbeite E-Mail-Anfrage...")
        # Beispielhafte Extraktion (sehr naiv!)
        try:
            parts = user_input.split("Betreff:")
            points_part = parts[0]
            subject_recipient = parts[1].split("Empfänger:")
            subject = subject_recipient[0].strip()
            recipient = subject_recipient[1].strip()
            # Punkte sind der Rest vom Anfang
            points = points_part.replace("entwirf eine e-mail", "", 1).replace("schreib eine mail", "", 1).strip()
            response = openai_utils.draft_email(recipient=recipient, subject=subject, points=points)
        except Exception as e:
            print(f"Fehler beim Parsen der E-Mail-Anfrage: {e}")
            response = "Ich konnte die Details für die E-Mail nicht verstehen. Bitte gib sie klar an, z.B.: Entwirf eine E-Mail Betreff: [Betreff] Empfänger: [Empfänger] mit den Punkten: [Punkte]"

    elif is_customer_server_query:
        # Statische Kunden-Server-Abfrage
        print("Bearbeite Kunden-Server-Anfrage...")
        found = False
        for customer, server in config.STATIC_CUSTOMER_SERVER_MAP.items():
            if customer.lower() in user_input.lower():
                response = f"Der Kunde {customer} ist dem Server {server} zugeordnet."
                found = True
                break
        if not found:
            response = "Ich konnte den gesuchten Kunden nicht in meiner Liste finden."

    elif is_docs_search:
        # Dokumentsuche mit /docs Präfix
        print("Bearbeite Dokumentsuche...")
        # Entferne das /docs Präfix und führe die Suche mit dem Rest durch
        search_query = user_input[5:].strip()
        
        if not search_query:
            return "Bitte gib nach `/docs` einen Suchbegriff ein, z.B. `/docs Topal` oder `/docs VPN Anleitung`."
        
        print("Suche in Outline nach Kontext für:")
        print(search_query)
        print("---")
        context_docs_raw = outline_utils.search_outline_documents(search_query)

        # Zeige nur Dokumenttitel und URLs an
        if context_docs_raw:
            # Extrahiere Titel, IDs und URLs
            docs_info = outline_utils.get_document_titles_and_urls(context_docs_raw)
            
            # Speichere die gefundenen Dokumente für den Dialog-Workflow
            last_interaction_details["found_documents"] = docs_info
            last_interaction_details["dialog_state"] = "document_list"
            
            # Erstelle eine formatierte Antwort mit Dokumenttiteln und URLs
            response = f"Ich habe {len(docs_info)} Dokument(e) gefunden, die zu deiner Anfrage '{search_query}' passen:\n\n"
            
            for i, doc in enumerate(docs_info, 1):
                response += f"{i}. **{doc['title']}**\n"
                if doc['url']:
                    response += f"   URL: {doc['url']}\n"
                response += "\n"
                
            response += "Bitte gib die Nummer des Dokuments an, zu dem du mehr Informationen möchtest, oder stelle eine spezifische Frage zu einem der Dokumente (z.B. '2: Wie funktioniert die Installation?')."
        else:
            response = f"Ich konnte leider keine passenden Dokumente zu '{search_query}' finden. Bitte versuche es mit anderen Suchbegriffen."
    
    else:
        # Allgemeine Frage - verwende OpenAI direkt ohne Outline-Kontext
        print("Bearbeite allgemeine Frage...")
        
        # Wenn ein ähnlicher Fall gefunden wurde, füge ihn als Kontext hinzu
        prompt = f"Beantworte die folgende Frage als IT-Support-Helfer: {user_input}"
        
        if case_suggestion:
            # Füge den Vorschlag zur Antwort hinzu
            response = openai_utils.get_openai_completion(prompt)
            response += "\n\n---\n\n" + case_suggestion
        else:
            response = openai_utils.get_openai_completion(prompt)
        
        # Hinweis auf /docs hinzufügen, wenn es wie eine Dokumentsuche aussieht
        if any(keyword in user_input.lower() for keyword in ["anleitung", "dokument", "doku", "finde", "suche", "wie geht", "wie macht man"]):
            response += "\n\n*Hinweis: Wenn du nach Dokumenten in unserer Wissensdatenbank suchen möchtest, verwende bitte das Format `/docs [Suchbegriff]`, z.B. `/docs Topal` oder `/docs VPN Anleitung`.*"

    last_interaction_details["response"] = response
    return response

def handle_document_selection(user_input: str) -> str:
    """Verarbeitet die Auswahl eines Dokuments durch den Benutzer.
    
    Args:
        user_input: Die Eingabe des Benutzers, z.B. "2" oder "2: Wie funktioniert...".
        
    Returns:
        Die Antwort des Agenten mit Informationen aus dem ausgewählten Dokument.
    """
    global last_interaction_details
    
    # Prüfen, ob der Benutzer eine neue Dokumentsuche starten möchte
    if user_input.lower().startswith("/docs"):
        # Setze den Dialog-Status zurück und starte eine neue Suche
        last_interaction_details["dialog_state"] = "initial"
        return process_query(user_input)
    
    # Extrahiere die Dokumentnummer und ggf. eine spezifische Frage
    parts = user_input.split(":", 1)
    try:
        # Versuche, die Dokumentnummer zu extrahieren
        doc_num = int(parts[0].strip())
        
        # Prüfe, ob die Nummer gültig ist
        if doc_num < 1 or doc_num > len(last_interaction_details["found_documents"]):
            return f"Bitte wähle eine gültige Dokumentnummer zwischen 1 und {len(last_interaction_details['found_documents'])}."
        
        # Hole das ausgewählte Dokument
        selected_doc = last_interaction_details["found_documents"][doc_num - 1]
        doc_id = selected_doc["id"]
        doc_title = selected_doc["title"]
        doc_url = selected_doc["url"]
        
        # Extrahiere die spezifische Frage, falls vorhanden
        specific_question = ""
        if len(parts) > 1:
            specific_question = parts[1].strip()
        
        # Hole den Dokumentinhalt mit Begrenzung (für OpenAI Token-Limit)
        # Wir verwenden eine Zeichenbegrenzung als einfache Näherung für Tokens
        # Ein besserer Ansatz wäre ein echter Token-Counter
        MAX_CHARS = 6000  # Ungefähre Begrenzung, um unter dem Token-Limit zu bleiben
        doc_content, _, _ = outline_utils.get_document_summary(doc_id, MAX_CHARS)
        
        if not doc_content:
            return f"Ich konnte leider den Inhalt des Dokuments '{doc_title}' nicht abrufen. Bitte versuche es später noch einmal."
        
        # Setze den Dialog-Status zurück
        last_interaction_details["dialog_state"] = "initial"
        
        # Erstelle den Prompt für OpenAI
        if specific_question:
            prompt = f"Beantworte folgende Frage basierend auf dem Dokument '{doc_title}': {specific_question}"
            context_snippets = [doc_content]
            response = openai_utils.answer_question_with_context(prompt, context_snippets)
        else:
            # Wenn keine spezifische Frage gestellt wurde, gib eine Zusammenfassung
            prompt = f"Fasse den Inhalt des Dokuments '{doc_title}' kurz zusammen."
            context_snippets = [doc_content]
            response = openai_utils.answer_question_with_context(prompt, context_snippets)
        
        # Füge die URL zum Dokument hinzu
        if doc_url:
            response += f"\n\n**Dokument-URL:** {doc_url}"
        
        # Hinweis auf neue Suche hinzufügen
        response += "\n\n*Für eine neue Dokumentsuche verwende bitte `/docs [Suchbegriff]`.*"
        
        return response
        
    except ValueError:
        # Wenn keine gültige Zahl eingegeben wurde
        return "Bitte gib eine gültige Dokumentnummer ein (z.B. '2' oder '2: Wie funktioniert...')."
    except Exception as e:
        print(f"Fehler bei der Verarbeitung der Dokumentauswahl: {e}")
        last_interaction_details["dialog_state"] = "initial"  # Zurücksetzen bei Fehler
        return "Es ist ein Fehler bei der Verarbeitung deiner Auswahl aufgetreten. Bitte versuche es erneut mit einer neuen Suche (`/docs [Suchbegriff]`)."

def get_follow_up_questions() -> list:
    """Gibt die Standard-Folgefragen zurück.

    Returns:
        Eine Liste von Folgefragen.
    """
    return [
        "Welcher Kunde hatte das Problem?",
        "Was genau war das Problem des Kunden?",
        "Was war die Lösung für das Problem?",
        "War der Kunde während des Supports schwierig oder verärgert?",
        "Tritt dieses Problem bei diesem Kunden häufiger auf?"
    ]

def process_follow_up_answers(answers: dict) -> str:
    """Verarbeitet die Antworten auf die Folgefragen und speichert sie in der Fallbasis.
    
    Args:
        answers: Dictionary mit Fragen als Schlüssel und Antworten als Werte
        
    Returns:
        Bestätigungsnachricht
    """
    try:
        # Extrahiere die Antworten
        customer = answers.get("Welcher Kunde hatte das Problem?", "")
        problem = answers.get("Was genau war das Problem des Kunden?", "")
        solution = answers.get("Was war die Lösung für das Problem?", "")
        customer_mood = answers.get("War der Kunde während des Supports schwierig oder verärgert?", "")
        recurring = "ja" in answers.get("Tritt dieses Problem bei diesem Kunden häufiger auf?", "").lower()
        
        # Speichere den Fall in der Vektordatenbank
        case_id = case_memory.store_support_case(
            customer=customer,
            problem=problem,
            solution=solution,
            customer_mood=customer_mood,
            recurring_problem=recurring
        )
        
        # Erstelle eine Bestätigungsnachricht
        case_count = case_memory.get_case_count()
        return f"Danke für die Dokumentation! Der Fall wurde erfolgreich gespeichert (ID: {case_id}).\n\nInsgesamt sind jetzt {case_count} Fälle in der Wissensdatenbank, die bei ähnlichen Anfragen helfen können."
    
    except Exception as e:
        print(f"Fehler beim Speichern des Falls: {e}")
        return "Es gab ein Problem beim Speichern des Falls. Bitte versuche es später noch einmal."

# Haupt-Schleife (für ein einfaches Kommandozeilen-Interface zum Testen)
if __name__ == "__main__":
    print("IT-Support-Agent gestartet. Tippe 'exit' zum Beenden.")
    print("Für Dokumentsuche verwende '/docs [Suchbegriff]', z.B. '/docs Topal'.")
    print("Für Falldokumentation verwende '/document'.")
    # Prüfen, ob API-Schlüssel gesetzt sind
    if not openai_utils.client or not config.OUTLINE_API_KEY or config.OUTLINE_API_KEY == "DEIN_OUTLINE_API_SCHLÜSSEL_HIER":
        print("\nWARNUNG: API-Schlüssel für OpenAI oder Outline fehlen in config.py!")
        print("Der Agent wird nur eingeschränkt oder gar nicht funktionieren.")
        print("Bitte trage die Schlüssel in /home/ubuntu/it_support_agent/config.py ein.\n")

    while True:
        user_query = input("\nDu: ")
        if user_query.lower() == 'exit':
            break

        agent_response = process_query(user_query)
        print(f"\nAgent: {agent_response}")

        # Stelle die Folgefragen nur, wenn wir nicht im Dialog-Workflow sind und keine Fehlermeldung vorliegt
        if agent_response and "FEHLER:" not in agent_response and last_interaction_details["dialog_state"] == "initial":
            print("\nAgent (Folgefragen):")
            follow_up_questions = get_follow_up_questions()
            follow_up_answers = {}
            for q in follow_up_questions:
                # Hier könnte man die Antworten des Nutzers sammeln und speichern/verarbeiten
                user_follow_up_answer = input(f"- {q} ")
                follow_up_answers[q] = user_follow_up_answer
                print(f"  (Notiert: {user_follow_up_answer[:50]}...)") # Nur zur Demo
            
            # Verarbeite die Antworten und speichere den Fall
            confirmation = process_follow_up_answers(follow_up_answers)
            print(f"\nAgent: {confirmation}")

    print("Agent beendet.")