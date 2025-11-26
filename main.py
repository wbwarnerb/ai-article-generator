import argparse
import os
from dotenv import load_dotenv
from scraper import fetch_headlines
from generator import generate_story
from publisher import publish_to_wordpress, upload_media
from researcher import analyze_headline, perform_research, format_citations
from image_generator import generate_image

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
    rss_feeds = personality_config.get('rss_feeds')
    headlines = fetch_headlines(rss_feeds)
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
        
        # 1.1 Analyze and Research
        print(f"  - Analyzing headline for {args.personality}...")
        thesis, queries = analyze_headline(headline, personality_config['prompt_modifier'])
        print(f"  - Thesis: {thesis}")
        print(f"  - Research Queries: {queries}")
        
        research_results = []
        if queries:
            print(f"  - Performing research...")
            research_results = perform_research(queries)
            
        research_data = format_citations(research_results)
        
        # Pass the personality's prompt modifier and research data
        title, content = generate_story(headline, personality_config['prompt_modifier'], thesis, research_data)
        
        if title == "Error":
            print(f"Error generating story: {content}")
            continue
            
        print(f"Generated Title: {title}")
        print(f"Generated story length: {len(content)} chars")
        
        # 2.1 Generate Image
        print(f"  - Generating image for {args.personality}...")
        image_prompt = f"A wide cinematic image representing: {title}. Style: {personality_config['style']}. High quality, detailed."
        image_url = generate_image(image_prompt)
        
        featured_media_id = None
        if image_url:
            print(f"  - Image generated: {image_url}")
            if not args.dry_run:
                print(f"  - Uploading image to WordPress...")
                featured_media_id = upload_media(image_url, wp_user, wp_pass)
                if featured_media_id:
                    print(f"  - Image uploaded. Media ID: {featured_media_id}")
                else:
                    print(f"  - Failed to upload image.")
        else:
            print(f"  - Failed to generate image.")

        # 3. Publish
        if args.dry_run:
            print("Dry run enabled. Skipping publication.")
            print(f"Content Preview: {content[:200]}...")
            if image_url:
                print(f"Image URL: {image_url}")
        else:
            print(f"Publishing to WordPress as {args.personality}...")
            result = publish_to_wordpress(title, content, wp_user, wp_pass, status='draft', featured_media_id=featured_media_id)
            print(result)
            
            # Add to history only if published successfully (or attempted)
            history.add(headline)
            save_history(history)
            new_stories_count += 1
            
    print(f"\nDone. Processed {new_stories_count} new stories.")

if __name__ == "__main__":
    main()
