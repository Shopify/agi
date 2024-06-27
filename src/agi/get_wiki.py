import wikipediaapi

class GetWikiSummary:
    """
    Get the summary of a wikipedia page by title

    Example:
    ```python
    get_wiki_summary = GetWikiSummary()
    get_summary = get_wiki_summary.get_summary('shopify')
    print(get_summary)

    get_summaries = get_wiki_summary.get_summary_by_titles(['shopify', 'canada'])
    for summary in get_summaries:
        print(f"title: {summary['title']}")
        print(f"summary: {summary['summary']}") 
    ```
    """
    def __init__(self):
        self.USER_AGENT = 'MyProjectName (xxxx@example.com)'
        self.agent = wikipediaapi.Wikipedia(self.USER_AGENT, 'en')

    def get_summary(self, title):
        page_py = self.agent.page(title=title)
        return page_py.summary
    
    def get_summary_by_titles(self, titles):
        return [
            {
                'title': title,
                'summary': self.get_summary(title)
            }
            for title in titles
        ]