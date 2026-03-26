#!/usr/bin/env python3
import csv
import sys
from pathlib import Path


def load_rows(path: Path):
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def classify_row(row):
    title = (row.get('title') or '').lower()
    reviews = int((row.get('reviews') or '0').strip() or 0)
    badges = (row.get('badges') or '').lower()

    if any(term in title for term in ['disney', 'marvel', 'pokemon', 'logo']):
        return 'exclude', 'possible IP risk'
    if reviews >= 5000 and 'bestseller' not in badges:
        return 'defender', 'high review count without strong fresh signal'
    if 'bestseller' in badges or 'popular now' in badges:
        return 'forward', 'fresh traction or standout marketplace signal'
    if reviews >= 200:
        return 'midfielder', 'proven demand with room for adaptation'
    return 'midfielder', 'limited evidence; treat as exploratory'


def main():
    if len(sys.argv) != 2:
        print('Usage: matrix_generator.py <csv-file>', file=sys.stderr)
        sys.exit(1)

    path = Path(sys.argv[1]).expanduser()
    rows = load_rows(path)

    print('# Research Matrix')
    print()
    print(f'- Source file: {path}')
    print(f'- Rows analyzed: {len(rows)}')
    print()
    print('| Title | Tier | Reason |')
    print('|---|---|---|')

    for row in rows:
        title = (row.get('title') or '').replace('|', '/').strip()
        tier, reason = classify_row(row)
        print(f'| {title} | {tier} | {reason} |')


if __name__ == '__main__':
    main()
