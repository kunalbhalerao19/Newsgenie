import feedparser

interests = ["Artificial Intelligence", "Technology"]
for interest in interests:
    query = interest.replace(" ", "+")
    url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
    print(f"Fetching: {url}")
    feed = feedparser.parse(url)
    print(f"  Entries found: {len(feed.entries)}")
    if feed.entries:
        print(f"  First title: {feed.entries[0].get('title', 'N/A')}")
    print("---")
