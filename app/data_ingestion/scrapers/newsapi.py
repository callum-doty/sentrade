from newsapi import NewsApiClient
import pandas as pd
import re
import os
from dotenv import load_dotenv

# TODO: Refactor path loading and API key management.
# This should ideally use app.core.config_loader or expect env vars.
# load_dotenv('/Users/ashfi/code/new_python/sentrade/token.env') # Replace with your own path
# NEWS_API = os.getenv("NEWS_API")
# newsapi = NewsApiClient(api_key=NEWS_API)


# TODO: Refactor this script to be function-based and integrate with the application's data flow.
# The current implementation with direct input and CSV output is not suitable for the main app.


def fetch_news_from_newsapi(query: str, api_key: str) -> list[dict]:
    """
    Fetches news articles from NewsAPI based on a query.
    Args:
        query (str): The search query (e.g., stock ticker or company name).
        api_key (str): The NewsAPI key.
    Returns:
        list[dict]: A list of articles, or an empty list if an error occurs.
    """
    try:
        newsapi_client = NewsApiClient(api_key=api_key)
        response = newsapi_client.get_everything(q=query)
        if response.get("status") == "ok":
            return response.get("articles", [])
        else:
            print(f"Error from NewsAPI: {response.get('message')}")
            return []
    except Exception as e:
        print(f"An error occurred while fetching news from NewsAPI: {e}")
        return []


def _process_articles_to_dataframe(articles: list[dict]):
    """Helper to process articles into a pandas DataFrame (internal use or for testing)."""
    if not articles:
        return pd.DataFrame()
    flat_df = pd.json_normalize(articles, sep="_")
    return flat_df


# Original script's direct execution logic (commented out for library use)
# if __name__ == '__main__':
#     # This section demonstrates original functionality but should not run when imported.
#     # For application use, call fetch_news_from_newsapi with parameters.
#
#     # Example of how API key might be loaded (replace with actual config loading)
#     load_dotenv() # Expects .env file in CWD or project root
#     NEWS_API_KEY = os.getenv("NEWS_API")
#
#     if not NEWS_API_KEY:
#         print("NEWS_API key not found. Please set it in your .env file.")
#     else:
#         user_input_query = input('Search stock news: ').strip()
#         if user_input_query:
#             fetched_articles = fetch_news_from_newsapi(user_input_query, NEWS_API_KEY)
#             if fetched_articles:
#                 articles_df = _process_articles_to_dataframe(fetched_articles)
#                 print(f"\nFetched {len(fetched_articles)} articles. DataFrame head:")
#                 print(articles_df.head())
#
#                 # Original CSV saving logic (for testing/standalone use)
#                 # safe_name = re.sub(r'[^A-Za-z0-9_]+', '_', user_input_query.strip())[:50]
#                 # output_filename = f'{safe_name}_newsapi_articles.csv'
#                 # articles_df.to_csv(output_filename, index=False)
#                 # print(f"\nSaved articles to {output_filename}")
#             else:
#                 print("No articles fetched.")
#         else:
#             print("No search query provided.")

# Original script content (kept for reference, to be refactored)
# newsapi = NewsApiClient(api_key=NEWS_API)
# user_input = input('Search stock news: ').strip()
# stock_news = newsapi.get_everything(q=user_input)
# flat = pd.json_normalize(stock_news['articles'], sep='_')
# safe_name = re.sub(r'[^A-Za-z0-9_]+', '_', user_input.strip())[:50]
# flat.to_csv(f'{safe_name}_reviews.csv', index=False)
