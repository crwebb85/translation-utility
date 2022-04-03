import os
from pathlib import Path
from typing import List, Optional
import typer
from tutils import __app_name__, __version__
import tutils.translation_client as client
from tutils.document_utils import resize_files
from datasize import DataSize

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

@app.command()
def resize(
    size: str = typer.Argument("1MB"),
    path: Path = typer.Option(
        None,
        '--path',
        '-p',
    ),
    files: Optional[List[Path]] = typer.Option(
        None,
        '--file',
        '-f',
    ),
    output_dir: Path = typer.Option(
        '--out',
        '-o',
    ),output_file_name: str = typer.Option(
        'out.txt',
        '--name',
        '-n',
    )
) -> None:
    dir_files =  [file for file in path.iterdir() if file.exists() and not file.is_dir() and file.stem.isnumeric ]
    dir_files = sorted(dir_files, key=lambda file: int(file.stem))
    all_files = files + dir_files
    all_files = [f for f in all_files if f.exists() and not f.is_dir()]
    print([os.path.basename(f) for f in all_files])
    resize_files(all_files, output_dir,output_file_name=output_file_name, max_file_size=DataSize(size))
    


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