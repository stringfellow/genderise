# -*- coding: utf-8 -*-
import click

from genderify.gender_finder import Genderifier


@click.command()
@click.option(
    '--spotify-token', help="Spotify OAuth token."
)
@click.option(
    '--lastfm-key', help="Spotify OAuth token."
)
@click.option(
    '--name', help="Optionally limit to lookup this name.", default=None
)
@click.option(
    '--offset', help="Offset for fetching artist search results", default=None,
    type=int
)
@click.option(
    '--batch-limit', help="How many to fetch at once", default=50,
    type=int
)
@click.option(
    '--db-file-path', help="Path to db file.", default=None, type=click.Path()
)
@click.option(
    '--forever/--once', help="Keep going until killed, or just once.",
    default=False
)
@click.option(
    '--force-fetch/--skip-found', help="Always re-try if already in database",
    default=False,
)
@click.option(
    '--playlist-url', help="A Spotify public playlist URL to scan."
)
def genderify(spotify_token, lastfm_key, name, offset, batch_limit,
              db_file_path, forever, force_fetch, playlist_url):
    """Get all the artist names."""

    with Genderifier(
        spotify_token=spotify_token,
        lastfm_api_key=lastfm_key,
        batch_limit=batch_limit,
        db_file_path=db_file_path,
        force_fetch=force_fetch,
    ) as genderifier:
        if name:
            genderifier.genderise(
                genderifier.get_artist_obj_from_name(name)
            )
            return

        if playlist_url:
            genderifier.set_artists_batch_from_spotify_public_playlist(
                url=playlist_url
            )
            genderifier.genderise_batch()
            report = genderifier.get_report()
            return report

        try:
            while forever:
                genderifier.set_artist_batch_from_spotify_search(offset)
                genderifier.genderise_batch()
            else:
                genderifier.set_artist_batch_from_spotify_search(offset)
                genderifier.genderise_batch()
        except RuntimeError as rte:
            click.secho(str(rte), fg="red")
        except KeyboardInterrupt:
            click.secho("You quit!", fg="blue")
        except SystemExit:
            click.secho("System exit.", fg="yellow")


if __name__ == '__main__':
    genderify()
