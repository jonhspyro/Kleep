# Kleep

Transform YouTube concert videos into organized music albums you can enjoy offline on any device.

## What is Kleep?

Kleep is a command-line tool that downloads YouTube videos and splits them into individual tracks, creating a properly tagged music album.

## Project Inspiration

I love watching concert videos on YouTube and wondered if there could be a way to have those same videos as albums I could listen to on my phone with no struggle. So I created Kleep, a simple CLI that allows you to create an album with as many tracks as you wish from any video on YouTube.

## Features

- **Automatic track splitting** - Uses YouTube chapters when available for instant track organization
- **Manual mode** - For videos without chapters, manually define tracks with custom names and timestamps
- **Full metadata tagging** - Adds album name, artist, track numbers, and titles to each MP3
- **Clean output** - Creates organized folders with properly named files

## How It Works

1. Paste a YouTube link
2. Kleep downloads the audio and detects chapters (if available)
3. Customize the album and artist names
4. If no chapters exist, enter track count, names, and respective timestamps for when each track starts
5. Get a folder with individual MP3 files, ready to transfer to your device

## Setup

### Prerequisites

- Python 3.8 or higher
- FFmpeg
- Poetry

### Installation

#### 1. Install FFmpeg

#### **macOS**

```bash
brew install ffmpeg
```

#### **Linux (Ubuntu/Debian)**

```bash
sudo apt install ffmpeg
```

#### **Windows**

```bash
winget install ffmpeg
```

#### 2. Install Poetry

#### **macOS/Linux**

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

#### **Windows (PowerShell)**

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

#### 3. Install Project Dependencies

```bash
poetry install
```

## Usage

```bash
poetry run kleep
```

Follow the interactive prompts to download and split your audio.
