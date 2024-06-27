import typer
from agi.db.neo4j_connection import Neo4jConnection
from agi.agent import Agent

app = typer.Typer()

@app.command(help="Add concept")
def add_concept(
    concept: str = typer.Option(help="The concept to add")
):
    print(f"adding this concept {concept}")

@app.command(help="Chat with agi agent")
def chat(
    message: str = typer.Argument(..., help="The prompt sent to the AGI"),
    trust_level: float = typer.Option(0.8, help="between 0 and 1.0 where 0 is no trust and 1.0 is absolute trust")
):
    print(f"Creating agent with a trust level of {trust_level}")
    agent = Agent(trust_level=trust_level)
    print(f'Sending this message to the AGI Agent "{message}"')
    agent.interact(message)

@app.command(help="test neo4j")
def neo4j():
    neo4j = Neo4jConnection()
    result = neo4j.query("MATCH (n) RETURN n")
    print(result)
    neo4j.close()

if __name__ == "__main__":
    app()
