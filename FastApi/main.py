from fastapi import FastAPI, Request

app = FastAPI()


# /webhook
@app.post("/webhook")
async def webhook(request:Request):
    body=await request.json()
    
    intent_name=body.get("queryResult").get("intent").get("displayName")
    print(intent_name)
    variable_name=body.get("queryResult").get("parameters").get("processor_name")
    context_name=body.get("session")+"/contexts/proccesor_info"
    response={
        "fulfillmentMessages":[
            {
                "text":{
                    "text":[
                        "Yes Server is Available"
                    ]
                }
            }
        ],
        "outputContexts": [
            {
                "name": context_name, 
                "lifespanCount": 5,  
                "parameters": {
                    "processor_name": variable_name,
                    "processor_price":20
                }
            }
        ]
    }
    # Return the response
    return response