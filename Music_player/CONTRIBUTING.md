# Contributing

Thanks for your interest in Tunes! Here's how to contribute.

## How to submit changes

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes in `src/`
4. Verify the player still runs: `cd src && python main.py`
5. Open a pull request with a clear description of what you changed and why

## Code standards

All contributions should follow the same standards used throughout the project:

- **NumPy-style docstrings** on every new function and class
- **Type hints** on all function signatures
- **Specific exception handling** — `except (ValueError, IndexError)`, never bare `except:`
- **Single responsibility** — if a function does more than one thing, split it

## Adding songs to the library

Open `src/library.py` and add `Song("Title", "Artist")` entries to `master_library`. Keep artists consistent with existing entries if the artist already appears.

## Suggesting new features

Open an issue describing the feature, why it's useful, and how it fits the existing module structure. Features that require a new module should explain what that module's single responsibility would be.
