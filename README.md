# Overview

This tool takes a news headline and generates a story based on it using an AI API. It then publishes the story to a WordPress site.  It can generate stories in different personalities (Alice, Wallace, Mike, and Mindy) and can be run in dry run mode to test without publishing. It also tracks processed headlines in history.json and skips duplicates. It uses Chat GPT to generate the story and WordPress to publish it. It is designed to be run as a cron job to generate and publish stories automatically. 

Your wordpress needs to have a user per personality with an application password. You can generate one in the WordPress admin panel under Users > Your Profile > Application Passwords. That password will be used to authenticate the requests to the WordPress REST API.

You can store your environment variables in a .env file or set them as environment variables in your system (zshrc, bashrc, etc.)

# Note 
Please use this responsibly.  This is a proof of concept. A tool of seeing what is possible with AI and scripting to create ongoing content based off a snipet of a headline.  Please be aware of any copyright issues and ethical concerns.  


# Changes
Instead of styles, I opted to use personalities: Alice, Wallace, Mike, and Mindy.

1. New Configuration
Created 
personalities.py
 which defines each personality's style, prompt modifier, and environment variable keys for credentials.
2. Updated Generator
generator.py
 now accepts a 
personality_context
 string instead of a fixed style enum. This allows for rich, custom instructions for each personality.
3. Updated Publisher
publisher.py
 now accepts wp_user and wp_app_password as arguments, allowing the application to switch credentials dynamically.
4. Updated Main Application
main.py
 now supports a --personality argument (default: alice).
It automatically loads the correct credentials (e.g., WP_USER_ALICE) and prompt instructions based on the selected personality.
5. Environment Variables
Updated 
.env.example
 to show how to configure credentials for each personality.

# How to Use
1. Configure Credentials
Update your .env file with the new keys:

WP_USER_ALICE=...
WP_PASS_ALICE=...
WP_USER_WALLACE=...
WP_PASS_WALLACE=...
etc...
2. Run with a Personality
`python main.py --personality alice`
`python main.py --personality wallace`
`python main.py --personality mike`
`python main.py --personality mindy`

# Verification Results
Unit Tests
created and ran 
test_personalities.py
 which verified:

generate_story
 correctly injects the personality's prompt modifier.
publish_to_wordpress
 correctly uses the passed credentials for authentication.
Ran 2 tests in 0.001s
OK
Manual Check
Verified that main.py --help shows the new options:

--personality {alice,wallace,mike,mindy}


# Setup

Environment Variables: Copy 
.env.example
 to .env and fill in your details:

cp .env.example .env
(see above for details)

source venv/bin/activate
`pip install -r requirements.txt`

# Usage
Run the tool using `python main.py --personality alice`.

# Personalities
alice: A positive and optimistic personality.

wallace: An analytical personality who breaks down events with rigorous logic.

mike: A financial analyst personality.

mindy: An economist personality.

derick: A conspiracy theorist personality who shades stories in dark tones of intrigue.

The above personalities are defined in personalities.py and can be modified as needed.


# Examples
Generate a positive story and publish:

`python main.py --personality alice`
Generate a conspiracy theory story (dry run):

`python main.py --personality wallace`

# Verification Results
Unit tests are used to verify the core logic. The tests mock external APIs and focus on the core functionality of the tool.

Scraping: Correctly parses RSS feeds.

Generation: Correctly constructs prompts for single headlines, handles API responses, and parses rewritten titles.

Publishing: Correctly formats requests for the WordPress REST API.

Deduplication: The tool now tracks processed headlines in history.json and skips duplicates.

Run tests with:

`python test_flow.py`