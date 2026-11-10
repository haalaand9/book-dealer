import json
import random
import re
import urllib.parse
import urllib.request
from datetime import date, timedelta
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA_PATH = BASE / 'data' / 'purchases.json'
DATA_PATH.parent.mkdir(exist_ok=True)

AMERICAN_AUTHORS = [
    'Sarah J. Maas',
    'John Green',
    'Angie Thomas',
    'Nicola Yoon',
    'Jennifer L. Holm',
    'Becky Albertalli',
    'Adam Silvera',
    'Tiffany D. Jackson',
    'Holly Jackson',
    'Stephanie Garber',
    'Rick Riordan',
    'Karen M. McManus',
    'Colleen Hoover',
    'Sabaa Tahir',
    'Nic Stone',
    'Kwame Alexander',
    'Rebecca Stead',
    'Ariana Godoy',
    'Tracy Wolff',
    'Abby Jimenez',
]

SEARCH_TERMS = [
    'American teen fantasy',
    'American YA romance',
    'American YA thriller',
    'American teen fiction',
    'American YA contemporary',
    'American teen mystery',
]

random.seed(42)


def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def normalize_text(value):
    if value is None:
        return ''
    if isinstance(value, str):
        return re.sub(r'\s+', ' ', value).strip()
    if isinstance(value, dict):
        return normalize_text(value.get('value') or value.get('text'))
    if isinstance(value, list):
        return ' '.join(normalize_text(item) for item in value if normalize_text(item))
    return str(value)


def enrich_book(doc, index):
    title = doc.get('title') or 'Untitled'
    author = (doc.get('author_name') or ['Unknown author'])[0]
    cover_id = doc.get('cover_i')
    cover_url = f'https://covers.openlibrary.org/b/id/{cover_id}-M.jpg' if cover_id else ''
    genre = (doc.get('subject') or ['General'])[0]
    first_year = doc.get('first_publish_year') or 0

    work_key = doc.get('key')
    description = ''
    if work_key:
        try:
            work = fetch_json(f'https://openlibrary.org{work_key}.json')
            desc = work.get('description')
            description = normalize_text(desc)
            if not description:
                desc = work.get('subjects')
                description = normalize_text(desc)
        except Exception:
            description = ''

    return {
        'id': f'B{index:03d}',
        'title': title,
        'author': author,
        'genre': genre,
        'price': round(random.uniform(14.0, 26.0), 2),
        'cover': cover_url,
        'description': description[:280],
        'publishedYear': first_year,
        'isbn': (doc.get('isbn') or [''])[0],
        'subjects': (doc.get('subject') or [])[:5],
    }


def fetch_books(limit=25):
    seen = set()
    books = []

    for author in AMERICAN_AUTHORS:
        if len(books) >= limit:
            break
        query = urllib.parse.quote(f'author:"{author}" young adult')
        url = f'https://openlibrary.org/search.json?q={query}&limit=6'
        try:
            payload = fetch_json(url)
        except Exception:
            continue
        for doc in payload.get('docs', []):
            if len(books) >= limit:
                break
            title = (doc.get('title') or '').strip()
            author_name = (doc.get('author_name') or [''])[0].strip()
            key = (title, author_name)
            if not title or not author_name or key in seen:
                continue
            seen.add(key)
            books.append(enrich_book(doc, len(books) + 1))

    for term in SEARCH_TERMS:
        if len(books) >= limit:
            break
        query = urllib.parse.quote(term)
        url = f'https://openlibrary.org/search.json?q={query}&limit=12'
        try:
            payload = fetch_json(url)
        except Exception:
            continue
        for doc in payload.get('docs', []):
            if len(books) >= limit:
                break
            title = (doc.get('title') or '').strip()
            author = (doc.get('author_name') or [''])[0].strip()
            key = (title, author)
            if not title or not author or key in seen:
                continue
            seen.add(key)
            books.append(enrich_book(doc, len(books) + 1))

    while len(books) < limit:
        fallback = {
            'title': f'American Teen Favorite {len(books) + 1}',
            'author_name': [f'American Author {len(books) + 1}'],
            'cover_i': None,
            'subject': ['Young Adult'],
            'first_publish_year': 2024,
            'key': '/works/OL000000W',
        }
        books.append(enrich_book(fallback, len(books) + 1))
    return books[:limit]


def generate_purchases(books):
    today = date.today()
    purchases = []
    for book in books:
        genre = book['genre']
        popularity = {
            'mystery': 18,
            'fantasy': 17,
            'romance': 15,
            'science fiction': 16,
            'thriller': 18,
            'historical fiction': 13,
            'adventure': 14,
            'fiction': 11,
            'literary fiction': 10,
            'nonfiction': 9,
            'general': 7,
        }.get((genre or 'general').lower(), 9)

        for offset in range(5):
            day = today - timedelta(days=4 - offset)
            wave = random.randint(-4, 7)
            daily_sales = max(3, popularity + wave + (offset == 4) * 3 + (offset == 0) * 2)
            for _ in range(daily_sales):
                purchases.append({
                    'bookId': book['id'],
                    'date': day.isoformat(),
                    'quantity': 1,
                })
    return purchases


def main():
    books = fetch_books(25)
    payload = {
        'generatedAt': date.today().isoformat(),
        'windowDays': 5,
        'books': books,
        'purchases': generate_purchases(books),
    }
    DATA_PATH.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
    print(f'Fetched {len(books)} real books from OpenLibrary and saved sales data for {len(payload["purchases"])} records.')


if __name__ == '__main__':
    main()
