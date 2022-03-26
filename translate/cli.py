from typing import Optional
from pathlib import Path
import os

import typer

from translate import __app_name__, __version__

app = typer.Typer()


def paragraphs(fileobj, separator='\n'):
    if separator[-1:] != '\n': separator += '\n'
    paragraph = []
    for line in fileobj:
        if line == separator:
            if paragraph:
                yield ''.join(paragraph)
                paragraph = []
        else:
            paragraph.append(line)
    if paragraph: yield ''.join(paragraph)

def translate_paragraph(paragraph):
    return paragraph #TODO

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
        exists=False,
    ),

) -> None:
    typer.secho(input_path)
    typer.secho(output_path)
    with open(input_path, 'r', encoding = 'utf-8') as input_file, open(output_path,'w', encoding = 'utf-8') as output_file :
        for paragraph in paragraphs(input_file):
            translation = translate_paragraph(paragraph)
            output_file.write(translation)
            output_file.write('\n')


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