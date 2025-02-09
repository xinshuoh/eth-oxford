import os
import time
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")
model = "mistral-large-latest"


def summarize_text(conversation_text):

    client = Mistral(api_key=api_key)
    prompt = f"""
    Summarize the following Twitter debate in a few sentences, highlighting key arguments from both sides:
    
    {conversation_text}
    
    Summary:
    """

    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are an AI assistant summarizing debates.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    time.sleep(1.5)

    summary = chat_response.choices[0].message.content.strip()
    return summary
