from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_structured_data(articles):

    structured_data = ""

    for article in articles[:5]:
        prompt = f"""
Extract structured startup funding info from this news:

Title: {article['title']}
Description: {article['description']}

Return:
Company, Sector, City, Funding Info
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        structured_data += response.choices[0].message.content + "\n\n"

    return structured_data