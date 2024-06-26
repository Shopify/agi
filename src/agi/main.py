import typer

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

if __name__ == "__main__":
    app()
