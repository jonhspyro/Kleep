from kleep.core.handle_info import kleep
import click

@click.group()
def cli():
    """Kleep: A tool to download YouTube audio and split it into tracks based on chapters/key moments"""
    pass

@cli.command()
@click.argument('link', type=str)
@click.option('-t', '--title', type=str, default=None,
              help='Set the desired album name/title, overriding the video title')
@click.option('-a', '--artist', type=str, default=None,
              help='Set the desired album artist, overriding the video author')
def link(link: str, title: str, artist: str) -> None:
    """
    Gets link from a YouTube video
    Link: The full URL of the YouTube video
    """
    try:
        kleep(link, title, artist)
        click.echo("\nKleeped successfully!")
    except Exception as e:
        click.echo(f"\n[!] Error while running Kleep: {e}", err=True)

if __name__ == "__main__":
    cli()
