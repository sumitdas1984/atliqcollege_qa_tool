from openai import OpenAI
import os
import json


def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

response_message = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": "What is the weather like in boston?"}
                ],
                functions=[
                    {
                        "name": "get_current_weather",
                        "description": "Get the current weather in a given location",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "The city and state, e.g. San Francisco, CA",
                                },
                                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                            },
                            "required": ["location"]
                        }
                    }
                ]
            )

if response_message.choices[0].message.function_call:
    function_name = response_message.choices[0].message.function_call.name
    function_args = json.loads(response_message.choices[0].message.function_call.arguments)

    available_functions = {
        'get_current_weather': get_current_weather
    }

    function_to_call = available_functions[function_name]

    function_response = function_to_call(
        location=function_args.get("location"),
        unit=function_args.get("unit")
    )
    print(function_response)
