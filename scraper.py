import feedparser
from typing import List

DEFAULT_SOURCES = [
    "http://feeds.bbci.co.uk/news/rss.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "https://www.theguardian.com/world/rss",
]

def fetch_headlines(sources: List[str] = None) -> List[str]:
    """
    Fetches headlines from a list of RSS feed URLs.
    
    Args:
        sources: A list of RSS feed URLs. If None, uses DEFAULT_SOURCES.
        
    Returns:
        A list of headline strings.
    """
    if sources is None:
        sources = DEFAULT_SOURCES
        
    headlines = []
    print(f"Fetching headlines from {len(sources)} sources...")
    
    for source in sources:
        try:
            feed = feedparser.parse(source)
            if feed.bozo:
                print(f"Warning: Issue parsing feed {source}: {feed.bozo_exception}")
                continue
                
            # Get top 5 headlines from each source to avoid overwhelming the context [:5]
            # lowering to 2 headlines for each source as 15 is a lot [:2]
            for entry in feed.entries[:2]:
                headlines.append(entry.title)
                
        except Exception as e:
            print(f"Error fetching from {source}: {e}")
            
    return headlines
