import lib.setup as lib_setup
import lib.build as lib_build

import click


@click.group()
def main():
    """
    Simple CLI for building protos in different languages.
    """
    pass


@main.command()
def setup():
    """
    Download and prepare the necessary files and libraries to build the protos
    on different languages.
    """
    click.echo("Setting up necessary files and frameworks for building.")
    lib_setup.setup()


@main.command()
@click.option('--language', '-l', multiple=True, help='Build proto to the current supported languages: ts (Typescript), kt (Kotlin), go (Go).')
def build(language):
    """
    Build the necessary protobuf and gRPC files for Go and Kotlin.
    """
    click.echo("Start building protos from definitions in proto-files.")
    if len(language) == 0:
        build_languages = ['ts','kt','go']
    else:
        build_languages = language
    try:
        lib_build.build(build_languages)
    except Exception as e:
        click.echo(f"Error: {e}")


@main.command()
def clean():
    """
    Clean the folder restoring it to the way it was before the setup and genration
    """
    click.echo("Cleaning files.")
    try:
        lib_build.clean_build()
        lib_setup.clean_setup()
    except Exception as e:
        click.echo(f"Error: {e}")


if __name__ == "__main__":
    main()
