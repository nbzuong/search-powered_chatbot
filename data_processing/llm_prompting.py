from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()



def response(prompt, content):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": content}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred during completion: {e}")
        return None

def summarize_query(search_query):
    prompt = (
        "You are an AI assistant specializing in concise search optimization. Based on the search query provided, create a focused Google search term in 3–4 words that captures the main intent and ensures results are relevant to the user's specified language."
    )
    search_term = response(prompt, search_query)
    return search_term


def summarize_content(content, search_term, character_limit=500):
    prompt = (
        f"You are an AI assistant specializing in content summarization for quick reference. Based on the topic '{search_term}', write a clear, engaging, and contextually relevant summary of the content in {character_limit} characters or less, ensuring it matches the user's specified language."
    )
    summarized_content = response(prompt, content)
    return summarized_content

