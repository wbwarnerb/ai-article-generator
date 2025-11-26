import os
from openai import OpenAI
from typing import Tuple

def generate_story(headline: str, personality_context: str, thesis: str = "", research_data: str = "") -> Tuple[str, str]:
    """
    Generates a story based on a single headline, personality context, and research data.
    
    Args:
        headline: A single news headline.
        personality_context: The specific instructions for the personality.
        thesis: The derived thesis statement.
        research_data: Formatted research findings and citations.
        
    Returns:
        A tuple containing (title, content).
    """
    
    api_key = os.getenv("AI_API_KEY")
    base_url = os.getenv("AI_BASE_URL", "https://api.openai.com/v1") # Default to OpenAI, but allow override
    
    if not api_key:
        raise ValueError("AI_API_KEY environment variable is not set.")
        
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    system_prompt = "You are a creative journalist and storyteller. You write detailed, well-researched articles."
    
    user_prompt = f"""
    Here is a news headline: "{headline}"
    
    Thesis Statement:
    {thesis}
    
    Research Data:
    {research_data}
    
    Write an engaging, cohesive 800-word story based on this headline and the provided research.
    
    Personality/Style Instructions:
    {personality_context}
    
    Requirements:
     - Incorporate the research points to support the thesis.
    - Use the provided research sources.
    - Cite your sources in the text using MLA format (Author/Title).
    - Include a "Works Cited" section at the end with the full MLA citations provided in the research data. Ensure that all URLs in the Works Cited section are formatted as clickable HTML hyperlinks (<a href="...">...</a>).
    - Structure the article with multiple sections using <h2> headings.
    - Each section MUST contain multiple paragraphs (aim for 3-4 paragraphs per section) to ensure depth and readability.
    - The content should be substantial and detailed.
    
    Formatting Guidelines:
    - Use HTML tags for headings (e.g., <h2>, <h3>). 
    - DO NOT use Markdown formatting for headings (like ** or #).
    - The output should be ready to paste into a WordPress HTML editor.
    
    Output Format:
    You MUST return the response in the following format:
    TITLE: [REWRITE the title to match the personality. Do NOT use the original headline.]
    CONTENT: [Your story content here, including Works Cited]
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-5.1", # Or a configurable model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
        )
        
        full_text = response.choices[0].message.content
        
        # Parse title and content
        title = headline # Default fallback
        content = full_text
        
        if "TITLE:" in full_text and "CONTENT:" in full_text:
            parts = full_text.split("CONTENT:")
            if len(parts) == 2:
                title_part = parts[0].replace("TITLE:", "").strip()
                content_part = parts[1].strip()
                if title_part:
                    title = title_part
                if content_part:
                    content = content_part
                    
        return title, content
        
    except Exception as e:
        return "Error", f"Error generating story: {e}"
