import os
import requests
import feedparser   # kept for potential fallback, but not used in fetch_news below
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# CORRECT: read the variable NAME, not the key value itself
GROQ_API_KEY = os.getenv("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")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")   # you must add this to your .env

USER_INTERESTS = ["Artificial Intelligence", "Technology", "Startups", "Programming"]
MAX_ARTICLES = 5


def fetch_news():
    """Fetch news using GNews API (requires GNEWS_API_KEY in .env)."""
    if not GNEWS_API_KEY:
        print("❌ GNEWS_API_KEY missing. Get one from https://gnews.io and add to .env")
        return []

    articles = []
    for interest in USER_INTERESTS:
        url = f"https://gnews.io/api/v4/search?q={interest}&lang=en&country=us&max=5&apikey={GNEWS_API_KEY}"
        try:
            resp = requests.get(url, timeout=10)
            data = resp.json()
            for article in data.get("articles", []):
                articles.append({
                    "title": article.get("title", "No title"),
                    "description": article.get("description", "No description"),
                    "url": article.get("url", "#")
                })
            if len(articles) >= MAX_ARTICLES:
                break
        except Exception as e:
            print(f"❌ Error fetching {interest}: {e}")
    return articles[:MAX_ARTICLES]


def build_prompt(articles):
    content = ""
    for i, a in enumerate(articles, 1):
        content += f"\nArticle {i}:\nTitle: {a['title']}\nDescription: {a['description']}\nLink: {a['url']}\n"
    return f"""You are a newsletter writer. Create a clean, engaging newsletter from these articles.
- Keep it short
- Use bullet points
- Add a catchy title
- Group similar topics

Articles:{content}"""


def generate_newsletter(client, prompt):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful newsletter assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"❌ Error generating newsletter: {e}")
        return None


def main():
    if not GROQ_API_KEY:
        print("❌ Missing GROQ_API_KEY. Set it in .env file.")
        return
    if not GNEWS_API_KEY:
        print("❌ Missing GNEWS_API_KEY. Get one from https://gnews.io")
        return

    client = Groq(api_key=GROQ_API_KEY)
    print("📰 Fetching latest articles...")
    articles = fetch_news()

    if not articles:
        print("❌ No articles found.")
        return

    print(f"✅ Found {len(articles)} articles. Generating newsletter...\n")
    prompt = build_prompt(articles)
    newsletter = generate_newsletter(client, prompt)

    if newsletter:
        print("====== 📰 YOUR NEWSLETTER ======\n")
        print(newsletter)
    else:
        print("❌ Failed to generate newsletter.")


if __name__ == "__main__":
    main()
