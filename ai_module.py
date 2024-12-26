import openai
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

openai.api_key = "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"

def analyze_scraped_data(data):
    prompt = f"Summarize the following scraped data:\n{data}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def recommend_program(user_input):
    data = pd.DataFrame({
        'name': ['Web App Program', 'Mobile Bug Bounty', 'Cloud Security Program'],
        'description': ['Find bugs in web apps', 'Hunt vulnerabilities in mobile apps', 'Test cloud services']
    })

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(data['description'])
    user_query = tfidf.transform([user_input])
    similarities = cosine_similarity(user_query, tfidf_matrix)
    recommended = data.iloc[similarities[0].argmax()]
    return f"Recommended Program:\nName: {recommended['name']}\nDescription: {recommended['description']}"

def generate_report(data):
    prompt = f"Generate a detailed report based on the following data:\n{data}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500
    )
    return response.choices[0].text.strip()

def extract_keywords(data):
    prompt = f"Extract the most important keywords from the following data:\n{data}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50
    )
    return response.choices[0].text.strip()

def translate_text(text, target_language):
    prompt = f"Translate the following text to {target_language}:\n{text}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()
