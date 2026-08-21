# Simple Audiobook Organizer

A small Python script for organizing audiobook folders.

The script moves audio files from subdirectories such as `CD 1`, `CD 2`, etc. into the audiobook's root directory. Before moving anything, it checks for filename collisions and shows a preview of all planned moves.

It can also:

* Remove `desktop.ini` files
* Move, delete, or keep other files individually
* Remove empty subdirectories

## Requirements

* Python 3
* No external Python packages are required

## Usage

Run the script with the audiobook directory as the argument:

```bash
python3 ~/SimpleAudiobookOrganizer.py /path/to/audiobook
```

Or use the current directory:

```bash
python3 ~/SimpleAudiobookOrganizer.py .
```

## Example

Before:

```text
Audiobook/
├── CD 1/
│   ├── 001.mp3
│   ├── 002.mp3
│   └── 003.mp3
├── CD 2/
│   ├── 004.mp3
│   ├── 005.mp3
│   └── 006.mp3
└── desktop.ini
```

The script previews the audio files before moving them:

```text
The following files will be moved:

  001.mp3  from  /CD 1/001.mp3
  002.mp3  from  /CD 1/002.mp3
  003.mp3  from  /CD 1/003.mp3
  004.mp3  from  /CD 2/004.mp3
  005.mp3  from  /CD 2/005.mp3
  006.mp3  from  /CD 2/006.mp3

Move all audio files to the root directory? [y/N]
```

After moving:

```text
Audiobook/
├── 001.mp3
├── 002.mp3
├── 003.mp3
├── 004.mp3
├── 005.mp3
└── 006.mp3
```

## Filename Collision Protection

Before moving any audio files, the script checks for filename collisions.

For example:

```text
CD 1/001.mp3
CD 2/001.mp3
```

Both files would need to become:

```text
001.mp3
```

The script detects this and **does not move any audio files**.

It also detects files that already exist in the audiobook root directory.

No files are overwritten.

## Supported Audio Formats

The following file extensions are recognized:

```text
.mp3
.m4a
.m4b
.aac
.flac
.ogg
.opus
.wav
.wma
.aiff
```

## Other Files

After processing the audio files, the script searches for `desktop.ini` files.

You can choose whether to delete them:

```text
Delete all desktop.ini files? [y/N]
```

Other non-audio files are handled individually:

```text
File:
  /path/to/audiobook/CD 1/cover.jpg

  [m] Move
  [d] Delete
  [k] Keep

Choice [m/d/k]:
```

* `m` — Move the file to the audiobook root
* `d` — Delete the file
* `k` — Keep the file in its current location

## Empty Directories

At the end, the script can remove all empty subdirectories.

Directories are processed from the deepest level upward, so nested empty directories can also be removed.

```text
Delete all empty subdirectories? [y/N]
```

## Safety

The script is designed to avoid accidental overwrites:

* Audio filename collisions are detected before any audio files are moved.
* Existing files in the root directory are detected.
* Audio files are only moved after explicit confirmation.
* Other files require an individual decision.
* Empty directories are only removed after explicit confirmation.
