import typer
from rich import print

print("[bold red]This is bold red text![/bold red]")


def main(name: str):
    print(f"CLI Processing {name}")


typer.run(main)

# Usage: python cli.py Ravi
