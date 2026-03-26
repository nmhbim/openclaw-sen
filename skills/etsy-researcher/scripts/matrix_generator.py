#!/usr/bin/env python3
import csv
import re
import sys
from pathlib import Path


FIELD_ALIASES = {
    'title': ['title', 'Title'],
    'price': ['price', 'Price'],
    'reviews': ['reviews', 'Reviews', 'review_count'],
    'sold_24h': ['sold_24h', 'Sold 24H', 'sold24', 'sold_24_hr'],
    'badge': ['badge', 'Badge', 'badges', 'Badges'],
}


def clean_number(value):
    if value is None:
        return 0
    text = str(value).strip().lower().replace(',', '')
    if not text or text == '-':
        return 0
    if 'k' in text:
        try:
            return int(float(text.replace('k', '')) * 1000)
        except ValueError:
            pass
    nums = re.findall(r'\d+(?:\.\d+)?', text)
    if not nums:
        return 0
    try:
        return int(float(nums[0]))
    except ValueError:
        return 0


def get_field(row, name):
    for key in FIELD_ALIASES.get(name, [name]):
        if key in row and row[key] not in (None, ''):
            return row[key]
    return ''


def normalize_row(row):
    return {
        'title': str(get_field(row, 'title') or '').strip(),
        'price': str(get_field(row, 'price') or 'N/A').strip(),
        'reviews': clean_number(get_field(row, 'reviews')),
        'sold_24h': clean_number(get_field(row, 'sold_24h')),
        'badge': str(get_field(row, 'badge') or '').strip(),
    }


def unique_by_title(rows):
    seen = set()
    out = []
    for row in rows:
        key = row['title'].lower().strip()
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out


def top_rows(rows, key, limit=10):
    return sorted(rows, key=lambda r: r[key], reverse=True)[:limit]


def print_section(title, rows):
    print(title)
    if not rows:
        print('- No rows available')
        print()
        return
    for row in rows:
        print(
            f"- {row['title']} | Giá: {row['price']} | Rev: {row['reviews']} | "
            f"Sold 24H: {row['sold_24h']} | Badge: {row['badge'] or '-'}"
        )
    print()


def analyze(csv_file):
    path = Path(csv_file).expanduser()
    print(f"# Research Digest\n")
    print(f"- Source file: {path}\n")

    with path.open('r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        raw_rows = list(reader)

    if not raw_rows:
        print('No data rows found.')
        return

    normalized = [normalize_row(row) for row in raw_rows]
    normalized = [row for row in normalized if row['title']]
    deduped = unique_by_title(normalized)

    top_sales = top_rows(deduped, 'sold_24h', limit=10)
    top_reviews = top_rows(deduped, 'reviews', limit=10)
    top_badges = [row for row in deduped if row['badge']][:10]

    merged_candidates = unique_by_title(top_sales + top_reviews + top_badges)

    print(f"- Raw rows: {len(raw_rows)}")
    print(f"- Normalized rows: {len(normalized)}")
    print(f"- Unique listings: {len(deduped)}")
    print()

    print_section('## Top Sales Candidates', top_sales)
    print_section('## Top Review Candidates', top_reviews)
    print_section('## Badge Candidates', top_badges)
    print_section('## Merged Candidate Set', merged_candidates)

    print('## Analysis Notes')
    print('- Seasonal interpretation is not applied in this script.')
    print('- Tactical classification is not assigned in this script.')
    print('- Use the merged candidate set as the primary shortlist for agent judgment.')
    print('- Apply `references/tactical-classification.md` to classify Defender / Midfielder / Forward.')
    print('- Exclude IP-risk, stale, or out-of-season patterns during final analysis.')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python matrix_generator.py <csv-file>')
    else:
        try:
            analyze(sys.argv[1])
        except Exception as exc:
            print(f'Error reading file: {exc}')
            sys.exit(1)
