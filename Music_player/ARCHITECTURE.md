# Architecture

This document explains the key design decisions behind Tunes in depth.

---

## Why a Doubly Linked List for Playlists?

The single most important structural decision in Tunes is using a doubly linked list (DLL) instead of a Python `list` for playlists.

### The problem with arrays

A Python list is backed by a contiguous block of memory. That gives you O(1) random access (`playlist[i]`) — but it makes every other operation more expensive:

- **Going back**: There is no "previous" pointer. To go one step back from index `i`, a naive implementation re-scans from `i-1`. Worse, if you only store `current_index` as an integer, you lose the reference and have to reconstruct it.
- **Inserting mid-list**: Inserting at position `i` requires shifting every element after `i` one position to the right — O(n).
- **Deleting mid-list**: Same issue — O(n) shift.

Music players **never need random access**. They only ever move forward one step or backward one step. An array's one advantage is irrelevant to the problem.

### What the DLL gives us

Every `Node` in the DLL holds three things:

```python
class Node:
    song: Song        # the track
    next: Node | None # pointer to the next song
    prev: Node | None # pointer to the previous song
```

The `MusicPlayer` tracks three additional pointers:

```python
class MusicPlayer:
    head:    Node | None  # first song
    tail:    Node | None  # last song
    current: Node | None  # currently playing
```

With this structure:

- **Skip forward**: `self.current = self.current.next` — O(1), one pointer follow
- **Go back**: `self.current = self.current.prev` — O(1), one pointer follow
- **Delete current song**: relink `current.prev.next` and `current.next.prev` — O(1)
- **Append song**: `self.tail.next = new_node; self.tail = new_node` — O(1)

All four operations a music player performs are constant time.

---

## Shuffle Implementation

Shuffle is implemented without a separate shuffled copy of the playlist. When shuffle is ON, `next_song()` calls `_play_random_song()`:

```python
def _play_random_song(self):
    # Collect all nodes into a list (O(n) traversal)
    all_nodes = []
    temp = self.head
    while temp:
        all_nodes.append(temp)
        temp = temp.next

    # Exclude current node to prevent back-to-back repeats
    candidates = [n for n in all_nodes if n != self.current]
    self.current = random.choice(candidates)
    self.play()
```

This is O(n) per skip — acceptable because playlists are small in practice. A production implementation would pre-compute a shuffled order and track position within it, avoiding the traversal on each skip.

---

## Progress Tracking

Elapsed time is tracked using two instance variables on `MusicPlayer`:

```python
play_start_time:   float | None  # time.time() when current song started
elapsed_before_pause: float      # seconds banked before the last pause
```

When `play()` is called, `play_start_time` is set and `elapsed_before_pause` is reset to 0. When `pause()` is called, the delta `time.time() - play_start_time` is added to `elapsed_before_pause` and `play_start_time` is cleared.

`show_progress()` computes the total as:

```
total = elapsed_before_pause + (time.time() - play_start_time)  # if playing
total = elapsed_before_pause                                     # if paused
```

This means progress survives any number of pause/resume cycles without drift.

---

## The Master Library as an Internet Simulation

`master_library` in `library.py` is intentionally modelled after what a real streaming API returns.

In production, a music app fetches its catalogue from the internet — a Spotify API call returns a JSON array of track objects. `master_library` replaces that network call with a hardcoded list of `Song` objects, but the interface is identical: a list of objects with `.title` and `.artist` attributes.

Every piece of code that operates on `master_library` — search, sort, the add-song flow — would work identically if `master_library` were replaced with:

```python
import requests

def fetch_library(query: str) -> list[Song]:
    response = requests.get(f"https://api.spotify.com/v1/search?q={query}")
    tracks = response.json()["tracks"]["items"]
    return [Song(t["name"], t["artists"][0]["name"]) for t in tracks]
```

The only change needed is the data source. All downstream logic — the DLL, search, sort, playlists, favorites — is already compatible.

---

## Module Dependency Graph

```
main.py
 └── menus.py
      ├── playlists.py
      │    ├── models.py  (MusicPlayer)
      │    └── library.py (master_library)
      ├── library.py
      │    └── models.py  (Song)
      └── favorites.py
           └── models.py  (Song)
```

`models.py` has no imports from the project — it is the foundation layer. Everything else imports from it. This means you can test `models.py` in complete isolation.

---

## Why No Circular Imports?

State (the `playlists` dict and `current_playlist`) lives entirely in `playlists.py`. Functions in `library.py` and `favorites.py` that need the active playlist accept it as a **parameter** rather than importing from `playlists.py`. This breaks any potential circular dependency and makes those functions independently testable.

---

## Decisions Not Taken

**Why not use `collections.deque`?**
A deque supports O(1) appends and pops at both ends, but does not support O(1) deletion from an arbitrary position or direct access to a "current" pointer with bidirectional traversal. The custom DLL gives more precise control for the music player use case.

**Why not use a database for the master library?**
For a terminal project, a hardcoded list is the right scope. The architecture is designed so a database (or API) can replace the list without touching any other module. See the Roadmap section in the README.

**Why not threads for "real" playback?**
Audio playback would require a separate thread to play audio while the main thread handles input. That is outside the scope of this project. The `play()` method simulates the concept correctly — tracking what is "playing" and for how long — without requiring platform-specific audio dependencies.
