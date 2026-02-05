import time
from datetime import datetime
import requests
import feedparser

HEADERS = {"User-Agent": "Mozilla/5.0 (RSS Scraper Practice)"}

def fetch_feed(url: str, timeout: int = 15) -> bytes:
    r = requests.get(url, headers=HEADERS, timeout=timeout)
    r.raise_for_status()
    return r.content

def to_iso(dt_struct):
    if not dt_struct:
        return None
    try:
        return datetime(*dt_struct[:6]).isoformat()
    except Exception:
        return None

def parse_entries(feed_name: str, url: str) -> list[dict]:
    raw = fetch_feed(url)
    parsed = feedparser.parse(raw)

    fetched_at = datetime.utcnow().isoformat()
    items = []

    for e in parsed.entries:
        link = (getattr(e, "link", "") or "").strip()
        if not link:
            continue

        published = (
            to_iso(getattr(e, "published_parsed", None))
            or to_iso(getattr(e, "updated_parsed", None))
        )

        items.append({
            "feed_name": feed_name,
            "feed_url": url,
            "title": (getattr(e, "title", "") or "").strip(),
            "link": link,
            "published": published,
            "summary": (getattr(e, "summary", "") or "").strip(),
            "fetched_at": fetched_at,
        })

    return items

def scrape_all(feeds: list[tuple[str, str]], delay_s: float = 0.5):
    results = []
    ok = 0
    failed = 0
    for name, url in feeds:
        try:
            items = parse_entries(name, url)
            results.append((name, url, items, None))
            ok += 1
        except Exception as ex:
            results.append((name, url, [], str(ex)))
            failed += 1
        time.sleep(delay_s)
    return results, ok, failed
