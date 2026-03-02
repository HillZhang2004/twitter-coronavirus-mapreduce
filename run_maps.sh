#!/bin/bash
mkdir -p outputs logs

for file in /data/Twitter\ dataset/geoTwitter20-*.zip; do
    base=$(basename "$file" .zip)
    nohup python3 src/map.py --input_path="$file" > "logs/${base}.log" 2>&1 &
done
