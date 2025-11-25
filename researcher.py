import os
import json
from openai import OpenAI
from ddgs import DDGS
from typing import List, Dict, Tuple

def analyze_headline(headline: str, personality_context: str) -> Tuple[str, List[str]]:
    """
    Analyzes a headline to derive a thesis and research points.
    
    Args:
        headline: The news headline.
        personality_context: The personality style to influence the thesis.
        
    Returns:
        A tuple containing (thesis_statement, list_of_search_queries).
    """
    api_key = os.getenv("AI_API_KEY")
    base_url = os.getenv("AI_BASE_URL", "https://api.openai.com/v1")
    
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    system_prompt = "You are a research assistant. Your goal is to analyze news headlines and plan a research strategy."
    
    user_prompt = f"""
    Headline: "{headline}"
    
    Personality Context: {personality_context}
    
    Task:
    1. Derive a thesis statement about this headline that aligns with the personality context.
    2. Identify 3 distinct points or questions that need to be researched to support this thesis.
    3. Convert these points into specific search queries.
    
    Output Format (JSON):
    {{
        "thesis": "The thesis statement...",
        "queries": ["query 1", "query 2", "query 3"]
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
        )
        
        data = json.loads(response.choices[0].message.content)
        return data.get("thesis", ""), data.get("queries", [])
        
    except Exception as e:
        print(f"Error analyzing headline: {e}")
        return "", []

def perform_research(queries: List[str]) -> List[Dict]:
    """
    Performs web searches for the given queries.
    
    Args:
        queries: List of search query strings.
        
    Returns:
        List of dictionaries containing source info (title, url, snippet).
    """
    results = []
    with DDGS() as ddgs:
        for query in queries:
            print(f"  - Searching for: {query}")
            try:
                # Get top 2 results per query to keep it focused
                search_results = list(ddgs.text(query, max_results=2))
                for res in search_results:
                    results.append({
                        "query": query,
                        "title": res.get("title"),
                        "url": res.get("href"),
                        "snippet": res.get("body")
                    })
            except Exception as e:
                print(f"    Error searching for '{query}': {e}")
                
    return results

def format_citations(research_results: List[Dict]) -> str:
    """
    Formats research results into a string with MLA-style citations.
    
    Args:
        research_results: List of research result dictionaries.
        
    Returns:
        A formatted string containing the research summary and citations.
    """
    if not research_results:
        return "No research data available."
        
    formatted_text = "RESEARCH DATA:\n\n"
    
    # Group by query for readability in the prompt
    for i, result in enumerate(research_results, 1):
        formatted_text += f"Source {i}:\n"
        formatted_text += f"Title: {result['title']}\n"
        formatted_text += f"URL: {result['url']}\n"
        formatted_text += f"Snippet: {result['snippet']}\n"
        # MLA-ish citation (simplified for the generator to use)
        formatted_text += f"MLA Citation: {result['title']}. {result['url']}. Accessed via Web Search.\n\n"
        
    return formatted_text
