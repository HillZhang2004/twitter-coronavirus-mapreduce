#!/usr/bin/env python3

import argparse
import json
import os
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('--input_path', required=True)
parser.add_argument('--key', required=True)
parser.add_argument('--percent', action='store_true')
parser.add_argument('--output_path', default=None)
args = parser.parse_args()

with open(args.input_path) as f:
    counts = json.load(f)

if args.key not in counts:
    raise KeyError(f'Key {args.key} not found in {args.input_path}')

items = list(counts[args.key].items())

if args.percent:
    items = [
        (k, v / counts['_all'][k])
        for k, v in items
        if k in counts.get('_all', {}) and counts['_all'][k] != 0
    ]

# keep top 10 by value
items = sorted(items, key=lambda item: (item[1], item[0]), reverse=True)[:10]

# then sort low -> high for plotting
items = sorted(items, key=lambda item: (item[1], item[0]))

labels = [k for k, v in items]
values = [v for k, v in items]

if args.output_path is None:
    base = os.path.basename(args.input_path)
    safe_key = args.key.replace('#', '').replace('/', '_')
    suffix = '.percent' if args.percent else ''
    args.output_path = f'img/{base}.{safe_key}{suffix}.png'

outdir = os.path.dirname(args.output_path) or '.'
os.makedirs(outdir, exist_ok=True)

plt.figure(figsize=(10, 6))
plt.bar(labels, values)
plt.xlabel('Key')
plt.ylabel('Percent' if args.percent else 'Count')
plt.title(f'{args.key} in {os.path.basename(args.input_path)}')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(args.output_path)
plt.close()

print('saved', args.output_path)
