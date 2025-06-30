# Streamlit Benutzeroberfläche für den IT-Support-Agenten

import streamlit as st
import agent
import config
import case_memory
import chat_storage
import os
import datetime
import json

# --- Seitenkonfiguration ---
st.set_page_config(page_title="IT-Support Helfer", layout="wide")

# --- Initialisierung des Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "follow_up_pending" not in st.session_state:
    st.session_state.follow_up_pending = False
if "follow_up_answers" not in st.session_state:
    st.session_state.follow_up_answers = {}
if "dialog_state" not in st.session_state:
    st.session_state.dialog_state = "initial"
if "current_chat_id" not in st.session_state:
    # Erstelle einen neuen Chat beim ersten Start
    st.session_state.current_chat_id = chat_storage.create_new_chat("Neue Unterhaltung")
if "show_chat_list" not in st.session_state:
    st.session_state.show_chat_list = False
if "rename_mode" not in st.session_state:
    st.session_state.rename_mode = False
if "rename_chat_id" not in st.session_state:
    st.session_state.rename_chat_id = None
if "export_format" not in st.session_state:
    st.session_state.export_format = "text"

# --- Funktionen für die Chat-Verwaltung ---
def create_new_chat():
    """Erstellt einen neuen Chat und wechselt zu diesem."""
    st.session_state.current_chat_id = chat_storage.create_new_chat("Neue Unterhaltung")
    st.session_state.messages = []
    st.session_state.follow_up_pending = False
    st.session_state.dialog_state = "initial"
    st.rerun()

def switch_to_chat(chat_id):
    """Wechselt zu einem bestehenden Chat."""
    st.session_state.current_chat_id = chat_id
    st.session_state.messages = []
    
    # Lade alle Nachrichten für diesen Chat
    messages = chat_storage.get_chat_messages(chat_id)
    for msg in messages:
        st.session_state.messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    
    st.session_state.follow_up_pending = False
    st.session_state.dialog_state = "initial"
    st.rerun()

def toggle_chat_list():
    """Schaltet die Anzeige der Chat-Liste ein/aus."""
    st.session_state.show_chat_list = not st.session_state.show_chat_list
    st.rerun()

def delete_current_chat():
    """Löscht den aktuellen Chat und wechselt zu einem neuen."""
    if st.session_state.current_chat_id:
        chat_storage.delete_chat(st.session_state.current_chat_id)
    create_new_chat()

def enter_rename_mode(chat_id):
    """Aktiviert den Umbenennen-Modus für einen Chat."""
    st.session_state.rename_mode = True
    st.session_state.rename_chat_id = chat_id
    st.rerun()

def save_chat_rename(chat_id, new_title):
    """Speichert den neuen Titel für einen Chat."""
    if new_title.strip():
        chat_storage.rename_chat(chat_id, new_title)
    st.session_state.rename_mode = False
    st.session_state.rename_chat_id = None
    st.rerun()

def cancel_rename():
    """Bricht den Umbenennen-Vorgang ab."""
    st.session_state.rename_mode = False
    st.session_state.rename_chat_id = None
    st.rerun()

def export_current_chat():
    """Exportiert den aktuellen Chat im gewählten Format."""
    if not st.session_state.current_chat_id:
        return None, "Kein aktiver Chat"
    
    success, content = chat_storage.export_chat(
        st.session_state.current_chat_id, 
        st.session_state.export_format
    )
    
    if not success:
        return None, "Export fehlgeschlagen"
    
    # Bestimme Dateiendung basierend auf Format
    extension = {
        "json": ".json",
        "text": ".txt",
        "html": ".html"
    }.get(st.session_state.export_format, ".txt")
    
    # Hole Chat-Titel für den Dateinamen
    chats = chat_storage.get_recent_chats(100)
    chat_title = "chat_export"
    for chat in chats:
        if chat["id"] == st.session_state.current_chat_id:
            chat_title = chat["title"].replace(" ", "_")[:30]
            break
    
    # Erstelle Dateinamen mit Zeitstempel
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{chat_title}_{timestamp}{extension}"
    
    # Speichere in temporärer Datei
    export_path = os.path.join("/tmp", filename)
    with open(export_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    return export_path, filename

# --- Haupttitel ---
st.title("M10 Support Agent")
st.caption("Ich kann Fragen zu internen Dokumenten beantworten, Kunden-Server-Infos liefern und E-Mails entwerfen.")

# --- Seitenleiste mit Chat-Liste ---
with st.sidebar:
    # Chat-Liste ein-/ausklappen
    if st.button("📝 " + ("Chat-Liste ausblenden" if st.session_state.show_chat_list else "Chat-Liste anzeigen")):
        toggle_chat_list()
    
    # Chat-Liste anzeigen, wenn aktiviert
    if st.session_state.show_chat_list:
        st.subheader("Deine Chats")
        
        # Neuer Chat Button
        if st.button("➕ Neuer Chat", key="new_chat_btn"):
            create_new_chat()
        
        # Liste der letzten Chats
        recent_chats = chat_storage.get_recent_chats(5)
        for chat in recent_chats:
            col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
            
            # Umbenennen-Modus für diesen Chat?
            if st.session_state.rename_mode and st.session_state.rename_chat_id == chat["id"]:
                with col1:
                    new_title = st.text_input("Neuer Titel:", value=chat["title"], key=f"rename_{chat['id']}")
                with col2:
                    if st.button("✓", key=f"save_{chat['id']}"):
                        save_chat_rename(chat["id"], new_title)
                with col3:
                    if st.button("✗", key=f"cancel_{chat['id']}"):
                        cancel_rename()
            else:
                # Normaler Anzeigemodus
                with col1:
                    # Markiere den aktuellen Chat
                    title_text = chat["title"]
                    if chat["id"] == st.session_state.current_chat_id:
                        title_text = f"**{title_text}** 👈"
                    
                    if st.button(title_text, key=f"chat_{chat['id']}", use_container_width=True):
                        switch_to_chat(chat["id"])
                
                with col2:
                    if st.button("✏️", key=f"edit_{chat['id']}"):
                        enter_rename_mode(chat["id"])
                
                with col3:
                    if st.button("🗑️", key=f"delete_{chat['id']}"):
                        if chat["id"] == st.session_state.current_chat_id:
                            delete_current_chat()
                        else:
                            chat_storage.delete_chat(chat["id"])
                            st.rerun()
    
    # Trennlinie
    st.divider()
    
    # Export-Funktionen
    if st.session_state.current_chat_id:
        st.subheader("Chat exportieren")
        export_format = st.selectbox(
            "Format:",
            options=["text", "json", "html"],
            format_func=lambda x: {"text": "Text (.txt)", "json": "JSON (.json)", "html": "HTML (.html)"}[x],
            key="export_format_select"
        )
        st.session_state.export_format = export_format
        
        if st.button("💾 Exportieren"):
            export_path, filename = export_current_chat()
            if export_path:
                with open(export_path, "r", encoding="utf-8") as f:
                    content = f.read()
                st.download_button(
                    label="📥 Download",
                    data=content,
                    file_name=filename,
                    mime={
                        "text": "text/plain",
                        "json": "application/json",
                        "html": "text/html"
                    }.get(export_format, "text/plain")
                )
    
    # Fallbasis-Statistik
    st.divider()
    st.subheader("Fallbasis-Statistik")
    case_count = case_memory.get_case_count()
    st.metric("Gespeicherte Support-Fälle", case_count)
    
    if case_count > 0:
        st.success(f"Der Agent kann aus {case_count} früheren Support-Fällen lernen und ähnliche Lösungen vorschlagen.")
    else:
        st.info("Noch keine Support-Fälle in der Fallbasis. Verwende den Befehl `/document`, um Fälle zu dokumentieren.")
    
    st.divider()
    st.caption("Verwende `/document`, um einen neuen Support-Fall zu dokumentieren.")
    st.caption("Verwende `/docs [Suchbegriff]`, um in der Wissensdatenbank zu suchen.")

# --- Anzeige des Chat-Verlaufs ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Haupt-Chat-Interaktion ---
# Nur anzeigen, wenn keine Folgefragen offen sind
if not st.session_state.follow_up_pending:
    if prompt := st.chat_input("Stell mir eine Frage oder gib mir eine Aufgabe..."):
        # Benutzereingabe zum Verlauf hinzufügen und anzeigen
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Nachricht in der Datenbank speichern
        chat_storage.add_message(st.session_state.current_chat_id, "user", prompt)
        
        # Bei der ersten Nachricht den Chat-Titel aktualisieren
        if len(st.session_state.messages) == 1:
            chat_storage.update_chat_title_from_first_message(st.session_state.current_chat_id)

        if prompt.strip().lower() == "/document":
            st.session_state.follow_up_pending = True
            st.session_state.follow_up_answers = {} # Reset für neue Antworten
            assistant_response_for_command = "Bitte fülle die Falldetails aus:"
            st.session_state.messages.append({"role": "assistant", "content": assistant_response_for_command})
            
            # Nachricht in der Datenbank speichern
            chat_storage.add_message(st.session_state.current_chat_id, "assistant", assistant_response_for_command)
            
            with st.chat_message("assistant"):
                st.markdown(assistant_response_for_command)
            st.rerun() 
        else:
            # Agentenantwort generieren und anzeigen
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                message_placeholder.markdown("Denke nach... 🧠")
                # Prüfen, ob API-Schlüssel konfiguriert sind
                api_keys_missing = not agent.openai_utils.client or \
                                   not config.OUTLINE_API_KEY or \
                                   config.OUTLINE_API_KEY == "DEIN_OUTLINE_API_SCHLÜSSEL_HIER" or \
                                   not config.OUTLINE_API_URL or \
                                   config.OUTLINE_API_URL == "DEINE_OUTLINE_INSTANZ_URL_HIER"

                if api_keys_missing:
                    response = "🚨 **FEHLER:** API-Schlüssel oder URL für OpenAI oder Outline fehlen in `config.py`! Bitte konfiguriere alles, damit ich richtig arbeiten kann."
                else:
                    # Synchronisiere den Dialog-Status mit dem Agent
                    agent.last_interaction_details["dialog_state"] = st.session_state.dialog_state
                    
                    # Verarbeite die Anfrage
                    response = agent.process_query(prompt)
                    
                    # Aktualisiere den Dialog-Status aus dem Agent
                    st.session_state.dialog_state = agent.last_interaction_details["dialog_state"]

                message_placeholder.markdown(response)
                # Agentenantwort zum Verlauf hinzufügen
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Nachricht in der Datenbank speichern
                chat_storage.add_message(st.session_state.current_chat_id, "assistant", response)

# --- Folgefragen-Interaktion ---
if st.session_state.follow_up_pending:
    st.info("Bitte beantworte die folgenden Fragen zur letzten Interaktion:")
    follow_up_questions = agent.get_follow_up_questions()
    all_answered = True

    form = st.form(key="follow_up_form")
    with form:
        for i, question in enumerate(follow_up_questions):
            # Verwende eindeutige Schlüssel für jedes Textfeld
            answer_key = f"follow_up_{i}"
            # Zeige die Frage an und sammle die Antwort
            st.session_state.follow_up_answers[question] = st.text_area(
                question,
                key=answer_key,
                value=st.session_state.follow_up_answers.get(question, "") # Behalte den Wert bei Re-Runs
            )
            # Prüfe, ob alle Fragen beantwortet wurden (einfache Prüfung auf Nicht-Leerheit)
            if not st.session_state.follow_up_answers[question]:
                all_answered = False

        submitted = st.form_submit_button("Antworten speichern")

    if submitted:
        if all_answered:
            # Verarbeite die Antworten und speichere den Fall in der Vektordatenbank
            confirmation = agent.process_follow_up_answers(st.session_state.follow_up_answers)
            
            # Füge eine Bestätigungsnachricht zum Chat hinzu
            st.session_state.messages.append({"role": "assistant", "content": confirmation})
            
            # Nachricht in der Datenbank speichern
            chat_storage.add_message(st.session_state.current_chat_id, "assistant", confirmation)
            
            # Setze den Status zurück, damit neue Eingaben möglich sind
            st.session_state.follow_up_pending = False
            st.session_state.follow_up_answers = {}
            
            # Seite neu laden, um das Formular auszublenden und die Bestätigung anzuzeigen
            st.rerun()
        else:
            st.warning("Bitte beantworte alle Folgefragen, bevor du speicherst.")

# --- Hinweis auf API-Schlüssel (wenn nicht konfiguriert) ---
if not agent.openai_utils.client or not config.OUTLINE_API_KEY or config.OUTLINE_API_KEY == "DEIN_OUTLINE_API_SCHLÜSSEL_HIER":
    st.warning("**Konfiguration unvollständig:** Bitte trage die API-Schlüssel für OpenAI und Outline in die Datei `config.py` im Verzeichnis `/home/ubuntu/it_support_agent/` ein, damit der Agent voll funktionsfähig ist.", icon="⚠️")
