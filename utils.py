import feedparser

def fetch_rss(url):
    try:
        feed = feedparser.parse(url)
        entries = feed.entries
        return [{"title": entry.title, "link": entry.link} for entry in entries]
    except Exception as e:
        return f"Error fetching RSS feed: {e}"
