#!/bin/bash

for file in *.mp3; do
    echo "Processing: $file"

    tmpfile="${file%.mp3}_fixed.mp3"

    ffmpeg -hide_banner -loglevel error -i "$file" -c:a copy -write_xing 0 "$tmpfile"

    if [ $? -eq 0 ]; then
        mv "$tmpfile" "$file"
        echo "Fixed: $file"
    else
        echo "Failed: $file"
        rm -f "$tmpfile"
    fi
done

