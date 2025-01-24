from fastapi import FastAPI, Request
import requests

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



# /webhook/weather
@app.post("/webhook/weather")
async def webhook(request:Request):
    try:
        body=await request.json()
        city_name=body.get("intentInfo").get("parameters").get("cityname").get("resolvedValue")
        country_name=body.get("intentInfo").get("parameters").get("cityname").get("resolvedValue")
        response_text=""
        
        try:
            url = f"https://p2pclouds.up.railway.app/v1/learn/weather?city={city_name}"
            response = requests.get(url)
            data = response.json()
            temp_c=data.get("current").get("temp_c")
            feelslike_c=data.get("current").get("feelslike_c")
            wind_kph=data.get("current").get("wind_kph")
            humidity=data.get("current").get("humidity")
            api_city_name=data.get("location").get("name")
            api_region_name=data.get("location").get("region")
            api_country_name=data.get("location").get("country")
            
            response_text=f"""
            {api_city_name}, {api_region_name}, {api_country_name}
            In {city_name} it's {temp_c}°C and feels like {feelslike_c}°C. The wind speed is {wind_kph} km/h and the humidity is {humidity}%."""
            
        except Exception as e:
            response_text=f"Something went wrong while getting weather details of {city_name}"
            
        response = {
            "fulfillmentResponse": {
                "messages": [
                    {
                        "text": {
                            "text": [response_text]
                        }
                    }
                ]
            },
        }
        # Return the response
        return response
    except Exception as e:
        print(e)
        return { "fulfillmentResponse": {
                "messages": [
                    {
                        "text": {
                            "text": ["Something went wrong"]
                        }
                    }
                ]
            }}
