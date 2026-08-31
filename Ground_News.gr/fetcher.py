import re
import requests
from config import NEWS_API_KEY, NEWS_API_URL, GREEK_STOP_WORDS

def extract_key_words(user_sentence: str) -> str:
    """Strips punctuation and stop words while preserving whatever accents the user typed."""

    cleaned_input = re.sub(r"[^\w\s]", "", user_sentence.lower())
    words = cleaned_input.split()

    keywords = [word for word in words if word not in GREEK_STOP_WORDS and len(word) > 2]

    return ' '.join(keywords)  


def clean_article_text(raw_text):
    '''Takes raw, messy text straight from the API or news site and strips out unwanted noise like HTML tags (<p>, br),
      extra whitespace, and API truncation markers (like [+1200 chars]).'''

    if not raw_text:
        return ''
    
    text = re.sub(r'<[^>]+>', '', raw_text)
    text = re.sub(r'\[\+\d+\s+chars\]', '', text)
    
    return ' '.join(text.split())


def fetch_greek_news(user_sentence: str) -> list[dict]:
    ''' Calls extract_keywords(), sends the result to the News API filtered for Greek sources,
      handles potential HTTP errors, and returns structured raw article data.'''

    query = extract_key_words(user_sentence)

    if not query:
        query = user_sentence

    params = {
        'q': query,
        'language': 'el',
        'sortby': 'publishedAt',
        'apiKey': NEWS_API_KEY 
    }

    try: 
        response = requests.get(NEWS_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        articles = data.get('articles', [])
        cleaned_articles = []

        for article in articles:
            cleaned_articles.append({
                "title": clean_article_text(article.get("title")),
                "source": article.get("source", {}).get("name", "Unknown"),
                "url": article.get("url"),
                "description": clean_article_text(article.get("description")),
                "content": clean_article_text(article.get("content")),
                "published_at": article.get("publishedAt"),
            })

        return cleaned_articles

    except requests.exceptions.RequestException as e:
        print(f'Error fetching news: {e}')
        return []
