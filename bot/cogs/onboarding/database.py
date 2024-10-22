import sqlite3
from datetime import datetime

class OnboardingDatabase:
    def __init__(self):
        self.conn = sqlite3.connect("onboarding.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS players (
                        member_id INTEGER PRIMARY KEY, 
                        player_tag TEXT,
                        current_step INTEGER, 
                        end_time TEXT,
                        channel_id INTEGER,
                        message_id INTEGER)''')
        self.conn.commit()

    def save_player(self, member_id, player_tag, current_step, end_time, channel_id, message_id):
        self.cursor.execute('''INSERT OR REPLACE INTO players (member_id, player_tag, current_step, end_time, channel_id, message_id) 
                            VALUES (?, ?, ?, ?, ?, ?)''', 
                            (member_id, player_tag, current_step, end_time.isoformat(), channel_id, message_id))
        self.conn.commit()

    def remove_player(self, member_id):
        self.cursor.execute("DELETE FROM players WHERE member_id = ?", (member_id,))
        self.conn.commit()

    def get_all_players(self):
        self.cursor.execute("SELECT member_id, player_tag, current_step, end_time, channel_id, message_id FROM players")
        rows = self.cursor.fetchall()
        return [(row[0], row[1], row[2], datetime.fromisoformat(row[3]), row[4], row[5]) for row in rows]

    def close(self):
        self.conn.close()