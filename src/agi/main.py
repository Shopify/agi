import typer
from agi.db.semantic_network import SemanticNetwork
from agi.config.settings import settings
from agi.agent import Agent

app = typer.Typer()


@app.command(help="Add concept")
def add_concept(concept: str = typer.Option(help="The concept to add")):
    print(f"adding this concept {concept}")


@app.command(help="Chat with agi agent")
def chat(
    message: str = typer.Argument(..., help="The prompt sent to the AGI"),
    trust: float = typer.Option(
        settings.TRUST,
        help="between 0 and 1.0 where 0 is no trust and 1.0 is absolute trust",
    ),
    gullibilty: float = typer.Option(
        settings.GULLIBLITY,
        help="between 0 and 1.0 where 0 is not gullible and 1.0 is very gullible",
    ),
    creativity: float = typer.Option(
        settings.GULLIBLITY,
        help="between 0 and 1.0 where 0 is not creative and 1.0 is very creative",
    ),
    susceptibility: float = typer.Option(
        settings.GULLIBLITY,
        help="between 0 and 1.0 where 0 is not susceptibile and 1.0 is very susceptibile",
    ),
):
    print(f"Creating agent with the following personality")
    print(f"Trust: {trust}")
    print(f"Gullibilty: {gullibilty}")
    print(f"Creativity: {creativity}")
    print(f"Susceptibility: {susceptibility}")

    agent = Agent(trust=trust)
    print(f'Sending this message to the AGI Agent "{message}"')
    agent.interact(message)


@app.command(help="test neo4j")
def neo4j():
    neo4j = SemanticNetwork()
    result = neo4j.query("MATCH (n) RETURN n")
    print(result)
    neo4j.close()


if __name__ == "__main__":
    app()
