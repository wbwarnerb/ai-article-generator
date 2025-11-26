import argparse
import os
from dotenv import load_dotenv
from personalities import PERSONALITIES
from image_generator import generate_image
from publisher import upload_media, publish_to_wordpress

def test_image_upload():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Test Image Upload for a Personality")
    parser.add_argument("--personality", type=str, choices=list(PERSONALITIES.keys()), required=True, help="The personality to test.")
    parser.add_argument("--prompt", type=str, default="A futuristic city skyline at sunset, synthwave style", help="Prompt for image generation.")
    parser.add_argument("--skip-gen", action="store_true", help="Skip generation and use a dummy URL (for testing upload only).")
    
    args = parser.parse_args()
    
    personality_config = PERSONALITIES[args.personality]
    print(f"--- Testing Image Upload for {args.personality.capitalize()} ---")
    
    # Load credentials
    wp_user = os.getenv(personality_config['env_user_key'])
    wp_pass = os.getenv(personality_config['env_pass_key'])
    
    if not (wp_user and wp_pass):
        print(f"Error: Credentials for {args.personality} not found.")
        return

    # 1. Generate Image
    image_url = None
    if args.skip_gen:
        print("Skipping generation. Using dummy URL.")
        image_url = "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png" # Google Logo
    else:
        print(f"Generating image with prompt: '{args.prompt}'...")
        image_url = generate_image(args.prompt)
    
    if not image_url:
        print("Failed to get image URL.")
        return
        
    print(f"Image URL: {image_url}")
    
    # 2. Upload Image
    print("Uploading image to WordPress...")
    media_id = upload_media(image_url, wp_user, wp_pass)
    
    if not media_id:
        print("Failed to upload image.")
        return
        
    print(f"Image uploaded successfully. Media ID: {media_id}")
    
    # 3. Create Dummy Post
    print("Creating dummy post with featured image...")
    title = f"Test Image Upload - {args.personality.capitalize()}"
    content = f"<p>This is a test post to verify image upload for {args.personality}.</p>"
    
    result = publish_to_wordpress(title, content, wp_user, wp_pass, status='draft', featured_media_id=media_id)
    print(result)

if __name__ == "__main__":
    test_image_upload()
