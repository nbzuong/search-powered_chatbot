from openai import OpenAI

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
        "Provide a google search term based on search query provided below in 3-4 words"
    )
    search_term = response(prompt, search_query)
    return search_term


def summarize_content(content, search_term, character_limit=500):
    prompt = (
        f"You are an AI assistant tasked with summarizing content relevant to '{search_term}'."
        f"Please provide a concise summary in {character_limit} characters or less."
    )
    summarized_content = response(prompt, content)
    return summarized_content

