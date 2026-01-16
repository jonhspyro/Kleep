from kleep.core.handle_info import kleep
import sys
import click

# Define the main command group for the CLI
@click.group()
def cli():
    """Kleep: A tool to download YouTube audio and split it into tracks based on chapters/key moments."""
    pass

# Define the 'kleep' subcommand
@cli.command()
@click.argument('link', type=str)
@click.option('-t', '--title', 'album_title', type=str, default=None,
              help='Set the desired album name/title, overriding the video title.')

@click.option('-a', '--artist', 'album_artist', type=str, default=None,
              help='Set the desired album artist, overriding the video author.')
def link(link: str, album_title: str, album_artist: str) -> None:
    """
    Gets link from a YouTube video.
    Link: The full URL of the YouTube video.
    """
    try:
        click.echo(f"Kleeping: {link}")
        kleep(link, album_title, album_artist)
        click.echo("\nKleeped successfully! 🎉")
    except Exception as e:
        click.echo(f"\n[!] Error while running Kleep: {e}", err=True)


if __name__ == "__main__":
    if getattr(sys, "frozen", False):
        if hasattr(sys, "_kleep_already_running"):
            sys.exit(0)
        sys._kleep_already_running = True
    cli()