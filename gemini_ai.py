from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_itinerary(destination, days, budget, interests, user_name):
    prompt = f"""
Create a {days}-day travel itinerary for {destination}.
Budget: {budget}
Interests: {interests}
Traveler name: {user_name}

IMPORTANT FORMAT (DO NOT DEVIATE):

DAY 1:
- Arrive at airport and transfer to hotel
- Morning: ...
- Afternoon: ...
- Evening: ...

DAY 2:
- Morning: ...
- Afternoon: ...
- Evening: ...

Also make sure each activity clearly mentions place names.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional travel planner."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
