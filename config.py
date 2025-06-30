# Konfigurationsdatei für den IT-Support-Agenten

# Füge hier deinen OpenAI API-Schlüssel ein
OPENAI_API_KEY = "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"

# Füge hier deinen Outline API-Schlüssel ein
OUTLINE_API_KEY = "ol_api_NgjmEJzifDXgGt1Qf3GD7Bule2VcobWzhL6bfE"
# Füge hier die Basis-URL deiner Outline-Instanz ein (falls selbst gehostet oder andere Domain)
# Standard ist "https://app.getoutline.com/api"
OUTLINE_API_URL = "https://docs.meta10.app/api"

# Statische Liste für Kunden-Server-Mapping (für den Anfang)
# Beispiel: {"Kunde A": "Server 1", "Kunde B": "Server 2"}
STATIC_CUSTOMER_SERVER_MAP = {
    "Beispielkunde GmbH": "webserver01.beispiel.com",
    "Musterfirma AG": "dbserver03.muster.local",
    "Meta10 AG" : "c00temphost35"
}
