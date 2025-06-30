"""
Modul zur Speicherung und zum Abrufen von Support-Fällen mit ChromaDB.
Ermöglicht das Lernen aus früheren Fällen und das Abrufen ähnlicher Fälle bei neuen Anfragen.
"""

import os
import json
import chromadb
from datetime import datetime
from typing import List, Dict, Any, Optional

# Pfad für die lokale Speicherung der ChromaDB-Daten
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "case_memory_db")

# Initialisierung der ChromaDB-Client
client = chromadb.PersistentClient(path=DB_PATH)

# Collection für Support-Fälle erstellen oder laden
try:
    collection = client.get_collection(name="support_cases")
    print("Support-Fälle Collection erfolgreich geladen.")
except Exception:
    collection = client.create_collection(name="support_cases")
    print("Support-Fälle Collection neu erstellt.")

def store_support_case(customer: str, problem: str, solution: str, customer_mood: str, recurring_problem: bool) -> str:
    """
    Speichert einen neuen Support-Fall in der Vektordatenbank.
    
    Args:
        customer: Name des Kunden
        problem: Beschreibung des Problems
        solution: Beschreibung der Lösung
        customer_mood: Stimmung des Kunden während des Supports
        recurring_problem: Ob das Problem bei diesem Kunden häufiger auftritt
        
    Returns:
        ID des gespeicherten Falls
    """
    # Eindeutige ID für den Fall generieren
    case_id = f"case_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Vollständigen Text für die Vektorisierung erstellen
    full_text = f"Kunde: {customer}\nProblem: {problem}\nLösung: {solution}\nKundenstimmung: {customer_mood}\nWiederholtes Problem: {'Ja' if recurring_problem else 'Nein'}"
    
    # Metadaten für den Fall
    metadata = {
        "customer": customer,
        "timestamp": datetime.now().isoformat(),
        "recurring_problem": recurring_problem,
        "customer_mood": customer_mood
    }
    
    # Fall in ChromaDB speichern
    collection.add(
        documents=[full_text],
        metadatas=[metadata],
        ids=[case_id]
    )
    
    print(f"Support-Fall für Kunde '{customer}' erfolgreich gespeichert (ID: {case_id}).")
    return case_id

def find_similar_cases(query: str, limit: int = 3) -> List[Dict[str, Any]]:
    """
    Findet ähnliche Support-Fälle basierend auf einer Anfrage.
    
    Args:
        query: Die Suchanfrage (Problem- oder Lösungsbeschreibung)
        limit: Maximale Anzahl zurückzugebender Fälle
        
    Returns:
        Liste ähnlicher Fälle mit Relevanz-Score
    """
    if collection.count() == 0:
        print("Keine Support-Fälle in der Datenbank vorhanden.")
        return []
    
    # Ähnliche Fälle in ChromaDB suchen
    results = collection.query(
        query_texts=[query],
        n_results=limit
    )
    
    # Ergebnisse formatieren
    similar_cases = []
    if results and results['documents'] and len(results['documents'][0]) > 0:
        for i, (doc, metadata, distance) in enumerate(zip(
            results['documents'][0], 
            results['metadatas'][0], 
            results['distances'][0]
        )):
            # Relevanz-Score berechnen (1 - normalisierte Distanz)
            # Je näher an 1, desto relevanter
            relevance = 1 - (distance / 2)  # Normalisierung für Cosine-Distanz
            
            # Extrahiere Problem und Lösung aus dem Dokument
            parts = doc.split('\n')
            problem = next((p.replace('Problem: ', '') for p in parts if p.startswith('Problem: ')), '')
            solution = next((p.replace('Lösung: ', '') for p in parts if p.startswith('Lösung: ')), '')
            
            similar_cases.append({
                "customer": metadata.get("customer", "Unbekannter Kunde"),
                "problem": problem,
                "solution": solution,
                "timestamp": metadata.get("timestamp", ""),
                "relevance": round(relevance * 100)  # Prozentuale Relevanz
            })
    
    return similar_cases

def get_case_suggestion(query: str) -> Optional[str]:
    """
    Erstellt einen Vorschlag basierend auf ähnlichen Fällen.
    
    Args:
        query: Die aktuelle Anfrage oder Problembeschreibung
        
    Returns:
        Ein formatierter Vorschlag oder None, wenn keine ähnlichen Fälle gefunden wurden
    """
    similar_cases = find_similar_cases(query)
    
    if not similar_cases:
        return None
    
    # Erstelle einen hilfreichen Vorschlag basierend auf dem relevantesten Fall
    best_match = similar_cases[0]
    suggestion = (
        f"**Ähnlicher Fall gefunden:** Bei Kunde *{best_match['customer']}* hatten wir "
        f"ein ähnliches Problem ({best_match['relevance']}% Übereinstimmung).\n\n"
        f"**Problem:** {best_match['problem']}\n\n"
        f"**Lösung:** {best_match['solution']}\n\n"
    )
    
    # Wenn es weitere ähnliche Fälle gibt, erwähne sie kurz
    if len(similar_cases) > 1:
        suggestion += "**Weitere ähnliche Fälle:**\n"
        for case in similar_cases[1:]:
            suggestion += f"- Kunde *{case['customer']}*: {case['problem'][:50]}... ({case['relevance']}% Übereinstimmung)\n"
    
    return suggestion

def get_case_count() -> int:
    """
    Gibt die Anzahl der gespeicherten Fälle zurück.
    
    Returns:
        Anzahl der Fälle in der Datenbank
    """
    return collection.count()

# Beispiel für die Verwendung (wird nur ausgeführt, wenn die Datei direkt ausgeführt wird)
if __name__ == "__main__":
    # Beispiel-Fall speichern
    case_id = store_support_case(
        customer="Testfirma GmbH",
        problem="Outlook startet nicht mehr nach Windows-Update",
        solution="Outlook im abgesicherten Modus gestartet und Add-Ins deaktiviert",
        customer_mood="Leicht verärgert",
        recurring_problem=False
    )
    
    # Ähnliche Fälle suchen
    similar = find_similar_cases("Outlook startet nicht")
    print(f"Gefundene ähnliche Fälle: {len(similar)}")
    for case in similar:
        print(f"- Kunde: {case['customer']}, Relevanz: {case['relevance']}%")
        print(f"  Problem: {case['problem']}")
        print(f"  Lösung: {case['solution']}")
