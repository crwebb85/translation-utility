import os
from pathlib import Path
from typing import Optional
import typer
from translate import __app_name__, __version__
import translate.client as client

app = typer.Typer()

@app.command()
def translate(
    input_path: Path = typer.Option(
        Path('input.txt'),
        '--file',
        '-f',
        prompt="Enter the text file to translate",
        exists=True,
    ),
    output_path: Path = typer.Option(
        Path('output.txt'),
        '--out',
        '-o',
        prompt='Enter the output file path:',
    ),
    deepl_executable_path: Path = typer.Option(
        Path(os.path.join(os.path.expanduser('~'),'AppData/Local/DeepL/DeepL.exe')),
        '-dl',
        '--deepl',
        prompt='Enter the path to DeepL executable:',
        exists=True,
    )
) -> None:
    client.translate(input_path, output_path, deepl_executable_path)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return