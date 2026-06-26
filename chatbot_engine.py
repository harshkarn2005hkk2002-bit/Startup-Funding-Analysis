# chatbot_engine.py

import pandas as pd
import requests

class StartupChatbot:
    def __init__(self, df, groq_api_key=None):
        self.df = df.copy()
        self.groq_api_key = groq_api_key
        # Combine important columns
        self.df['Startup Info'] = self.df[['Startup Name', 'Industry', 'Country', 'Funding Stage']].agg(' | '.join, axis=1)

    def ask(self, question):
        # Filter relevant startups locally
        relevant_startups = self.df[self.df['Startup Info'].str.contains(question, case=False, na=False)]

        # Default answer
        answer = "Sorry, couldn't get an answer from Groq API."

        # Use Groq API if API key provided
        if self.groq_api_key:
            url = "https://api.groq.ai/v1/answers"  # Use correct Groq endpoint
            headers = {"Authorization": f"Bearer {self.groq_api_key}"}
            data = {
                "question": question,
                "context": self.df['Startup Info'].tolist()
            }
            try:
                response = requests.post(url, headers=headers, json=data, timeout=10)
                if response.status_code == 200:
                    answer = response.json().get("answer", "No answer returned by Groq API.")
                else:
                    answer = f"Groq API error {response.status_code}: {response.text}"
            except Exception as e:
                answer = f"Error calling Groq API: {e}"

        if relevant_startups.empty:
            relevant_startups = pd.DataFrame(columns=['Startup Name','Country','Industry','Funding Stage','Amount Raised (USD)'])
        return relevant_startups.head(5), answer