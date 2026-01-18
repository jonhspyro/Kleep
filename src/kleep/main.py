from kleep.core.handle_info import kleep
from typing import List
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
def link(link: str, album_title: str, album_artist: str, track_names: List[str]) -> None:
    """
    Gets link from a YouTube video
    Link: The full URL of the YouTube video
    """
    try:
        kleep(link, album_title, album_artist, track_names)
        click.echo("\nKleeped successfully!")
    except Exception as e:
        click.echo(f"\n[!] Error while running Kleep: {e}", err=True)
