import sqlite3
from datetime import datetime

SCHEMA_SQL = """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS feeds (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  url TEXT NOT NULL UNIQUE,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS runs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  started_at TEXT NOT NULL,
  finished_at TEXT,
  feeds_ok INTEGER NOT NULL DEFAULT 0,
  feeds_failed INTEGER NOT NULL DEFAULT 0,
  items_seen INTEGER NOT NULL DEFAULT 0,
  items_upserted INTEGER NOT NULL DEFAULT 0,
  error TEXT
);

CREATE TABLE IF NOT EXISTS items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  feed_id INTEGER NOT NULL,
  title TEXT,
  link TEXT NOT NULL UNIQUE,
  published TEXT,
  summary TEXT,
  fetched_at TEXT NOT NULL,
  FOREIGN KEY(feed_id) REFERENCES feeds(id)
);

CREATE INDEX IF NOT EXISTS idx_items_feed_id ON items(feed_id);
CREATE INDEX IF NOT EXISTS idx_items_published ON items(published);

-- FTS5 (si tu SQLite no lo soporta, fallará aquí; el código lo detecta)
CREATE VIRTUAL TABLE IF NOT EXISTS items_fts USING fts5(
  title, summary, link,
  content='items',
  content_rowid='id'
);

CREATE TRIGGER IF NOT EXISTS items_ai AFTER INSERT ON items BEGIN
  INSERT INTO items_fts(rowid, title, summary, link)
  VALUES (new.id, COALESCE(new.title,''), COALESCE(new.summary,''), COALESCE(new.link,''));
END;

CREATE TRIGGER IF NOT EXISTS items_ad AFTER DELETE ON items BEGIN
  INSERT INTO items_fts(items_fts, rowid, title, summary, link)
  VALUES ('delete', old.id, COALESCE(old.title,''), COALESCE(old.summary,''), COALESCE(old.link,''));
END;

CREATE TRIGGER IF NOT EXISTS items_au AFTER UPDATE ON items BEGIN
  INSERT INTO items_fts(items_fts, rowid, title, summary, link)
  VALUES ('delete', old.id, COALESCE(old.title,''), COALESCE(old.summary,''), COALESCE(old.link,''));
  INSERT INTO items_fts(rowid, title, summary, link)
  VALUES (new.id, COALESCE(new.title,''), COALESCE(new.summary,''), COALESCE(new.link,''));
END;
"""

def connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db(conn: sqlite3.Connection) -> None:
    try:
        conn.executescript(SCHEMA_SQL)
        conn.commit()
    except sqlite3.OperationalError as e:
        msg = str(e).lower()
        if "fts5" in msg:
            # Reintenta sin FTS si no está disponible
            conn.rollback()
            conn.executescript(_schema_without_fts())
            conn.commit()
        else:
            raise

def _schema_without_fts() -> str:
    parts = []
    for line in SCHEMA_SQL.splitlines():
        if "VIRTUAL TABLE" in line or "items_fts" in line or "TRIGGER" in line:
            continue
        parts.append(line)
    return "\n".join(parts)

def ensure_feeds(conn: sqlite3.Connection, feeds: list[tuple[str, str]]) -> None:
    now = datetime.utcnow().isoformat()
    with conn:
        for name, url in feeds:
            conn.execute(
                "INSERT OR IGNORE INTO feeds(name, url, created_at) VALUES(?,?,?)",
                (name, url, now),
            )

def start_run(conn: sqlite3.Connection) -> int:
    now = datetime.utcnow().isoformat()
    cur = conn.execute("INSERT INTO runs(started_at) VALUES(?)", (now,))
    conn.commit()
    return cur.lastrowid

def finish_run(conn: sqlite3.Connection, run_id: int, **fields) -> None:
    fields["finished_at"] = datetime.utcnow().isoformat()
    cols = ", ".join([f"{k}=?" for k in fields.keys()])
    values = list(fields.values()) + [run_id]
    conn.execute(f"UPDATE runs SET {cols} WHERE id=?", values)
    conn.commit()

def get_feed_id(conn: sqlite3.Connection, name: str, url: str) -> int:
    row = conn.execute("SELECT id FROM feeds WHERE url=?", (url,)).fetchone()
    if row:
        return row[0]
    now = datetime.utcnow().isoformat()
    cur = conn.execute(
        "INSERT INTO feeds(name, url, created_at) VALUES(?,?,?)",
        (name, url, now),
    )
    conn.commit()
    return cur.lastrowid

def upsert_item(conn: sqlite3.Connection, item: dict) -> None:
    conn.execute("""
    INSERT INTO items (feed_id, title, link, published, summary, fetched_at)
    VALUES (?, ?, ?, ?, ?, ?)
    ON CONFLICT(link) DO UPDATE SET
      feed_id=excluded.feed_id,
      title=excluded.title,
      published=excluded.published,
      summary=excluded.summary,
      fetched_at=excluded.fetched_at
    """, (
        item["feed_id"],
        item.get("title"),
        item["link"],
        item.get("published"),
        item.get("summary"),
        item["fetched_at"],
    ))
