#!/usr/bin/env python3
import csv
import sys
from pathlib import Path


IP_TERMS = ['disney', 'marvel', 'pokemon', 'logo', 'naruto', 'ghibli']
SEASONAL_TERMS = [
    'valentine', 'halloween', 'christmas', 'graduation', 'back to school',
    'easter', 'mother\'s day', 'fathers day', 'father\'s day', 'election'
]
FORWARD_BADGES = ['bestseller', 'popular now']


def load_rows(path: Path):
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def to_int(value, default=0):
    if value is None:
        return default
    text = str(value).strip().lower().replace(',', '')
    if not text:
        return default
    mult = 1
    if text.endswith('k'):
        mult = 1000
        text = text[:-1]
    try:
        return int(float(text) * mult)
    except ValueError:
        return default


def classify_row(row):
    title = (row.get('title') or '').lower()
    badges = (row.get('badges') or '').lower()
    reviews = to_int(row.get('reviews'))
    sold_24h = to_int(row.get('sold_24h'))
    total_sold = to_int(row.get('total_sold'))
    listing_age_days = to_int(row.get('listing_age_days'), default=-1)
    search_position = to_int(row.get('search_position'), default=9999)

    if any(term in title for term in IP_TERMS):
        return 'exclude', 'high', 'possible IP risk'

    if any(term in title for term in SEASONAL_TERMS):
        if sold_24h >= 5 or any(b in badges for b in FORWARD_BADGES):
            return 'midfielder', 'medium', 'event-driven keyword with active momentum'

    if listing_age_days != -1 and listing_age_days <= 60:
        if sold_24h >= 10:
            return 'forward', 'high', 'new listing with strong recent sales velocity'
        if reviews < 50 and any(b in badges for b in FORWARD_BADGES):
            return 'forward', 'medium', 'new low-review listing with strong marketplace badge'

    if total_sold >= 1000 and sold_24h >= 1:
        return 'defender', 'high', 'large total sold with continuing fresh sales'
    if reviews >= 1000 and search_position <= 24:
        return 'defender', 'medium', 'very high reviews with strong search placement'
    if reviews >= 5000 and sold_24h == 0:
        return 'exclude', 'medium', 'possible dead pattern: high legacy reviews without fresh-sales evidence'

    if reviews >= 200:
        return 'midfielder', 'low', 'proven demand but freshness signals are incomplete'

    return 'midfielder', 'low', 'exploratory pattern with limited evidence'


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
    print('| Title | Tier | Confidence | Reason |')
    print('|---|---|---|---|')

    for row in rows:
        title = (row.get('title') or '').replace('|', '/').strip()
        tier, confidence, reason = classify_row(row)
        print(f'| {title} | {tier} | {confidence} | {reason} |')


if __name__ == '__main__':
    main()
