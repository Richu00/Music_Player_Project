"""
playlists.py
------------
Global playlist state and all functions that create, modify, or
remove playlists.

Variables
---------
playlists : dict[str, MusicPlayer]
    Maps every playlist name to its MusicPlayer instance.
current_playlist : MusicPlayer or None
    The playlist that is currently active. None until the user creates
    or switches to one.

Functions
---------
create_new_playlist()
    Create an empty playlist and make it active.
create_random_playlist()
    Create a playlist pre-filled with random songs and make it active.
switch_playlist()
    Change the active playlist.
rename_playlist()
    Rename an existing playlist, keeping all pointers in sync.
delete_playlist()
    Remove a playlist by name.
show_all_playlists()
    Print the names of every created playlist.
"""

import random
from models import MusicPlayer
from library import master_library


# ──────────────────────────────────────────────────────────────────────────────
# Global state
# ──────────────────────────────────────────────────────────────────────────────

# All playlists keyed by name. Populated as the user creates playlists.
playlists: dict = {}

# The playlist currently in use. Any menu that needs a playlist reads
# this variable; any function that changes which playlist is active
# must update it via `global current_playlist`.
current_playlist = None


# ──────────────────────────────────────────────────────────────────────────────
# Playlist operations
# ──────────────────────────────────────────────────────────────────────────────

def create_new_playlist() -> None:
    """
    Create a new, empty playlist and set it as the active one.

    Prompts the user for a name, validates it is non-empty and not
    already taken, then stores a new ``MusicPlayer`` in ``playlists``
    and updates ``current_playlist``.
    """
    global current_playlist

    name = input("Enter playlist name: ").strip()

    if not name:
        print("Name cannot be empty.")
        return
    if name in playlists:
        print("A playlist with that name already exists.")
        return

    playlists[name]  = MusicPlayer(name)
    current_playlist = playlists[name]
    print(f"Playlist '{name}' created and selected.")


def create_random_playlist() -> None:
    """
    Create a playlist pre-filled with random songs and make it active.

    Picks up to 10 unique songs from ``master_library`` using
    ``random.sample``, which guarantees no duplicates within a single
    random playlist.

    Notes
    -----
    If ``master_library`` has fewer than 10 songs, all songs are added.
    """
    global current_playlist

    if not master_library:
        print("Master library is empty.")
        return

    name = input("Enter random playlist name: ").strip()

    if not name:
        print("Name cannot be empty.")
        return
    if name in playlists:
        print("A playlist with that name already exists.")
        return

    new_playlist = MusicPlayer(name)

    # random.sample returns `count` unique items — no duplicate songs
    count        = min(10, len(master_library))
    random_songs = random.sample(master_library, count)

    for song in random_songs:
        new_playlist.add_song(song)

    playlists[name]  = new_playlist
    current_playlist = new_playlist
    print(f"Random playlist '{name}' created and selected.")


def switch_playlist() -> None:
    """
    Change the active playlist.

    Lists all available playlist names before prompting, so the user
    does not need to remember exact names from memory.
    """
    global current_playlist

    if not playlists:
        print("No playlists available.")
        return

    show_all_playlists()
    name = input("Enter playlist name to switch to: ").strip()

    if name in playlists:
        current_playlist = playlists[name]
        print(f"Switched to '{name}'")
    else:
        print("Playlist not found.")


def rename_playlist() -> None:
    """
    Rename an existing playlist, keeping all internal references in sync.

    Updates both the ``playlists`` dictionary key (external reference)
    and the ``MusicPlayer.name`` attribute (internal reference) so they
    always agree. Also refreshes ``current_playlist`` when the renamed
    playlist is the currently active one.
    """
    global current_playlist

    if not playlists:
        print("No playlists available.")
        return

    show_all_playlists()
    old_name = input("Enter the name of the playlist to rename: ").strip()

    if old_name not in playlists:
        print("Playlist not found.")
        return

    new_name = input("Enter the new name: ").strip()

    if not new_name:
        print("Name cannot be empty.")
        return
    if new_name in playlists:
        print("A playlist with that name already exists.")
        return

    # Pop the object under the old key, update its internal name,
    # then re-insert it under the new key
    playlist_obj      = playlists.pop(old_name)
    playlist_obj.name = new_name
    playlists[new_name] = playlist_obj

    # If this was the active playlist, point current_playlist at the
    # re-inserted object so the reference does not go stale
    if current_playlist and current_playlist.name == new_name:
        current_playlist = playlists[new_name]

    print(f"Playlist renamed: '{old_name}' → '{new_name}'")


def delete_playlist() -> None:
    """
    Delete a playlist by name.

    If the deleted playlist is currently active, ``current_playlist``
    is set to None so the application does not hold a dangling reference
    to a removed object.
    """
    global current_playlist

    if not playlists:
        print("No playlists available.")
        return

    show_all_playlists()
    name = input("Enter playlist name to delete: ").strip()

    if name not in playlists:
        print("Playlist not found.")
        return

    del playlists[name]

    # Deselect if the active playlist was just deleted
    if current_playlist and current_playlist.name == name:
        current_playlist = None

    print(f"Playlist '{name}' deleted.")


def show_all_playlists() -> None:
    """Print the names of every playlist stored in ``playlists``."""
    if not playlists:
        print("No playlists created.")
    else:
        print("\nAll Playlists:")
        for name in playlists:
            print(f"  - {name}")
