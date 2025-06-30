"""
Testskript für die Fallbasis-Funktionalität.
Dieses Skript testet das Speichern und Abrufen von Support-Fällen in der Vektordatenbank.
"""

import case_memory

def main():
    # Aktuelle Anzahl der gespeicherten Fälle anzeigen
    print(f'Aktuelle Anzahl gespeicherter Fälle: {case_memory.get_case_count()}')
    
    # Testfall speichern
    case_id = case_memory.store_support_case(
        customer='Testfirma GmbH',
        problem='Outlook startet nicht mehr nach Windows-Update',
        solution='Outlook im abgesicherten Modus gestartet und Add-Ins deaktiviert',
        customer_mood='Leicht verärgert',
        recurring_problem=False
    )
    print(f'Testfall gespeichert mit ID: {case_id}')
    
    # Zweiten Testfall speichern
    case_id2 = case_memory.store_support_case(
        customer='Meta10 AG',
        problem='Excel-Datei mit Makros wird blockiert',
        solution='Makros in den Vertrauenseinstellungen zugelassen und Datei in vertrauenswürdigen Speicherort verschoben',
        customer_mood='Neutral',
        recurring_problem=True
    )
    print(f'Zweiter Testfall gespeichert mit ID: {case_id2}')
    
    # Nach ähnlichen Fällen suchen
    print('\nSuche nach ähnlichen Fällen für "Outlook startet nicht":')
    similar = case_memory.find_similar_cases('Outlook startet nicht')
    print(f'Gefundene ähnliche Fälle: {len(similar)}')
    
    for case in similar:
        print(f'- Kunde: {case["customer"]}, Relevanz: {case["relevance"]}%')
        print(f'  Problem: {case["problem"]}')
        print(f'  Lösung: {case["solution"]}')
    
    # Vorschlag für eine ähnliche Anfrage generieren
    suggestion = case_memory.get_case_suggestion('Outlook Problem nach Update')
    print(f'\nVorschlag für "Outlook Problem nach Update":')
    print(suggestion)
    
    # Suche nach Excel-Problem
    print('\nSuche nach ähnlichen Fällen für "Excel Makro Problem":')
    similar_excel = case_memory.find_similar_cases('Excel Makro Problem')
    print(f'Gefundene ähnliche Fälle: {len(similar_excel)}')
    
    for case in similar_excel:
        print(f'- Kunde: {case["customer"]}, Relevanz: {case["relevance"]}%')
        print(f'  Problem: {case["problem"]}')
        print(f'  Lösung: {case["solution"]}')
    
    # Aktuelle Anzahl der gespeicherten Fälle nach dem Test anzeigen
    print(f'\nAktuelle Anzahl gespeicherter Fälle nach dem Test: {case_memory.get_case_count()}')

if __name__ == "__main__":
    main()
