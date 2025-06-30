# wissensdatebank für Spezifischeri Usecases

COMPANY_SPECIFIC_KNOWLEDGE = {
    "cloud_login_issues": {
        "keywords": ["cloud anmelden", "cloud login", "anmeldung cloud",
                     "kann nicht in die cloud", "cloud zugriff",
                     "anmeldeproblem", "einloggen cloud"],
        "title": "Cloud-Anmeldeprobleme",
        "solutions": [
            "1. **Kennwort abgelaufen** - Prüfen Sie, ob das Passwort des Kunden abgelaufen ist und setzen Sie es ggf. zurück",
            "2. **Duo User Expired - Kann es sein dass der Duo User blockiert wurde wegen zu vielen Anmeldungen oder sogar wegen Abwesenheit",
            "3. **VHDX noch gemountet in der PrivateCloud** - Prüfen Sie, ob Terminal-Server-Sessions hängen geblieben sind",
            "4. **Lokales Profil blockiert** - Versuchen Sie, das lokale Profil auf dem Client-Rechner zu löschen",
            "5. **Zu viele gleichzeitige Anmeldungen** - Prüfen Sie, ob der Benutzer die maximale Anzahl an Sessions erreicht hat"
        ],
        "follow_up_questions": [
            "Hat der Kunde kürzlich sein Passwort geändert?",
            "Tritt das Problem auf allen Geräten auf oder nur auf einem bestimmten?"
        ]
    },

    # Weitere Probleme hier hinzufügen
    "vpn_connection_issues": {
        "keywords": ["vpn verbindung", "vpn problem", "kann nicht verbinden"],
        "title": "VPN-Verbindungsprobleme",
        "solutions": [
            "1. **Netzwerkprobleme** - Prüfen Sie die Internetverbindung des Kunden",
            "2. **VPN-Client veraltet** - Aktualisieren Sie den VPN-Client auf die neueste Version",
            # Weitere Lösungen...
        ],
        "follow_up_questions": [
            # Folgefragen...
        ]
    }

    "1001 Fehlermeldung" : {
        "keywords": ["1001 error", "1001 fehler", "1001 fehlermeldung", "Outlook Anmeldung fehlgeschlagen"],
    }
}


def find_matching_knowledge(query: str) -> dict:
    """Findet passendes Wissen basierend auf der Benutzeranfrage.

    Args:
        query: Die Benutzeranfrage

    Returns:
        Matching knowledge entry or None
    """
    query_lower = query.lower()

    for problem_id, problem_data in COMPANY_SPECIFIC_KNOWLEDGE.items():
        if any(keyword in query_lower for keyword in problem_data["keywords"]):
            return problem_data

    return None