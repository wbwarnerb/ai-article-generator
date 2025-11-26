PERSONALITIES = {
    "alice": {
        "style": "compassionate",
        "prompt_modifier": "Add a style of compassion to the story. Focus on the human element, empathy, and emotional connection. Be kind and understanding in the tone.",
        "env_user_key": "WP_USER_ALICE",
        "env_pass_key": "WP_PASS_ALICE",
        "rss_feeds": [
            "https://www.goodnewsnetwork.org/feed/",
            "http://feeds.bbci.co.uk/news/education/rss.xml",
            "http://feeds.bbci.co.uk/news/health/rss.xml"
        ]
    },
    "wallace": {
        "style": "analytical",
        "prompt_modifier": "Add a very detailed analysis to the story. Break down the events, causes, and effects with rigorous logic. Use data-driven language where appropriate and be extremely precise.",
        "env_user_key": "WP_USER_WALLACE",
        "env_pass_key": "WP_PASS_WALLACE",
        "rss_feeds": [
            "http://feeds.bbci.co.uk/news/technology/rss.xml",
            "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
            "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml"
        ]
    },
    "mike": {
        "style": "financial",
        "prompt_modifier": "Focus heavily on financial implications and markets. Discuss stocks, bonds, economic indicators, and how this news affects the bottom line for businesses and investors.",
        "env_user_key": "WP_USER_MIKE",
        "env_pass_key": "WP_PASS_MIKE",
        "rss_feeds": [
            "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664",
            "http://feeds.bbci.co.uk/news/business/rss.xml",
            "https://finance.yahoo.com/news/rssindex"
        ]
    },
    "mindy": {
        "style": "economist",
        "prompt_modifier": "Adopt the persona of an economist. Write to an audience of economists and financial professionals. Focus on global stability, conflict, and trade. Discuss macroeconomic trends, geopolitical ramifications, and long-term societal impact.",
        "env_user_key": "WP_USER_MINDY",
        "env_pass_key": "WP_PASS_MINDY",
        "rss_feeds": [
            "http://feeds.bbci.co.uk/news/world/rss.xml",
            "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
            "https://www.theguardian.com/world/economics/rss"
        ]
    },
    "derick": {
        "style": "conspiracy",
        "prompt_modifier": "Add a style of conspiracy and intrigue. Shade the story in dark tones, questioning official narratives and suggesting hidden agendas. Connect events to a grander, more sinister theory.",
        "env_user_key": "WP_USER_DERICK",
        "env_pass_key": "WP_PASS_DERICK",
        "rss_feeds": [
            "http://feeds.bbci.co.uk/news/world/rss.xml", # Derick finds conspiracies everywhere
            "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"
        ]
    }
}
