import requests
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(r'C:\Users\mayhi\PycharmProjects\noticias_resumidas_api\.env')

API_KEY = os.getenv('API_KEY')
news_key = os.getenv('news_api_key')
groq_key = os.getenv('groq_api_key')

resposta = requests.get('https://newsapi.org/v2/top-headlines', params={'apiKey': news_key, 'country': 'us'})
cliente = OpenAI(
    api_key=groq_key,
    base_url='https://api.groq.com/openai/v1'
)

for news in resposta.json()['articles']:
    if news['description'] is None:
        continue
    print(news['title'])
    print(news['description'])
    resultado = cliente.chat.completions.create(
        model='llama-3.1-8b-instant',
        messages=[
            {'role': 'system', 'content': 'Você é um assistente que resume notícias. Responda SEMPRE em português do Brasil, sem exceções.'},
            {'role': 'user', 'content': f'Resuma em 2 linhas: {news["title"]} - {news["description"]}'}
        ]
    )
    print(resultado.choices[0].message.content)