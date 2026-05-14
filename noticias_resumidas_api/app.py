from flask import Flask, render_template
import requests
import os
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime

load_dotenv(r'C:\Users\mayhi\PycharmProjects\noticias_resumidas_api\.env')

API_KEY = os.getenv('API_KEY')
news_key = os.getenv('news_api_key')
groq_key = os.getenv('groq_api_key')

app = Flask(__name__)

@app.route("/")
def index():
    noticias = []
    resposta = requests.get('https://newsapi.org/v2/top-headlines',
                            params={'apiKey': news_key, 'country': 'us'})
    cliente = OpenAI(
        api_key=groq_key,
        base_url='https://api.groq.com/openai/v1'
    )

    for news in resposta.json()['articles']:
        if news['description'] is None:
            continue
        resultado = cliente.chat.completions.create(
            model='llama-3.1-8b-instant',
            messages=[
                {'role': 'system',
                 'content': 'Você é um assistente que resume notícias. Responda SEMPRE em português do Brasil, sem exceções.'},
                {'role': 'user', 'content': f'Resuma em 4 linhas: {news["title"]} - {news["description"]}'}
            ]
        )
        noticias.append({ #adiciona a próxima notícia no fim da lista "notícias"
            'titulo': news['title'],
            'resumo': resultado.choices[0].message.content,
            'fonte': news['source']['name'],
            'data': datetime.strptime(news['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').strftime('%d/%m/%Y %H:%M'),
            'url': news['url']
        })

    return render_template('index.html', noticias=noticias)
if __name__ == "__main__":
    app.run(debug=True)
