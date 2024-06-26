import typer
from agi.db.neo4j_connection import Neo4jConnection

app = typer.Typer()

@app.command(help="Add concept")
def add_concept(
    concept: str = typer.Option(help="The concept to add")
):
    print(f"adding this concept {concept}")

@app.command(help="Chat with agi")
def chat(
    prompt: str = typer.Option(help="The prompt sent to the AGI")
):
    print(f'Prompting AGI with "{prompt}"')

@app.command(help="test neo4j")
def neo4j():
    neo4j = Neo4jConnection()
    result = neo4j.query("MATCH (n) RETURN n")
    print(result)
    neo4j.close()

if __name__ == "__main__":
    app()
