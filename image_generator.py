import os
from openai import OpenAI

def generate_image(prompt: str) -> str:
    """
    Generates an image using OpenAI's DALL-E 3 model.
    
    Args:
        prompt: The text prompt for the image.
        
    Returns:
        The URL of the generated image, or None if failed.
    """
    api_key = os.getenv("AI_API_KEY")
    base_url = os.getenv("AI_BASE_URL", "https://api.openai.com/v1")
    
    if not api_key:
        print("Error: AI_API_KEY not set.")
        return None
        
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1792x1024", # Wide format
            quality="standard",
            n=1,
        )
        
        return response.data[0].url
        
    except Exception as e:
        print(f"Error generating image: {e}")
        return None
