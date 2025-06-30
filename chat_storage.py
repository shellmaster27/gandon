"""
Modul zur Verwaltung der Chat-Historie mit SQLite.
Ermöglicht das Speichern, Laden, Umbenennen und Löschen von Chatverläufen.
"""

import os
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple

# Pfad für die SQLite-Datenbank
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chat_history.db")

def init_database():
    """Initialisiert die SQLite-Datenbank mit den notwendigen Tabellen."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tabelle für Chat-Sessions
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chat_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Tabelle für Chat-Nachrichten
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chat_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (session_id) REFERENCES chat_sessions (id) ON DELETE CASCADE
    )
    ''')
    
    conn.commit()
    conn.close()
    
    print(f"Datenbank initialisiert: {DB_PATH}")

def create_new_chat(title: str = "Neue Unterhaltung") -> int:
    """
    Erstellt eine neue Chat-Session in der Datenbank.
    
    Args:
        title: Titel der Chat-Session
        
    Returns:
        ID der erstellten Chat-Session
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO chat_sessions (title) VALUES (?)",
        (title,)
    )
    
    session_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    print(f"Neue Chat-Session erstellt: {title} (ID: {session_id})")
    return session_id

def add_message(session_id: int, role: str, content: str) -> int:
    """
    Fügt eine Nachricht zu einer Chat-Session hinzu.
    
    Args:
        session_id: ID der Chat-Session
        role: Rolle des Absenders (user oder assistant)
        content: Inhalt der Nachricht
        
    Returns:
        ID der hinzugefügten Nachricht
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Nachricht hinzufügen
    cursor.execute(
        "INSERT INTO chat_messages (session_id, role, content) VALUES (?, ?, ?)",
        (session_id, role, content)
    )
    
    message_id = cursor.lastrowid
    
    # Updated_at der Session aktualisieren
    cursor.execute(
        "UPDATE chat_sessions SET updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (session_id,)
    )
    
    conn.commit()
    conn.close()
    
    return message_id

def get_chat_messages(session_id: int) -> List[Dict[str, Any]]:
    """
    Holt alle Nachrichten einer Chat-Session.
    
    Args:
        session_id: ID der Chat-Session
        
    Returns:
        Liste von Nachrichten als Dictionaries
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Ermöglicht Zugriff auf Spalten über Namen
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, role, content, timestamp FROM chat_messages WHERE session_id = ? ORDER BY timestamp",
        (session_id,)
    )
    
    messages = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return messages

def get_recent_chats(limit: int = 5) -> List[Dict[str, Any]]:
    """
    Holt die neuesten Chat-Sessions.
    
    Args:
        limit: Maximale Anzahl der zurückzugebenden Sessions
        
    Returns:
        Liste von Chat-Sessions als Dictionaries
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, title, created_at, updated_at FROM chat_sessions ORDER BY updated_at DESC LIMIT ?",
        (limit,)
    )
    
    chats = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return chats

def rename_chat(session_id: int, new_title: str) -> bool:
    """
    Benennt eine Chat-Session um.
    
    Args:
        session_id: ID der Chat-Session
        new_title: Neuer Titel
        
    Returns:
        True bei Erfolg, False bei Fehler
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE chat_sessions SET title = ? WHERE id = ?",
            (new_title, session_id)
        )
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    except Exception as e:
        print(f"Fehler beim Umbenennen des Chats: {e}")
        return False

def delete_chat(session_id: int) -> bool:
    """
    Löscht eine Chat-Session und alle zugehörigen Nachrichten.
    
    Args:
        session_id: ID der Chat-Session
        
    Returns:
        True bei Erfolg, False bei Fehler
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Nachrichten löschen
        cursor.execute("DELETE FROM chat_messages WHERE session_id = ?", (session_id,))
        
        # Session löschen
        cursor.execute("DELETE FROM chat_sessions WHERE id = ?", (session_id,))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    except Exception as e:
        print(f"Fehler beim Löschen des Chats: {e}")
        return False

def export_chat(session_id: int, format_type: str = "json") -> Tuple[bool, str]:
    """
    Exportiert eine Chat-Session in verschiedenen Formaten.
    
    Args:
        session_id: ID der Chat-Session
        format_type: Format des Exports (json, text, html)
        
    Returns:
        Tuple mit (Erfolg, Exportinhalt)
    """
    try:
        # Chat-Daten abrufen
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Session-Informationen
        cursor.execute(
            "SELECT title, created_at FROM chat_sessions WHERE id = ?",
            (session_id,)
        )
        session = cursor.fetchone()
        
        if not session:
            return False, "Chat-Session nicht gefunden"
        
        # Nachrichten
        messages = get_chat_messages(session_id)
        
        # Export je nach Format
        if format_type == "json":
            export_data = {
                "title": session["title"],
                "created_at": session["created_at"],
                "messages": messages
            }
            return True, json.dumps(export_data, indent=2)
        
        elif format_type == "text":
            lines = [f"Chat: {session['title']}", f"Erstellt am: {session['created_at']}", ""]
            
            for msg in messages:
                role = "Du" if msg["role"] == "user" else "Agent"
                lines.append(f"{role} ({msg['timestamp']}):")
                lines.append(msg["content"])
                lines.append("")
            
            return True, "\n".join(lines)
        
        elif format_type == "html":
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Chat-Export: {session['title']}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .message {{ margin-bottom: 15px; padding: 10px; border-radius: 5px; }}
                    .user {{ background-color: #e6f7ff; text-align: right; }}
                    .assistant {{ background-color: #f0f0f0; }}
                    .timestamp {{ font-size: 0.8em; color: #666; }}
                </style>
            </head>
            <body>
                <h1>Chat: {session['title']}</h1>
                <p>Erstellt am: {session['created_at']}</p>
                <div class="chat">
            """
            
            for msg in messages:
                role_class = "user" if msg["role"] == "user" else "assistant"
                html += f"""
                <div class="message {role_class}">
                    <div class="content">{msg['content']}</div>
                    <div class="timestamp">{msg['timestamp']}</div>
                </div>
                """
            
            html += """
                </div>
            </body>
            </html>
            """
            
            return True, html
        
        else:
            return False, "Unbekanntes Exportformat"
        
    except Exception as e:
        print(f"Fehler beim Exportieren des Chats: {e}")
        return False, str(e)

def update_chat_title_from_first_message(session_id: int) -> bool:
    """
    Aktualisiert den Titel einer Chat-Session basierend auf der ersten Benutzernachricht.
    
    Args:
        session_id: ID der Chat-Session
        
    Returns:
        True bei Erfolg, False bei Fehler
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Erste Benutzernachricht finden
        cursor.execute(
            "SELECT content FROM chat_messages WHERE session_id = ? AND role = 'user' ORDER BY timestamp LIMIT 1",
            (session_id,)
        )
        
        result = cursor.fetchone()
        if not result:
            return False
        
        first_message = result[0]
        
        # Titel auf die ersten 30 Zeichen der Nachricht kürzen
        new_title = first_message[:30] + ("..." if len(first_message) > 30 else "")
        
        # Titel aktualisieren
        cursor.execute(
            "UPDATE chat_sessions SET title = ? WHERE id = ?",
            (new_title, session_id)
        )
        
        conn.commit()
        conn.close()
        
        return True
    except Exception as e:
        print(f"Fehler beim Aktualisieren des Chat-Titels: {e}")
        return False

# Initialisierung beim Import
init_database()

# Beispiel für die Verwendung (wird nur ausgeführt, wenn die Datei direkt ausgeführt wird)
if __name__ == "__main__":
    # Beispiel-Chat erstellen
    session_id = create_new_chat("Test-Chat")
    
    # Nachrichten hinzufügen
    add_message(session_id, "user", "Hallo, wie kann ich mein Outlook-Problem lösen?")
    add_message(session_id, "assistant", "Gerne helfe ich dir bei deinem Outlook-Problem. Kannst du mir mehr Details geben?")
    add_message(session_id, "user", "Es startet nicht mehr nach dem letzten Update.")
    
    # Titel basierend auf erster Nachricht aktualisieren
    update_chat_title_from_first_message(session_id)
    
    # Chat-Nachrichten abrufen
    messages = get_chat_messages(session_id)
    print(f"Chat-Nachrichten: {len(messages)}")
    for msg in messages:
        print(f"- {msg['role']}: {msg['content']}")
    
    # Neueste Chats abrufen
    recent_chats = get_recent_chats(5)
    print(f"Neueste Chats: {len(recent_chats)}")
    for chat in recent_chats:
        print(f"- {chat['id']}: {chat['title']} (Aktualisiert: {chat['updated_at']})")
    
    # Chat exportieren
    success, export_text = export_chat(session_id, "text")
    if success:
        print("\nChat-Export (Text):")
        print(export_text)
