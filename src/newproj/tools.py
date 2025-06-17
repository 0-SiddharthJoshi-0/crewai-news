from datetime import datetime
import requests
from typing import List, Dict
import feedparser
import os
from dotenv import load_dotenv

load_dotenv()

class NewsTools:
    def __init__(self):
        self.newsapi_key = os.getenv('NEWS_API_KEY')
        if not self.newsapi_key:
            raise ValueError("NEWS_API_KEY environment variable is not set")

    def get_current_date(self) -> str:
        """Get the current date in a formatted string"""
        return datetime.now().strftime("%B %d, %Y")

    def fetch_newsapi_articles(self, category: str, country: str = None) -> List[Dict]:
        """Fetch current news from NewsAPI"""
        base_url = "https://newsapi.org/v2/top-headlines"
        params = {
            'apiKey': self.newsapi_key,
            'category': category,
            'language': 'en',
            'pageSize': 5
        }
        if country:
            params['country'] = country

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            articles = response.json().get('articles', [])
            
            # Filter for articles from the last 24 hours
            current_time = datetime.now()
            filtered_articles = []
            for article in articles:
                if article.get('publishedAt'):
                    pub_date = datetime.fromisoformat(article['publishedAt'].replace('Z', '+00:00'))
                    if (current_time - pub_date).total_seconds() <= 86400:  # 24 hours in seconds
                        filtered_articles.append({
                            'title': article['title'],
                            'source': article['source']['name'],
                            'url': article['url'],
                            'description': article['description'],
                            'publishedAt': article['publishedAt']
                        })
            return filtered_articles
        except Exception as e:
            print(f"Error fetching news from NewsAPI: {e}")
            return []

    def fetch_google_news(self, query: str) -> List[Dict]:
        """Fetch current news from Google News RSS"""
        try:
            # Format the query for Google News RSS
            formatted_query = query.replace(' ', '+')
            url = f"https://news.google.com/rss/search?q={formatted_query}&hl=en-US&gl=US&ceid=US:en"
            
            feed = feedparser.parse(url)
            current_time = datetime.now()
            articles = []
            
            for entry in feed.entries[:5]:  # Get top 5 articles
                if hasattr(entry, 'published'):
                    pub_date = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %Z')
                    if (current_time - pub_date).total_seconds() <= 86400:  # 24 hours
                        articles.append({
                            'title': entry.title,
                            'source': entry.source.title,
                            'url': entry.link,
                            'description': entry.description if hasattr(entry, 'description') else '',
                            'publishedAt': entry.published
                        })
            return articles
        except Exception as e:
            print(f"Error fetching news from Google News: {e}")
            return []

    def get_indian_news(self) -> List[Dict]:
        """Get current Indian news"""
        # Try NewsAPI first
        articles = self.fetch_newsapi_articles('general', 'in')
        
        # If not enough articles, supplement with Google News
        if len(articles) < 5:
            google_articles = self.fetch_google_news('India news')
            # Add only unique articles
            existing_urls = {article['url'] for article in articles}
            for article in google_articles:
                if article['url'] not in existing_urls and len(articles) < 5:
                    articles.append(article)
        
        return articles[:5]  # Return top 5 articles

    def get_tech_news(self) -> List[Dict]:
        """Get current technology news"""
        # Try NewsAPI first
        articles = self.fetch_newsapi_articles('technology')
        
        # If not enough articles, supplement with Google News
        if len(articles) < 5:
            google_articles = self.fetch_google_news('technology news')
            # Add only unique articles
            existing_urls = {article['url'] for article in articles}
            for article in google_articles:
                if article['url'] not in existing_urls and len(articles) < 5:
                    articles.append(article)
        
        return articles[:5]  # Return top 5 articles 