import requests  
import json
from langchain_ollama import ChatOllama

GEMINI_API_KEY="AIzaSyAYWBwTfL3qwRhgo4IXMPyVSwdh1USBLCI"
GEMINI_URL=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

def book_content_generation(topic, raw_text):
    prompt = f"""
    Process the following raw information into a structured book format on '{topic}'.
    Ensure it includes:
    - An introduction
    - At least 3 sections with sub-sections(if any)
    - Ad real easy examples
    - A conclusion
    - also remove pledge and humanize it.

    Raw Data:
    {raw_text}
    """
    llm = ChatOllama(
    model="llama3.2",
    temperature=0,
    )
    res=llm.invoke(prompt)
    try:
        content = res.content
    except Exception as e:
        print(e)
        content ="Something went wrong"

    return content


def topic_extracter( raw_query):
    prompt = f"""
    Extract the Topic from the following sentence:

    Sentence:
    {raw_query}

    **Output:**
    * Only the topic itself. 
    * No other information or analysis.
    """

    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(GEMINI_URL, headers=headers, data=json.dumps(data))
    result = response.json()
    # Extract generated text
    try:
        topic = result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print(e)
        topic ="No Topic"

    return topic



def country_code_extracter( raw_query):
    prompt = f"""
    Extract the Country from the following sentence:

    Sentence:
    {raw_query}

    **Output:**
    * Only the Country Code. 
    * If Country not found use country code default value PK(Pakistan).
    """

    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(GEMINI_URL, headers=headers, data=json.dumps(data))
    result = response.json()
    try:
        topic = result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        topic ="PK"

    return topic


def linkedin_post_generation(trends):
    """
    Generate a LinkedIn-style post based on raw text input.
    
    Args:
        trends (str): Topic for the LinkedIn post
    Returns:
        str: Generated LinkedIn post content
    """
    
    # Construct the prompt with proper formatting and spelling
    prompt = f"""
    You are a Digital Media Marketer. Based on these current trends {trends}, choose one trend and create a professional LinkedIn-style post 
    also Optimize the content for SEO and include relevant hashtags.
    """
    
    # Prepare the API request data structure
    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    
    # Set up headers with proper content type
    headers = {
        "Content-Type": "application/json"
    }
    
    # Send request with comprehensive error handling
    try:
        response = requests.post(GEMINI_URL, headers=headers, json=data)
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Parse JSON response
        result = response.json()
        
        # Extract generated text with safe navigation
        try:
            content = result["candidates"][0]["content"]["parts"][0]["text"]
        except KeyError as e:
            print(f"Error accessing response data: {e}")
            return "Failed to generate content"
            
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error occurred: {errh}")
        return "Request failed"
    except requests.exceptions.ConnectionError as errc:
        print(f"Error connecting to API: {errc}")
        return "Connection failed"
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error occurred: {errt}")
        return "Request timed out"
    except requests.exceptions.RequestException as err:
        print(f"Something went wrong: {err}")
        return "An error occurred"
    
    return content
