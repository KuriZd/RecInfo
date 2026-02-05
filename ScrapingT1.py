import csv
import time
import sqlite3
from datetime import datetime
import requests
import feedparser

FEEDS = [
    ("BBC World", "https://feeds.bbci.co.uk/news/world/rss.xml"),
    ("CNN Top", "http://rss.cnn.com/rss/edition.rss"),
    ("TechCrunch", "https://techcrunch.com/feed/"),
    ("CNBC Business", "https://www.cnbc.com/id/100003114/device/rss/rss.html"),
    ("ESPN News", "https://www.espn.com/espn/rss/news"),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (RSS Scraper Practice)"
}

DB_PATH = "rss.db"
CSV_PATH = "rss_items.csv"

def fetch_feed(url: str, timeout: int = 15) -> bytes:
    r = requests.get(url, headers=HEADERS, timeout=timeout)
    r.raise_for_status()
    return r.content

def to_iso(dt_struct) -> str | None:
    if not dt_struct:
        return None
    try:
        return datetime(*dt_struct[:6]).isoformat()
    except Exception:
        return None

def init_db(conn: sqlite3.Connection):
    conn.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        feed TEXT NOT NULL,
        title TEXT,
        link TEXT NOT NULL UNIQUE,
        published TEXT,
        summary TEXT,
        fetched_at TEXT NOT NULL
    )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_items_feed ON items(feed)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_items_published ON items(published)")
    conn.commit()

def upsert_item(conn: sqlite3.Connection, item: dict):
    conn.execute("""
    INSERT INTO items (feed, title, link, published, summary, fetched_at)
    VALUES (?, ?, ?, ?, ?, ?)
    ON CONFLICT(link) DO UPDATE SET
        feed=excluded.feed,
        title=excluded.title,
        published=excluded.published,
        summary=excluded.summary,
        fetched_at=excluded.fetched_at
    """, (
        item["feed"],
        item.get("title"),
        item["link"],
        item.get("published"),
        item.get("summary"),
        item["fetched_at"],
    ))

def parse_feed(feed_name: str, url: str) -> list[dict]:
    raw = fetch_feed(url)
    parsed = feedparser.parse(raw)

    fetched_at = datetime.utcnow().isoformat()
    items = []

    for e in parsed.entries:
        link = getattr(e, "link", "") or ""
        link = link.strip()
        if not link:
            continue

        published_iso = (
            to_iso(getattr(e, "published_parsed", None))
            or to_iso(getattr(e, "updated_parsed", None))
        )

        items.append({
            "feed": feed_name,
            "title": getattr(e, "title", "").strip(),
            "link": link,
            "published": published_iso,
            "summary": getattr(e, "summary", "").strip(),
            "fetched_at": fetched_at,
        })
    return items

def export_csv(conn: sqlite3.Connection, path: str):
    rows = conn.execute("""
        SELECT feed, title, link, published, summary, fetched_at
        FROM items
        ORDER BY COALESCE(published, fetched_at) DESC
    """).fetchall()

    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["feed", "title", "link", "published", "summary", "fetched_at"])
        w.writerows(rows)

def main():
    conn = sqlite3.connect(DB_PATH)
    try:
        init_db(conn)

        inserted_total = 0
        for name, url in FEEDS:
            try:
                print(f"Leyendo: {name} -> {url}")
                items = parse_feed(name, url)
                print(f"  Parseados: {len(items)} items")

                with conn:
                    for it in items:
                        upsert_item(conn, it)

                inserted_total += len(items)
            except Exception as ex:
                print(f"  ERROR en {name}: {ex}")
            time.sleep(0.5)

        export_csv(conn, CSV_PATH)

        count = conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]
        print(f"\nDB: {DB_PATH} | Filas totales: {count}")
        print(f"CSV exportado: {CSV_PATH}")
        print(f"Items procesados esta corrida (aprox): {inserted_total}")

    finally:
        conn.close()

if __name__ == "__main__":
    main()
