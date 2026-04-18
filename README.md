# Kleep

Transform YouTube concert videos into organized music albums you can enjoy offline on any device.

## What is Kleep?

Kleep is a command-line tool that downloads YouTube videos and splits them into individual tracks, creating a properly tagged music album.

## Project Inspiration

I love watching concert videos on YouTube and wondered if there could be a way to have those same videos as albums I could listen to on my phone with no struggle. So I created Kleep, a simple CLI that allows you to create an album with as many tracks as you wish from any video on YouTube.

## Features

- **Automatic track splitting** - Uses YouTube chapters or key moments, when available, for instant track organization
- **Manual mode** - For videos without chapters or key moments, manually define how many tracks you want with custom names and timestamps
- **Full metadata tagging** - Adds album name, artist, track numbers, and titles to each MP3
- **Clean output** - On a first run it lets you choose where you want to save your files

## Installation

Download  from the [Releases](../../releases) page.

Make it executable (macOS/Linux):

```bash
chmod +x kleep-[os]-latest
```

## Execution example

```bash
# Basic usage
kleep link [Youtube video]

# With custom title and artist
kleep link [Youtube video] -t "Album Title" -a "Artist Name"
```

Note: for videos that have no chapters or key moments available, you'll be asked interactively for the number of tracks, their respective names and timestamps.
