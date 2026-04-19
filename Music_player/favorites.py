"""
favorites.py
------------
Global favorites list and the functions that manage it.

The favorites list is shared across all playlists — a song favorited
in one playlist appears in the favorites list everywhere.

Variables
---------
favorites : list[Song]
    Songs the user has marked as favorites.

Functions
---------
add_to_favorites(current_playlist)
    Add the currently playing song to the favorites list.
show_favorites()
    Print every song in the favorites list.
"""

from models import Song


# ──────────────────────────────────────────────────────────────────────────────
# Global state
# ──────────────────────────────────────────────────────────────────────────────

# Grows as the user favorites songs. Persists for the lifetime of the session.
favorites: list = []


# ──────────────────────────────────────────────────────────────────────────────
# Favorites operations
# ──────────────────────────────────────────────────────────────────────────────

def add_to_favorites(current_playlist) -> None:
    """
    Add the currently selected song to the favorites list.

    Prevents duplicates by checking membership before appending.
    ``current_playlist`` is passed in as a parameter rather than read
    from a global so this function remains decoupled from the state
    module and is easier to test in isolation.

    Parameters
    ----------
    current_playlist : MusicPlayer or None
        The active playlist whose ``current`` node holds the song to
        favorite. If None or no song is selected, a notice is printed.
    """
    if not current_playlist or not current_playlist.current:
        print("No song is currently selected.")
        return

    song = current_playlist.current.song

    if song not in favorites:
        favorites.append(song)
        print(f"{song} added to favorites.")
    else:
        print("Already in favorites.")


def show_favorites() -> None:
    """
    Print every song in the favorites list, numbered from 1.

    Prints a notice if the list is empty.
    """
    if not favorites:
        print("No favorite songs yet.")
        return

    print("\nFavorite Songs:")
    for i, song in enumerate(favorites, 1):
        print(f"  {i}. {song}")
