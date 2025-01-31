from fastapi import FastAPI, Request
from utils.search import search_content
from utils.llm import book_content_generation,topic_extracter
from utils.pdf import create_content_pdf
from utils.llm import country_code_extracter,linkedin_post_generation
from utils.search import search_google_trends

app = FastAPI()

# /webhook
@app.post("/v1/agent/content/book")
async def webhook(request:Request):
    body=await request.json()
    query=body['text']
    extracted_topic=topic_extracter(query)
    raw_data=search_content(extracted_topic)
    content=book_content_generation(extracted_topic,raw_data)
    create_content_pdf(extracted_topic,content)
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

# /webhook
@app.post("/v1/agent/linkedin/post")
async def webhook(request:Request):
    body=await request.json()
    query=body['text']
    print(query)        
    country_code=country_code_extracter(query)
    print(country_code)
    trends=search_google_trends(country_code)
    print(trends)
    post_content=linkedin_post_generation(",".join(trends))
    print(post_content)
    response = {
                "fulfillmentResponse": {
                    "messages": [
                        {
                            "text": {
                                "text": [post_content]
                            }
                        }
                    ]
                },
            }
    # Return the response
    return response



