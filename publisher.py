import os
import requests
import base64

def upload_media(image_url: str, wp_user: str, wp_app_password: str) -> int:
    """
    Uploads an image to WordPress Media Library from a URL.
    
    Args:
        image_url: The URL of the image to upload.
        wp_user: The WordPress username.
        wp_app_password: The WordPress application password.
        
    Returns:
        The ID of the uploaded media, or None if failed.
    """
    wp_url = os.getenv("WP_URL")
    if not all([wp_url, wp_user, wp_app_password, image_url]):
        print("Error: Missing credentials or image URL for upload.")
        return None
        
    api_url = f"{wp_url.rstrip('/')}/wp-json/wp/v2/media"
    credentials = f"{wp_user}:{wp_app_password}"
    token = base64.b64encode(credentials.encode()).decode('utf-8')
    
    headers = {
        "Authorization": f"Basic {token}",
        "Content-Disposition": "attachment; filename=generated_image.png",
        "Content-Type": "image/png"
    }
    
    try:
        # Download image first
        img_response = requests.get(image_url)
        img_response.raise_for_status()
        image_data = img_response.content
        
        # Upload to WordPress
        response = requests.post(api_url, headers=headers, data=image_data)
        response.raise_for_status()
        
        return response.json().get('id')
        
    except Exception as e:
        print(f"Error uploading media: {e}")
        return None

def publish_to_wordpress(title: str, content: str, wp_user: str, wp_app_password: str, status: str = 'draft', featured_media_id: int = None) -> str:
    """
    Publishes a post to a WordPress site via the REST API.
    
    Args:
        title: The title of the post.
        content: The HTML content of the post.
        wp_user: The WordPress username.
        wp_app_password: The WordPress application password.
        status: The status of the post ('draft', 'publish', 'private').
        featured_media_id: Optional ID of the featured image.
        
    Returns:
        The URL of the created post, or an error message.
    """
    
    wp_url = os.getenv("WP_URL")
    
    if not all([wp_url, wp_user, wp_app_password]):
        return "Error: WordPress credentials (WP_URL, wp_user, wp_app_password) are not fully set."
        
    # Ensure URL ends with /wp-json/wp/v2/posts
    api_url = f"{wp_url.rstrip('/')}/wp-json/wp/v2/posts"
    
    credentials = f"{wp_user}:{wp_app_password}"
    token = base64.b64encode(credentials.encode()).decode('utf-8')
    
    headers = {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "title": title,
        "content": content,
        "status": status
    }
    
    if featured_media_id:
        data["featured_media"] = featured_media_id
    
    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        
        post_data = response.json()
        return f"Successfully published! Link: {post_data.get('link')}"
        
    except requests.exceptions.RequestException as e:
        return f"Error publishing to WordPress: {e}. Response: {response.text if 'response' in locals() else 'None'}"
