import sqlite3
import datetime
from typing import List, Dict

DB_PATH = "polytrader.db"

class Database:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    condition_id TEXT,
                    strategy TEXT,
                    action TEXT,
                    token_id TEXT,
                    price REAL,
                    size_usd REAL,
                    edge REAL,
                    pnl_usd REAL DEFAULT 0.0,
                    paper_trade INTEGER
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS daily_stats (
                    date TEXT PRIMARY KEY,
                    total_trades INTEGER,
                    pnl_usd REAL,
                    win_rate REAL
                )
            """)
            conn.commit()

    def log_trade(self, condition_id: str, strategy: str, action: str, token_id: str, price: float, size_usd: float, edge: float, paper: bool = True):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO trades (timestamp, condition_id, strategy, action, token_id, price, size_usd, edge, paper_trade)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                datetime.datetime.utcnow().isoformat(),
                condition_id,
                strategy,
                action,
                token_id,
                price,
                size_usd,
                edge,
                1 if paper else 0
            ))
            conn.commit()

    def get_recent_trades(self, limit: int = 20) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM trades ORDER BY id DESC LIMIT ?", (limit,))
            return [dict(row) for row in cursor.fetchall()]
