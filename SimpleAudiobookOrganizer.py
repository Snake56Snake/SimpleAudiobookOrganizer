#!/usr/bin/env python3

"""
SimpleAudiobookOrganizer.py

Organizes an audiobook folder by moving audio files from subdirectories
into the root directory. Checks for filename collisions before moving
files and provides options for handling desktop.ini files, other files,
and empty subdirectories.


Usage:
    python3 ~/SimpleAudiobookOrganizer.py .
"""

import sys
import shutil
from pathlib import Path


# Audio file extensions to process
AUDIO_EXTENSIONS = {
    ".mp3",
    ".m4a",
    ".m4b",
    ".aac",
    ".flac",
    ".ogg",
    ".opus",
    ".wav",
    ".wma",
    ".aiff",
}


def ask_yes_no(question):
    """Ask a yes/no question."""
    answer = input(f"{question} [y/N] ").strip().lower()
    return answer in ("y", "yes")


# Get the root directory from the command line or use the current directory
ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
ROOT = ROOT.resolve()

if not ROOT.is_dir():
    print()
    print(f"Error: {ROOT} is not a directory.")
    print()
    sys.exit(1)
print()
print(f"Root directory: {ROOT}")
print()


# ------------------------------------------------------------
# Find all audio files in subdirectories
# ------------------------------------------------------------

audio_files = sorted(
    (
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.parent != ROOT
        and path.suffix.lower() in AUDIO_EXTENSIONS
    ),
    key=lambda p: str(p).lower(),
)


# ------------------------------------------------------------
# Check for filename collisions
# ------------------------------------------------------------
collisions = []
target_names = set()

for path in audio_files:
    target = ROOT / path.name

    if target.exists():
        collisions.append((path, target))

    elif target.name in target_names:
        collisions.append((path, target))

    target_names.add(target.name)
    
    
# ------------------------------------------------------------
# Stop if collisions were found
# ------------------------------------------------------------

if collisions:
    print()
    print("NAME COLLISIONS FOUND:")
    print()

    for source, target in collisions:
        print(f"  Source: {source}")
        print(f"  Target: {target}")
        print()

    print("No audio files were moved.")
else:
    # --------------------------------------------------------
    # Move audio files
    # --------------------------------------------------------

    if audio_files:
        print()
        print("The following files will be moved:")
        print()


        moves = [
            (path.name, path.relative_to(ROOT))
            for path in audio_files
        ]


        max_target_length = max(len(filename) for filename, source in moves)

        for filename, source in moves:
            print(f"  {filename:<{max_target_length}}  from  /{source}")
        print()

        if ask_yes_no("Move all audio files to the root directory?"):
            for path in audio_files:
                target = ROOT / path.name
                shutil.move(str(path), str(target))

            print("Audio files moved.")
        else:
            print("Audio files were not moved.")


# ------------------------------------------------------------
# Find desktop.ini files
# ------------------------------------------------------------

desktop_files = [
    path
    for path in ROOT.rglob("*")
    if path.is_file() and path.name.lower() == "desktop.ini"
]

if desktop_files:
    print()
    print("desktop.ini files found:")
    print()

    for path in desktop_files:
        print(f"  {path}")

    print()

    if ask_yes_no("Delete all desktop.ini files?"):
        for path in desktop_files:
            path.unlink()

        print("desktop.ini files deleted.")
    else:
        print("desktop.ini files were kept.")


# ------------------------------------------------------------
# Find all other files in subdirectories
# ------------------------------------------------------------

other_files = []

for path in ROOT.rglob("*"):
    if not path.is_file():
        continue

    # Only process files below the root directory
    if path.parent == ROOT:
        continue

    # Skip audio files
    if path.suffix.lower() in AUDIO_EXTENSIONS:
        continue

    # Skip desktop.ini files
    if path.name.lower() == "desktop.ini":
        continue

    other_files.append(path)


# ------------------------------------------------------------
# Ask what to do with each remaining file
# ------------------------------------------------------------

for path in other_files:
    print()
    print("File:")
    print(f"  {path}")
    print()
    print("  [m] Move")
    print("  [d] Delete")
    print("  [k] Keep")

    while True:
        answer = input("Choice [m/d/k]: ").strip().lower()

        if answer == "m":
            target = ROOT / path.name

            if target.exists():
                print(f"  ERROR: {target} already exists.")
                print("  File was kept.")
            else:
                shutil.move(str(path), str(target))
                print("  Moved.")

            break

        elif answer == "d":
            path.unlink()
            print("  Deleted.")
            break

        elif answer == "k":
            print("  Kept.")
            break

        else:
            print("  Please enter m, d or k.")


# ------------------------------------------------------------
# Remove empty subdirectories
# ------------------------------------------------------------

print()

if ask_yes_no("Delete all empty subdirectories?"):
    # Process deepest directories first
    directories = sorted(
        [path for path in ROOT.rglob("*") if path.is_dir()],
        key=lambda p: len(p.parts),
        reverse=True,
    )

    for path in directories:
        try:
            path.rmdir()
        except OSError:
            # Directory is not empty
            pass

    print("Empty subdirectories deleted.")
else:
    print("Empty subdirectories were kept.")


print()
print("Done.")
