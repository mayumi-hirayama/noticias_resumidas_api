# News Summarizer com IA

Aplicação em Python que busca as principais notícias do dia via NewsAPI e utiliza o modelo LLaMA 3 (Groq) para gerar resumos automáticos em português.

## Tecnologias utilizadas

- **Python**
- **NewsAPI** — coleta de notícias em tempo real
- **Groq API (LLaMA 3)** — resumo das notícias com IA
- **python-dotenv** — gerenciamento seguro de chaves de API

## Como usar

1. Clone o repositório
2. Instale as dependências:
```bash
pip install requests openai python-dotenv
```
3. Crie um arquivo `.env` na pasta do projeto com suas chaves:
```
news_api_key=sua_chave_aqui
groq_api_key=sua_chave_aqui
```
4. Execute o arquivo principal:
```bash
python noticias_resumidas_api.py
```

## Observação

O arquivo `.env` não está incluído no repositório por segurança. Você precisará criar o seu próprio com as chaves obtidas em:
- [newsapi.org](https://newsapi.org)
- [console.groq.com](https://console.groq.com)
