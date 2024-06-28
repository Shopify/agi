import typer
from typing import List
from agi.db.neo4j import Neo4jConnection
from agi.config.settings import settings
from agi.agent import Agent
from agi.wiki_connector import WikiArticle
import re

app = typer.Typer()


@app.command(help="Chat with agi agent")
def chat(
    message: str = typer.Argument(..., help="The prompt sent to the AGI"),
    trust: float = typer.Option(
        settings.TRUST,
        help="between 0 and 1.0 where 0 is no trust and 1.0 is absolute trust",
    )
):
    print(f"🤔")
    agent = Agent(trust=trust)
    response = agent.interact(message)
    print(response)


@app.command(help="drop semantic network")
def destroy():
    neo4j = Neo4jConnection()
    neo4j.drop_all()
    print("🤖🔫 AGI has been destroyed... says the computer...")
    

@app.command(help="Ingest the summary of Wikipedia articles")
def wiki(
    titles: List[str] = typer.Argument(..., help="Comma separated list of Wikipedia articles to ingest"),
    summary: bool = typer.Option(False, "--summary", help="Only the summary of the articles")
):
    for title in titles:
        print(f"🔎 collecting `{title}` Wikipedia article...")
        article = WikiArticle(title)

        if summary:
            print(f"I will read the summary of the Wikipedia article for `{article.title}`...")
            text = article.summary
        else:
            print(f"I will read the full Wikipedia article for `{article.title}`")
            text = article.text

        paragraphs = re.split(r'\n+', text.strip())
        agent = Agent(trust=1.0)
        for paragraph in paragraphs:
            print(f"I'm reading this paragraph:\n```\n{paragraph}\n```")
            agent.interact(paragraph)


if __name__ == "__main__":
    app()
