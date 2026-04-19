"""
library.py
----------
Master song library plus search and sort utilities.

Variables
---------
master_library : list[Song]
    The full catalogue of tracks available to add to any playlist.

Functions
---------
search_song(current_playlist)
    Search the library by title or artist and optionally add a result
    to the active playlist.
sort_master_library()
    Interactively sort ``master_library`` in-place by title or artist.
merge_sort(arr, key)
    Recursively sort a list of Song objects using merge sort.
_merge(left, right, key)
    Merge two sorted Song lists into one (internal helper).
"""

from models import Song


# ──────────────────────────────────────────────────────────────────────────────
# Master library
# ──────────────────────────────────────────────────────────────────────────────

# Full catalogue of songs. Add or remove Song entries here to change
# what is available across the entire application.
master_library: list = [
    Song("Into the Night",            "Yasobi"),
    Song("Blinding Lights",           "The Weeknd"),
    Song("Jo Tum Mere Ho",            "Anuv Jain"),
    Song("Mockingbird",               "Eminem"),
    Song("Heat Waves",                "Glass Animals"),
    Song("Husn",                      "Anuv Jain"),
    Song("Rap God",                   "Eminem"),
    Song("Butter",                    "BTS"),
    Song("Die For You",               "The Weeknd"),
    Song("Fairytale",                 "Alexander Rybak"),

    Song("Golden Brown",              "The Stranglers"),
    Song("Back To Friends",           "Sombr"),
    Song("Freaks",                    "Surf Curse"),
    Song("Love Story",                "Indila"),
    Song("The Night We Met",          "Lord Huron"),
    Song("I Wanna Be Yours",          "Arctic Monkeys"),
    Song("Running Up That Hill",      "Kate Bush"),
    Song("Blue",                      "Yung Kai"),
    Song("Always The Sun",            "The Stranglers"),

    Song("Washing Machine Heart",     "Mitski"),
    Song("End of Beginning",          "Djo"),
    Song("Runaway",                   "AURORA"),
    Song("Sailor Song",               "Gigi Perez"),
    Song("Night Changes",             "One Direction"),
    Song("Tears",                     "Sabrina Carpenter"),
    Song("Shape of You",              "Ed Sheeran"),
    Song("World's Smallest Violin",   "AJR"),

    Song("Taste",                     "Sabrina Carpenter"),
    Song("Bed Chem",                  "Sabrina Carpenter"),
    Song("Coincidence",               "Sabrina Carpenter"),
    Song("We Don't Talk Anymore",     "Charlie Puth, Selena Gomez"),
    Song("STAY",                      "The Kid LAROI, Justin Bieber"),
    Song("Memories",                  "Maroon 5"),
    Song("A Thousand Years",          "Christina Perri"),
    Song("Die With A Smile",          "Lady Gaga, Bruno Mars"),
    Song("Arz Kiya Hai",              "Anuv Jain"),

    Song("Chubina - Super Slowed",    "East Duo"),
    Song("Daylight",                  "David Kushner"),
    Song("Dandelions",                "Ruth B."),
    Song("Under The Influence",       "Chris Brown"),
    Song("Love Nwantiti",             "CKay"),
    Song("Take Me To Church",         "Hozier"),
    Song("Summertime Sadness",        "Lana Del Rey"),
    Song("Save Your Tears",           "The Weeknd"),
    Song("Another Love",              "Tom Odell"),

    Song("7 Years",                   "Lukas Graham"),
    Song("Someone Like You",          "Adele"),
    Song("When I Was Your Man",       "Bruno Mars"),
    Song("Gul",                       "Anuv Jain"),
    Song("Baarishein",                "Anuv Jain"),
    Song("Meri Baaton Mein Tu",       "Anuv Jain"),
    Song("Alag Aasmaan",              "Anuv Jain"),
    Song("Alag Aasmaan - Acoustic",   "Anuv Jain"),

    Song("Levitating",                "Dua Lipa"),
    Song("Light Switch - Brighter Mix", "Charlie Puth"),
    Song("Beautiful Things - Slowed", "Benson Boone"),
    Song("Death Bed",                 "Powfu, Beabadoobee"),
    Song("Double Take",               "Dhruv"),
    Song("Interstellar",              "JERRIK DIZLOP"),
    Song("Lovely",                    "Billie Eilish, Khalid"),
]


# ──────────────────────────────────────────────────────────────────────────────
# Search
# ──────────────────────────────────────────────────────────────────────────────

def search_song(current_playlist) -> None:
    """
    Search the master library by song title or artist name.

    Performs a case-insensitive substring match against every song in
    ``master_library``. Displays matching results and, if the user
    chooses, adds a selected result to the active playlist.

    ``current_playlist`` is accepted as a parameter (rather than read
    from a global) so this function is not tightly coupled to the
    state module and can be tested independently.

    Parameters
    ----------
    current_playlist : MusicPlayer or None
        The playlist to which a found song may be added.
        If None and the user attempts to add a song, a notice is shown.
    """
    if not master_library:
        print("Master library empty.")
        return

    keyword = input("Enter song title or artist to search: ").lower()
    results = []

    # Collect every song whose title or artist contains the keyword
    for index, song in enumerate(master_library):
        if keyword in song.title.lower() or keyword in song.artist.lower():
            results.append((index, song))

    # Evaluate AFTER the full loop — checking inside the loop would
    # trigger a false "not found" on every iteration before the last one
    if not results:
        print("No songs found.")
        return

    print("\nSearch Results:")
    for i, (_, song) in enumerate(results, 1):
        print(f"  {i}. {song}")

    choice = input("\nAdd a song to current playlist? (y/n): ").lower()

    if choice == "y":
        if not current_playlist:
            print("No playlist selected.")
            return

        # Only prompt for a selection number when the user confirmed "y"
        try:
            num          = int(input("Enter result number: "))
            selected_song = results[num - 1][1]
            current_playlist.add_song(selected_song)
        except (ValueError, IndexError):
            print("Invalid selection.")


# ──────────────────────────────────────────────────────────────────────────────
# Sorting
# ──────────────────────────────────────────────────────────────────────────────

def sort_master_library() -> None:
    """
    Sort ``master_library`` in-place, interactively.

    Prompts the user to choose a sort key (title or artist) then
    replaces ``master_library`` with the sorted result returned by
    ``merge_sort``.
    """
    global master_library

    print("Sort by:")
    print("  1. Title")
    print("  2. Artist")

    choice = input("Choose option: ")

    if choice == "1":
        master_library = merge_sort(master_library, "title")
        print("Sorted by title.")
    elif choice == "2":
        master_library = merge_sort(master_library, "artist")
        print("Sorted by artist.")
    else:
        print("Invalid choice.")


def merge_sort(arr: list, key: str) -> list:
    """
    Sort a list of Song objects using recursive merge sort.

    Splits the list in half, recursively sorts each half, then merges
    them back together in sorted order via ``_merge``.

    Parameters
    ----------
    arr : list[Song]
        The list of songs to sort.
    key : str
        The Song attribute to sort by, e.g. ``'title'`` or ``'artist'``.

    Returns
    -------
    list[Song]
        A new sorted list. The original list is not mutated.

    Notes
    -----
    Time complexity  : O(n log n) in all cases.
    Space complexity : O(n) due to temporary lists created during merging.
    """
    if len(arr) <= 1:
        return arr   # base case — a list of 0 or 1 items is already sorted

    mid   = len(arr) // 2
    left  = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)

    return _merge(left, right, key)


def _merge(left: list, right: list, key: str) -> list:
    """
    Merge two sorted Song lists into a single sorted list.

    Comparison is performed on ``getattr(song, key).lower()`` so the
    sort is always case-insensitive regardless of the chosen key.

    Parameters
    ----------
    left : list[Song]
        First sorted half.
    right : list[Song]
        Second sorted half.
    key : str
        The Song attribute to compare, e.g. ``'title'`` or ``'artist'``.

    Returns
    -------
    list[Song]
        A merged, sorted list containing all elements from both halves.

    Notes
    -----
    Prefixed with ``_`` to signal this is an internal helper.
    Call ``merge_sort`` from outside this module.
    """
    result: list = []
    i = j = 0

    # Compare the front elements of each half and take the smaller one
    while i < len(left) and j < len(right):
        if getattr(left[i], key).lower() <= getattr(right[j], key).lower():
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # One half may still have remaining elements — append them all
    result.extend(left[i:])
    result.extend(right[j:])
    return result
