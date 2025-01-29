from fastapi import FastAPI, Request
import requests
import json
import requests  
from serpapi import GoogleSearch
import re
from fpdf import FPDF

app = FastAPI()

SERP_API_KEY="<SERP API HERE>"
GEMINI_API_KEY="<GEMINI API HERE>"
GEMINI_URL=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

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
        content = result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print(e)
        content ="Something went wrong"

    return content

def search_content(topic):
    params = {
        "q": topic,
        "api_key": SERP_API_KEY,
        "num": 10 
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    content = ""
    for item in results["organic_results"]:
        content += f"{item['title']}\n{item['snippet']}\n{item['redirect_link']}\n"
    
    return content

def clean_text(text):
    """Replace unsupported characters with ASCII equivalents."""
    replacements = {
        "\u2018": "'", "\u2019": "'",  # Smart single quotes → '
        "\u201C": '"', "\u201D": '"',  # Smart double quotes → "
        "\u2013": "-", "\u2014": "--",  # Dashes → -
        "\u2026": "..."  # Ellipsis → ...
    }
    for key, value in replacements.items():
        text = text.replace(key, value)
    
    # Remove other non-ASCII characters
    text = re.sub(r"[^\x00-\x7F]+", "", text)  
    return text

def create_pdf(book_title, book_content):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    book_title = clean_text(book_title)
    book_content = clean_text(book_content)

    pdf.cell(200, 10, book_title, ln=True, align="C")
    pdf.ln(10)  # Line break
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10, book_content)

    filename = f"{book_title.replace(' ', '_').replace('\n','')}.pdf"
    pdf.output(filename, "F")
    return filename

# /webhook
@app.post("/v1/agent/content/book")
async def webhook(request:Request):
    body=await request.json()
    query=body['text']
    extracted_topic=topic_extracter(query)
    print(extracted_topic)
    raw_data=search_content(extracted_topic)
    print(raw_data)
    content=book_content_generation(extracted_topic,raw_data)
    print(content)
    create_pdf(extracted_topic,content)
    response = {
                "fulfillmentResponse": {
                    "messages": [
                        {
                            "text": {
                                "text": ["Working"]
                            }
                        }
                    ]
                },
            }
    # Return the response
    return response
