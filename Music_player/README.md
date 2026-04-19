# 🎵 Tunes

> A command-line music player built in Python, backed by a **doubly linked list** and a hand-written **merge sort** — the same structural choices used by real streaming platforms.

```
===== TUNES =====
Current Playlist : My Mix
Now Playing      : ON
Volume           : 70
Shuffle          : ON  |  Repeat : OFF

1. Playlist Options
2. Edit Current Playlist
3. Playback Controls
4. Library Options
5. Favorites
0. Exit
```

---

## Table of Contents

- [About](#about)
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [How It Works](#how-it-works)
  - [Why a Doubly Linked List?](#why-a-doubly-linked-list)
  - [The Master Library](#the-master-library)
  - [Merge Sort](#merge-sort)
- [Module Reference](#module-reference)
- [Data Structures & Algorithms](#data-structures--algorithms)
- [Roadmap — Scaling to a Real App](#roadmap--scaling-to-a-real-app)
- [Code Quality](#code-quality)

---

## About

Tunes is a fully functional Python music player built for a college CS project. Every core mechanic is implemented from scratch using deliberate data structure choices — no built-in `sorted()`, no simple lists for playlists. The goal is to demonstrate that the same structural decisions behind real apps like Spotify can be applied in a 100% Python terminal project.

The **master library** is a local simulation of what would, in a production app, come from a live music streaming API. Each `Song` object mirrors what a real app deserialises from a JSON response. Swapping `master_library` for an API call is a one-line change.

---

## Features

| Feature | Description |
|---|---|
| **Playlist Management** | Create, rename, delete, and switch between multiple named playlists |
| **Shuffle** | True random shuffle — never repeats the same song back-to-back |
| **Repeat** | Loop the entire playlist when the last song ends |
| **Favorites** | Global favorites list shared across all playlists |
| **Search** | Case-insensitive search by title or artist across the full library |
| **Merge Sort** | Sort the master library by title or artist in O(n log n) |
| **Progress Tracking** | Live elapsed time per song — pause-safe, time is banked not reset |
| **Volume Control** | Set volume 0–100 from the playback menu |

---

## Project Structure

```
tunes/
│
├── src/                        # All application source code
│   ├── main.py                 # Entry point — run this to start the player
│   ├── models.py               # Song, Node, MusicPlayer classes
│   ├── library.py              # Master catalogue + search + sort
│   ├── playlists.py            # Playlist state + create/switch/rename/delete
│   ├── favorites.py            # Global favorites list + add/show
│   └── menus.py                # All sub-menu routing (no business logic)
│
├── docs/
│   └── ARCHITECTURE.md         # Deep-dive on data structures and design decisions
│
├── assets/
│   └── demo.txt                # Sample session output
│
├── README.md                   # You are here
├── .gitignore                  # Python + OS ignores
└── LICENSE                     # MIT License
```

### Why this structure?

Each module has **one job**. `models.py` holds classes, `menus.py` routes input, `playlists.py` owns state. This mirrors how a production app would be split across services or packages, and makes it easy to find, fix, or extend any one part without touching the others.

---

## Getting Started

### Requirements

- Python 3.8 or higher
- No third-party libraries required — standard library only

### Run

```bash
git clone https://github.com/your-username/tunes.git
cd tunes/src
python main.py
```

### Quick walkthrough

1. Start the player — you'll see the main menu with a live status header
2. Go to **Playlist Options → Create Playlist** and give it a name
3. Go to **Edit Current Playlist → Add Song from Library** and pick a track
4. Go to **Playback Controls → Play** to start playing
5. Use **Next**, **Previous**, **Toggle Shuffle**, and **Show Progress** from the same menu

---

## How It Works

### Why a Doubly Linked List?

A standard Python list is the obvious choice for a playlist — but it's the wrong one. Here's why Tunes uses a doubly linked list instead:

| Operation | `list` (array) | Doubly Linked List |
|---|---|---|
| Skip forward | O(1) — index jump | O(1) — follow `.next` |
| Go back | **O(n) — rescan from start** | **O(1) — follow `.prev`** |
| Insert at position | O(n) — shift elements | O(1) — relink pointers |
| Delete at position | O(n) — shift elements | O(1) — relink pointers |
| Random access | O(1) | O(n) |

Music players **never need random access** — they always move one step forward or backward. The doubly linked list gives O(1) performance for every operation a music player actually performs.

Every `Node` stores a `Song` plus `.next` and `.prev` pointers:

```
[Prev Song] <──────────────> [♪ Current] <──────────────> [Next Song]
              .prev / .next               .prev / .next
```

Going back is `self.current = self.current.prev`. Going forward is `self.current = self.current.next`. Both are a single pointer follow with no scanning.

### The Master Library

`master_library` in `library.py` is a local simulation of what the internet looks like to a real music app.

In production, this data comes from the internet — Spotify's Web API, Apple Music, or a custom streaming server. The list is our local stand-in for that live data feed. Every `Song(title, artist)` object mirrors what a production app would deserialise from a JSON API response:

```python
# What Tunes does (offline)
Song("Heat Waves", "Glass Animals")

# What a real app receives from Spotify's API
{
  "name": "Heat Waves",
  "artists": [{ "name": "Glass Animals" }],
  ...
}
```

Search and sort run on `master_library` exactly as they would run on a result set fetched from a real server. **Replacing the list with a live API call is a one-line change in `library.py`** — the rest of the application stays identical.

### Merge Sort

The library is sorted using a hand-written recursive merge sort — not Python's built-in `sorted()`. Merge sort was chosen because:

- **O(n log n)** in all cases — no worst-case degradation
- **Stable** — equal-key items keep their original relative order
- **Readable** — the divide-and-merge structure maps naturally to Python recursion

The sort key is passed as a string attribute name (`"title"` or `"artist"`), and `getattr()` is used to access it dynamically — the same function sorts by either field:

```python
master_library = merge_sort(master_library, "title")   # sort by title
master_library = merge_sort(master_library, "artist")  # sort by artist
```

---

## Module Reference

### `main.py`
Entry point. Displays the live status header (playlist, now playing, volume, shuffle, repeat) and routes input to sub-menus. Run with `python main.py`.

### `models.py`
Contains three classes:

- **`Song`** — `title` + `artist`, with a `__str__` for clean printing
- **`Node`** — wraps a `Song` with `.next` and `.prev` pointers
- **`MusicPlayer`** — the full doubly linked list playlist with playback controls, shuffle, repeat, volume, and elapsed-time tracking

### `library.py`
Holds `master_library` (the 60+ song catalogue), `search_song()`, `sort_master_library()`, `merge_sort()`, and the internal `_merge()` helper.

### `playlists.py`
Owns the global `playlists` dict and `current_playlist`. All functions that create, rename, switch, or delete playlists live here.

### `favorites.py`
Holds the global `favorites` list and `add_to_favorites()` / `show_favorites()`. Favorites are session-scoped and shared across all playlists.

### `menus.py`
Pure routing — five sub-menu loops (`playlist_menu`, `edit_playlist_menu`, `playback_menu`, `library_menu`, `favorites_menu`). No business logic; everything delegates to the modules above.

---

## Data Structures & Algorithms

```
MusicPlayer (Doubly Linked List)
├── head  ──► Node ◄──► Node ◄──► Node ◄──► None
├── tail  ──────────────────────────────────────►
└── current ──► (currently playing node)

Node
├── song   : Song
├── next   : Node | None
└── prev   : Node | None

Song
├── title  : str
└── artist : str
```

**Merge sort** (in `library.py`):

```
merge_sort([A, B, C, D, E, F])
├── merge_sort([A, B, C])          merge_sort([D, E, F])
│   ├── merge_sort([A])            ├── merge_sort([D])
│   └── merge_sort([B, C])         └── merge_sort([E, F])
│       ├── merge_sort([B])            ├── merge_sort([E])
│       └── merge_sort([C])            └── merge_sort([F])
│
└── _merge(sorted_left, sorted_right, key)
```

---

## Roadmap — Scaling to a Real App

Tunes is designed so the business logic never needs to change — only the surrounding layer does.

| Component | Current (Tunes) | Production version |
|---|---|---|
| Song catalogue | `master_library` list | Spotify Web API / custom streaming API |
| Search | Substring match | Elasticsearch / API query |
| Sort | In-memory merge sort | `ORDER BY` on a database query |
| Playlists | `MusicPlayer` objects | User playlist API + database rows |
| Saved songs | `favorites` list | Saved tracks API endpoint |
| Interface | Terminal menus | GUI (Tkinter, PyQt, React Native) |
| Persistence | Session only | SQLite / PostgreSQL |
| Audio | Simulated | `pygame` / VLC Python bindings |

The doubly linked list, merge sort, search, shuffle, repeat, and favorites logic all carry over unchanged. Converting Tunes to a production app is a matter of wiring, not rewriting.

---

## Code Quality

All modules follow a consistent set of standards:

- **NumPy-style docstrings** on every class and function (`Parameters`, `Returns`, `Attributes`, `Notes`)
- **Type hints** on all function signatures — e.g. `def add_song(self, song: Song) -> None`
- **Module-level docstrings** listing every export at the top of each file
- **Typed exception handling** — `except (ValueError, IndexError)` only, never bare `except:`
- **Single responsibility** — each module does exactly one thing
- **No tight global coupling** — functions accept `current_playlist` as a parameter rather than reading it from a global

---

## License

MIT — see [LICENSE](LICENSE) for details.
