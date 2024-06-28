import wikipediaapi

class WikiArticle:
    """
    Get the summary section of a wikipedia page by title

    Example:
    ```python
    from agi.wiki_connector import WikiArticle
    
    shopify_article = WikiArticle("shopify")
    print(shopify_article.title)
    ```
    """
    def __init__(self, title):
        self.user_agent = 'AGI (xxxx@example.com)'
        self.agent = wikipediaapi.Wikipedia(self.user_agent, 'en')
        self.article = self.agent.page(title=title)
        self.title = self.article.title
        self.summary = self.article.summary
        self.text = self.article.text
        self.backlinks = self.article.backlinks
        self.links = self.article.links
        self.linked_articles = list(self.article.links.keys())
        self.backlinked_articles = list(self.article.backlinks.keys())
