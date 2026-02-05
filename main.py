import csv
from datetime import datetime
from db import connect, init_db, ensure_feeds, start_run, finish_run, get_feed_id, upsert_item
from scraper import scrape_all

FEEDS = [
    ("BBC World", "https://feeds.bbci.co.uk/news/world/rss.xml"),
    ("CNN Top", "http://rss.cnn.com/rss/edition.rss"),
    ("TechCrunch", "https://techcrunch.com/feed/"),
    ("CNBC Business", "https://www.cnbc.com/id/100003114/device/rss/rss.html"),
    ("ESPN News", "https://www.espn.com/espn/rss/news"),
]

DB_PATH = "rss.db"
CSV_PATH = "rss_items.csv"

def export_csv(conn, path: str):
    rows = conn.execute("""
      SELECT f.name as feed, i.title, i.link, i.published, i.summary, i.fetched_at
      FROM items i
      JOIN feeds f ON f.id = i.feed_id
      ORDER BY COALESCE(i.published, i.fetched_at) DESC
    """).fetchall()

    with open(path, "w", newline="", encoding="utf-8") as fp:
        w = csv.writer(fp)
        w.writerow(["feed", "title", "link", "published", "summary", "fetched_at"])
        w.writerows(rows)

def search_fts(conn, query: str, limit: int = 10):
    # Si FTS5 no existe (tu SQLite no lo soporta), esto fallará.
    # En ese caso puedes hacer LIKE en items.title/summary.
    return conn.execute("""
      SELECT i.id, f.name, i.title, i.link
      FROM items_fts
      JOIN items i ON i.id = items_fts.rowid
      JOIN feeds f ON f.id = i.feed_id
      WHERE items_fts MATCH ?
      ORDER BY rank
      LIMIT ?
    """, (query, limit)).fetchall()

def main():
    conn = connect(DB_PATH)
    try:
        init_db(conn)
        ensure_feeds(conn, FEEDS)

        run_id = start_run(conn)

        scraped, feeds_ok, feeds_failed = scrape_all(FEEDS, delay_s=0.5)

        items_seen = 0
        items_upserted = 0

        for name, url, items, err in scraped:
            if err:
                print(f"ERROR {name}: {err}")
                continue

            feed_id = get_feed_id(conn, name, url)
            items_seen += len(items)

            with conn:
                for it in items:
                    upsert_item(conn, {
                        "feed_id": feed_id,
                        "title": it["title"],
                        "link": it["link"],
                        "published": it["published"],
                        "summary": it["summary"],
                        "fetched_at": it["fetched_at"],
                    })
                    items_upserted += 1

            print(f"OK {name}: {len(items)} items")

        export_csv(conn, CSV_PATH)

        total = conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]
        finish_run(
            conn,
            run_id,
            feeds_ok=feeds_ok,
            feeds_failed=feeds_failed,
            items_seen=items_seen,
            items_upserted=items_upserted,
            error=None,
        )

        print("\n--- RESUMEN ---")
        print(f"DB: {DB_PATH}")
        print(f"CSV: {CSV_PATH}")
        print(f"Items totales en DB: {total}")
        print(f"Run ID: {run_id}")
        print(f"Feeds OK: {feeds_ok} | Feeds Failed: {feeds_failed}")

        # Demo de búsqueda (si FTS5 está disponible)
        try:
            q = "technology OR startup"
            hits = search_fts(conn, q, limit=5)
            print(f"\nFTS demo (query: {q})")
            for _id, feed, title, link in hits:
                print(f"- [{feed}] {title} -> {link}")
        except Exception as ex:
            print("\nFTS no disponible en este SQLite (o falló la query).")
            print("Tip: usa LIKE en items.title/summary o instala SQLite con FTS5.")
            # Ejemplo LIKE:
            like_hits = conn.execute("""
              SELECT f.name, i.title, i.link
              FROM items i JOIN feeds f ON f.id=i.feed_id
              WHERE i.title LIKE ? OR i.summary LIKE ?
              ORDER BY COALESCE(i.published, i.fetched_at) DESC
              LIMIT 5
            """, ("%technology%", "%technology%")).fetchall()
            for feed, title, link in like_hits:
                print(f"- [{feed}] {title} -> {link}")

    finally:
        conn.close()

if __name__ == "__main__":
    main()
