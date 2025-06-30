# Hilfsfunktionen für die Outline API

import requests
import config

def search_outline_documents(query: str) -> list:
    """Durchsucht Outline-Dokumente über die API.

    Args:
        query: Der Suchbegriff.

    Returns:
        Eine Liste von Suchergebnissen (Dokumenten-Infos) oder eine leere Liste bei Fehlern.
    """
    if not config.OUTLINE_API_KEY or config.OUTLINE_API_KEY == "DEIN_OUTLINE_API_SCHLÜSSEL_HIER":
        print("FEHLER: Outline API-Schlüssel fehlt in config.py")
        # Im echten Betrieb würden wir hier vielleicht eine Fehlermeldung an den Nutzer geben
        # oder eine Exception werfen.
        # Für die Entwicklung geben wir eine leere Liste zurück.
        return []

    headers = {
        "Authorization": f"Bearer {config.OUTLINE_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    # Outline API Endpunkt für die Dokumentensuche
    # Siehe Outline API Dokumentation für den korrekten Endpunkt und Parameter
    # Beispiel: '/documents.search'
    search_endpoint = f"{config.OUTLINE_API_URL.rstrip('/')}/documents.search"

    payload = {
        "query": query,
        # Weitere Parameter nach Bedarf, z.B. limit, offset, collectionId etc.
        # "limit": 10
    }

    try:
        response = requests.post(search_endpoint, headers=headers, json=payload)
        response.raise_for_status()  # Löst einen Fehler aus bei HTTP-Statuscodes 4xx/5xx

        results = response.json()
        # Die Struktur der Antwort hängt von der Outline API ab.
        # Wir nehmen an, 'data' enthält die Liste der Dokumente.
        documents = results.get("data", [])
        # Möglicherweise müssen wir auch die dazugehörigen Dokument-Kontexte extrahieren
        # context = results.get("context", {})

        print(f"Outline Suche für '{query}' ergab {len(documents)} Dokument(e).")
        return documents # Oder eine verarbeitete Liste davon

    except requests.exceptions.RequestException as e:
        print(f"FEHLER bei der Outline API-Anfrage: {e}")
        # Hier könnte man spezifischer auf Fehler wie ungültigen API-Schlüssel (401)
        # oder nicht gefundenen Endpunkt (404) reagieren.
        return []
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
        return []

def get_document_content(document_id: str) -> str:
    """Ruft den vollständigen Inhalt eines Dokuments über die Outline API ab.
    
    Args:
        document_id: Die ID des Dokuments.
        
    Returns:
        Der vollständige Inhalt des Dokuments oder ein leerer String bei Fehlern.
    """
    if not config.OUTLINE_API_KEY or config.OUTLINE_API_KEY == "DEIN_OUTLINE_API_SCHLÜSSEL_HIER":
        print("FEHLER: Outline API-Schlüssel fehlt in config.py")
        return ""
        
    headers = {
        "Authorization": f"Bearer {config.OUTLINE_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    
    # Outline API Endpunkt für Dokumentendetails
    info_endpoint = f"{config.OUTLINE_API_URL.rstrip('/')}/documents.info"
    
    payload = {
        "id": document_id
    }
    
    try:
        response = requests.post(info_endpoint, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        document = result.get("data", {})
        
        # Extrahiere den Inhalt des Dokuments
        title = document.get("title", "")
        text = document.get("text", "")
        url = document.get("url", "")
        
        print(f"Dokument '{title}' (ID: {document_id}) erfolgreich abgerufen.")
        
        # Kombiniere Titel und Text für besseren Kontext
        full_content = f"# {title}\n\n{text}"
        return full_content, title, url
        
    except requests.exceptions.RequestException as e:
        print(f"FEHLER beim Abrufen des Dokuments (ID: {document_id}): {e}")
        return "", "", ""
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
        return "", "", ""

def get_document_summary(document_id: str, max_chars: int = 1000) -> str:
    """Ruft eine gekürzte Zusammenfassung eines Dokuments ab.
    
    Args:
        document_id: Die ID des Dokuments.
        max_chars: Maximale Anzahl an Zeichen für die Zusammenfassung.
        
    Returns:
        Eine gekürzte Zusammenfassung des Dokuments oder ein leerer String bei Fehlern.
    """
    full_content, title, url = get_document_content(document_id)
    
    if not full_content:
        return "", title, url
    
    # Einfache Kürzung auf max_chars Zeichen
    if len(full_content) > max_chars:
        summary = full_content[:max_chars] + "..."
    else:
        summary = full_content
        
    return summary, title, url

def get_document_titles_and_urls(search_results: list) -> list:
    """Extrahiert Titel, IDs und URLs aus Suchergebnissen.
    
    Args:
        search_results: Liste von Suchergebnissen aus search_outline_documents.
        
    Returns:
        Liste von Dictionaries mit Titel, ID und URL für jedes Dokument.
    """
    documents_info = []
    
    for doc_info in search_results:
        doc = doc_info.get("document", {})
        doc_id = doc.get("id", "")
        title = doc.get("title", "")
        url = doc.get("url", "")
        
        if doc_id and title:
            documents_info.append({
                "id": doc_id,
                "title": title,
                "url": url
            })
    
    return documents_info

# Beispielaufruf (nur zum Testen, wird nicht ausgeführt, wenn importiert)
if __name__ == "__main__":
    # Stelle sicher, dass config.py existiert und Schlüssel (testweise) gesetzt sind
    # Beispiel: config.OUTLINE_API_KEY = "test_key"
    # config.OUTLINE_API_URL = "https://app.getoutline.com/api"
    if config.OUTLINE_API_KEY != "DEIN_OUTLINE_API_SCHLÜSSEL_HIER":
        search_term = "Serverkonfiguration"
        found_docs = search_outline_documents(search_term)
        if found_docs:
            print("Gefundene Dokumente:")
            docs_info = get_document_titles_and_urls(found_docs)
            for doc in docs_info:
                print(f"- Titel: {doc['title']}, URL: {doc['url']}")
                
                # Teste auch das Abrufen des vollständigen Inhalts
                if doc['id']:
                    summary, title, url = get_document_summary(doc['id'], 200)
                    print(f"  Inhalt (Auszug): {summary}")
        else:
            print(f"Keine Dokumente für '{search_term}' gefunden oder Fehler.")
    else:
        print("Bitte zuerst API-Schlüssel in config.py setzen für den Test.")
