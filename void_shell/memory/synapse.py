import sqlite3
import os
import json
from typing import List, Dict, Any
from datetime import datetime
from void_shell.utils.paths import MEMORY_DB

class SynapseMemory:
    """
    Synapse: The Long-Term Intelligence Persistence Layer for VOID-SHELL.
    """
    def __init__(self, db_path: str = None):
        self.db_path = db_path or str(MEMORY_DB)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS commands (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    command TEXT,
                    exit_code INTEGER,
                    duration REAL,
                    output_summary TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS intelligence (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    type TEXT,
                    target TEXT,
                    data TEXT,
                    source_command_id INTEGER,
                    FOREIGN KEY(source_command_id) REFERENCES commands(id)
                )
            """)
            conn.commit()

    def store_command(self, command: str, exit_code: int, duration: float, summary: str = "") -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO commands (timestamp, command, exit_code, duration, output_summary) VALUES (?, ?, ?, ?, ?)",
                (datetime.now().isoformat(), command, exit_code, duration, summary)
            )
            conn.commit()
            return cursor.lastrowid

    def store_finding(self, finding_type: str, target: str, data: Dict[str, Any], command_id: int = None):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO intelligence (timestamp, type, target, data, source_command_id) VALUES (?, ?, ?, ?, ?)",
                (datetime.now().isoformat(), finding_type, target, json.dumps(data), command_id)
            )
            conn.commit()

    def query_recent_context(self, limit: int = 5) -> str:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT command, exit_code FROM commands ORDER BY id DESC LIMIT ?", (limit,))
                rows = cursor.fetchall()
                return "\n".join([f"Cmd: {r[0]} (Exit: {r[1]})" for r in rows])
        except:
            return ""
