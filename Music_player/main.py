"""
main.py
-------
Entry point for the Music Player application.

Run this file directly to start the player::

    python main.py

Project layout
--------------
main.py       Entry point and main menu (this file).
models.py     Song, Node, and MusicPlayer classes.
library.py    Master song catalogue plus search and sort utilities.
playlists.py  Global playlist state and create/switch/rename/delete logic.
favorites.py  Global favorites list and add/show logic.
menus.py      All sub-menu loop functions (routing only, no business logic).

Functions
---------
menu()
    Display the main menu, show a live status header, and route the
    user to the appropriate sub-menu.
"""

import playlists as pl
from menus import (
    playlist_menu,
    edit_playlist_menu,
    playback_menu,
    library_menu,
    favorites_menu,
)


# ──────────────────────────────────────────────────────────────────────────────
# Main menu
# ──────────────────────────────────────────────────────────────────────────────

def menu() -> None:
    """
    Display the main menu and route user input to sub-menus.

    A live status header is printed at the top of every loop iteration
    so the user can always see the active playlist, playback state,
    volume, shuffle, and repeat settings without navigating anywhere.

    Options
    -------
    1  Playlist Options  — create, switch, rename, or delete playlists.
    2  Edit Playlist     — add, remove, or clear songs.
    3  Playback Controls — play, pause, skip, volume, shuffle, repeat.
    4  Library Options   — search or sort the master library.
    5  Favorites         — add the current song or view saved favorites.
    0  Exit the application.
    """
    while True:
        # Snapshot the active playlist into a short alias for the header
        cp = pl.current_playlist

        print(f"""
===== MUSIC PLAYER =====
Current Playlist : {cp.name        if cp else 'None'}
Now Playing      : {'ON'           if cp and cp.is_playing else 'OFF'}
Volume           : {cp.volume      if cp else 'N/A'}
Shuffle          : {'ON'           if cp and cp.shuffle    else 'OFF'}  |  \
Repeat : {'ON' if cp and cp.repeat else 'OFF'}

1. Playlist Options
2. Edit Current Playlist
3. Playback Controls
4. Library Options
5. Favorites
0. Exit
""")

        choice = input("Choose option: ")

        if   choice == "1": playlist_menu()
        elif choice == "2": edit_playlist_menu()
        elif choice == "3": playback_menu()
        elif choice == "4": library_menu()
        elif choice == "5": favorites_menu()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


# ──────────────────────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────────────────────

# Guard ensures menu() only runs when this file is executed directly.
# Importing main.py as a module (e.g. for testing) will not trigger it.
if __name__ == "__main__":
    menu()
