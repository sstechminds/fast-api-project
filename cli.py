import typer

def main(name: str):
    print(f"CLI Processing {name}")

typer.run(main)

# Usage: python cli.py Ravi