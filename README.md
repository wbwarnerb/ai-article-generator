# Overview

This tool takes a news headline and generates a story based on it using an AI API. It then publishes the story to a WordPress site.  It can generate stories in different styles (conspiracy, positive, human interest) and can be run in dry run mode to test without publishing. It also tracks processed headlines in history.json and skips duplicates. It uses Chat GPT to generate the story and WordPress to publish it. It is designed to be run as a cron job to generate and publish stories automatically. 

Your wordpress needs to have a user with an application password. You can generate one in the WordPress admin panel under Users > Your Profile > Application Passwords. That password will be used to authenticate the requests to the WordPress REST API.

You can store your environment variables in a .env file or set them as environment variables in your system (zshrc, bashrc, etc.)

# Note 
Please use this responsibly.  This is a proof of concept. A tool of seeing what is possible with AI and scripting to create ongoing content based off a snipet of a headline.  Please be aware of any copyright issues and ethical concerns.  


# Setup

Environment Variables: Copy 
.env.example
 to .env and fill in your details:

cp .env.example .env
You will need:

AI_API_KEY: Your OpenAI (or compatible) API key.
WP_URL: Your WordPress site URL.
WP_USER: Your WordPress username.
WP_APP_PASSWORD: Your WordPress Application Password (generated in WP Admin > Users > Profile).
Install Dependencies: (If not already done)

source venv/bin/activate
pip install -r requirements.txt

Usage
Run the tool using python main.py.

# Options
--style: Choose the story style. Options: conspiracy, positive, human interest. Default: positive.
--dry-run: Generate the story but do not publish to WordPress. Useful for testing.

# Examples
Generate a positive story and publish:

`python main.py --style positive`
Generate a conspiracy theory story (dry run):

`python main.py --style conspiracy --dry-run`

# Verification Results
Unit tests are used to verify the core logic. The tests mock external APIs and focus on the core functionality of the tool.

Scraping: Correctly parses RSS feeds.
Generation: Correctly constructs prompts for single headlines, handles API responses, and parses rewritten titles.
Publishing: Correctly formats requests for the WordPress REST API.
Deduplication: The tool now tracks processed headlines in history.json and skips duplicates.

Run tests with:

`python test_flow.py`