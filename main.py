import argparse
import os
from dotenv import load_dotenv
from scraper import fetch_headlines
from generator import generate_story
from publisher import publish_to_wordpress

import json

HISTORY_FILE = "history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return set(json.load(f))
        except:
            return set()
    return set()

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(list(history), f)

from personalities import PERSONALITIES

def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Gravity Storybuilder: Scrape news, generate stories, and publish.")
    parser.add_argument("--personality", type=str, choices=list(PERSONALITIES.keys()), default='alice', help="The personality to use for generation and publishing.")
    parser.add_argument("--dry-run", action="store_true", help="Generate story but do not publish to WordPress.")
    
    args = parser.parse_args()
    
    personality_config = PERSONALITIES[args.personality]
    
    print(f"--- Starting Gravity Storybuilder (Personality: {args.personality.capitalize()}) ---")
    
    # Load credentials for this personality
    wp_user = os.getenv(personality_config['env_user_key'])
    wp_pass = os.getenv(personality_config['env_pass_key'])
    
    if not args.dry_run and not (wp_user and wp_pass):
        print(f"Error: Credentials for {args.personality} not found in environment variables.")
        print(f"Expected {personality_config['env_user_key']} and {personality_config['env_pass_key']}.")
        return

    # Load history
    history = load_history()
    print(f"Loaded {len(history)} previously processed headlines.")
    
    # 1. Scrape
    print("Step 1: Scraping headlines...")
    headlines = fetch_headlines()
    if not headlines:
        print("No headlines found. Exiting.")
        return
    print(f"Found {len(headlines)} headlines.")
    
    # 2. Generate and Publish
    print(f"Step 2: Generating and Publishing stories...")
    
    new_stories_count = 0
    
    for i, headline in enumerate(headlines, 1):
        if headline in history:
            print(f"Skipping duplicate: {headline[:50]}...")
            continue
            
        print(f"\n--- Processing Headline {i}/{len(headlines)}: {headline[:50]}... ---")
        
        # Pass the personality's prompt modifier
        title, content = generate_story(headline, personality_config['prompt_modifier'])
        
        if title == "Error":
            print(f"Error generating story: {content}")
            continue
            
        print(f"Generated Title: {title}")
        print(f"Generated story length: {len(content)} chars")
        
        # 3. Publish
        if args.dry_run:
            print("Dry run enabled. Skipping publication.")
            print(f"Content Preview: {content[:200]}...")
        else:
            print(f"Publishing to WordPress as {args.personality}...")
            result = publish_to_wordpress(title, content, wp_user, wp_pass, status='draft')
            print(result)
            
            # Add to history only if published successfully (or attempted)
            history.add(headline)
            save_history(history)
            new_stories_count += 1
            
    print(f"\nDone. Processed {new_stories_count} new stories.")

if __name__ == "__main__":
    main()
