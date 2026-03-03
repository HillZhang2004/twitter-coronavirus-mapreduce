#!/usr/bin/env python3

import argparse
import glob
import json
import os
from collections import defaultdict
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('hashtags', nargs='+')
parser.add_argument('--input_glob', default='outputs/*.lang')
parser.add_argument('--output_path', default='img/alternative_reduce.png')
args = parser.parse_args()

files = sorted(
    path for path in glob.glob(args.input_glob)
    if not path.endswith('final.lang') and not path.endswith('final.country')
)

series = defaultdict(list)
days = []

for day_index, path in enumerate(files, start=1):
    with open(path) as f:
        counts = json.load(f)

    days.append(day_index)

    for hashtag in args.hashtags:
        total = sum(counts.get(hashtag, {}).values())
        series[hashtag].append(total)

outdir = os.path.dirname(args.output_path) or '.'
os.makedirs(outdir, exist_ok=True)

plt.figure(figsize=(12, 6))

for hashtag in args.hashtags:
    plt.plot(days, series[hashtag], label=hashtag)

plt.xlabel('Day of year')
plt.ylabel('Number of tweets')
plt.title('Hashtag usage over time')
plt.legend()
plt.tight_layout()
plt.savefig(args.output_path)
plt.close()

print('saved', args.output_path)
