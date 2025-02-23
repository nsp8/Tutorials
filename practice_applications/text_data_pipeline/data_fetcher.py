from os import getenv
from dotenv import load_dotenv
import newsapi
from newsapi.newsapi_exception import NewsAPIException

load_dotenv()


class NewsDataExtractor:
    def __init__(self):
        self.api_client = newsapi.NewsApiClient(api_key=getenv("NEWS_API_KEY"))

    def fetch_news_articles(
        self, query: str | None, source: str | None = None
    ) -> dict | None:
        try:
            all_articles = self.api_client.get_everything(q=query, sources=source)
        except NewsAPIException as news_e:
            print(f"Encountered: {news_e}")
            return None
        else:
            return all_articles
