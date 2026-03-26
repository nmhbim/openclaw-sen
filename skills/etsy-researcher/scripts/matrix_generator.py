#!/usr/bin/env python3
import csv
import re
import sys
from datetime import datetime
from pathlib import Path


IP_TERMS = ['disney', 'marvel', 'pokemon', 'logo', 'naruto', 'ghibli']
EVENT_MONTHS = {
    'valentine': [1, 2],
    'easter': [2, 3, 4],
    'bunny': [2, 3, 4],
    'mother': [3, 4, 5],
    'mom': [3, 4, 5],
    'spring': [2, 3, 4, 5],
    'st patrick': [2, 3],
    'nurse week': [4, 5],
    'teacher appreciation': [4, 5],
    'graduation': [4, 5, 6],
    'back to school': [7, 8, 9],
    'halloween': [8, 9, 10],
    'spooky': [8, 9, 10],
    'witch': [8, 9, 10],
    'thanksgiving': [9, 10, 11],
    'christmas': [10, 11, 12],
    'santa': [10, 11, 12],
}
FORWARD_BADGES = ['bestseller', 'popular now']


FIELD_ALIASES = {
    'title': ['title', 'Title'],
    'price': ['price', 'Price'],
    'reviews': ['reviews', 'Reviews', 'review_count'],
    'sold_24h': ['sold_24h', 'Sold 24H', 'sold24', 'sold_24_hr'],
    'badge': ['badge', 'Badge', 'badges', 'Badges'],
    'sort_type': ['sort_type', 'Sort_Type'],
    'total_sold': ['total_sold', 'Total Sold', 'totalSold'],
    'listing_age_days': ['listing_age_days', 'Listing_Age_Days', 'age_days'],
    'search_position': ['search_position', 'Search_Position', 'position'],
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


def has_ip_risk(title):
    lower = title.lower()
    return any(term in lower for term in IP_TERMS)


def matched_events(title):
    lower = title.lower()
    return [event for event in EVENT_MONTHS if event in lower]


def classify_row(row, current_month):
    title = str(get_field(row, 'title'))
    title_lower = title.lower()
    badge = str(get_field(row, 'badge')).lower()
    sort_type = str(get_field(row, 'sort_type') or 'date_desc').lower()
    reviews = clean_number(get_field(row, 'reviews'))
    sold_24h = clean_number(get_field(row, 'sold_24h'))
    total_sold = clean_number(get_field(row, 'total_sold'))
    listing_age_days = clean_number(get_field(row, 'listing_age_days'))
    search_position = clean_number(get_field(row, 'search_position')) or 9999

    if has_ip_risk(title):
        return 'exclude', 'high', 'possible IP risk'

    events = matched_events(title)
    if events:
        live_events = [e for e in events if current_month in EVENT_MONTHS[e]]
        dead_events = [e for e in events if current_month not in EVENT_MONTHS[e]]
        if dead_events and not live_events and sold_24h == 0:
            return 'exclude', 'medium', 'out-of-season event pattern without fresh sales'
        if live_events and (sold_24h >= 1 or any(b in badge for b in FORWARD_BADGES)):
            return 'midfielder', 'medium', f'event-driven demand with current momentum: {", ".join(live_events)}'

    if listing_age_days and listing_age_days <= 60:
        if sold_24h >= 10:
            return 'forward', 'high', 'new listing with strong recent sales velocity'
        if reviews < 50 and any(b in badge for b in FORWARD_BADGES):
            return 'forward', 'medium', 'new low-review listing with breakout marketplace badge'

    if sold_24h > 5:
        return 'forward', 'medium', 'strong recent sales suggesting short-term breakout potential'

    if total_sold >= 1000 and sold_24h >= 1:
        return 'defender', 'high', 'high total sold with continuing fresh sales'
    if reviews >= 1000 and search_position <= 24:
        return 'defender', 'medium', 'very high reviews with strong search placement'
    if (reviews > 500 or sort_type == 'highest_reviews') and sold_24h == 0 and not any(b in badge for b in FORWARD_BADGES):
        return 'exclude', 'medium', 'possible dead pattern: legacy reviews without clear fresh momentum'
    if reviews > 500 or sort_type == 'highest_reviews':
        return 'defender', 'low', 'high review strength suggests evergreen demand'

    if reviews >= 200:
        return 'midfielder', 'low', 'proven demand but freshness signals are incomplete'

    return 'midfielder', 'low', 'exploratory pattern with limited evidence'


def analyze(csv_file):
    print(f"\n# 📊 Báo Cáo Phân Tích Máy Tính (Từ File: {csv_file})\n")
    path = Path(csv_file).expanduser()
    current_month = datetime.now().month

    try:
        with path.open('r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            data = list(reader)

        if not data:
            print('Chưa có dòng dữ liệu nào.')
            return

        hau_ve = []
        tien_ve = []
        tien_dao = []
        excluded = []

        for row in data:
            tier, confidence, reason = classify_row(row, current_month)
            record = {
                'title': str(get_field(row, 'title') or 'N/A'),
                'price': str(get_field(row, 'price') or 'N/A'),
                'reviews': str(get_field(row, 'reviews') or '0'),
                'sold_24h': str(get_field(row, 'sold_24h') or '-'),
                'confidence': confidence,
                'reason': reason,
            }

            if tier == 'defender':
                hau_ve.append(record)
            elif tier == 'midfielder':
                tien_ve.append(record)
            elif tier == 'forward':
                tien_dao.append(record)
            else:
                excluded.append(record)

        hau_ve.sort(key=lambda x: clean_number(x['reviews']), reverse=True)
        tien_ve.sort(key=lambda x: clean_number(x['sold_24h']), reverse=True)
        tien_dao.sort(key=lambda x: clean_number(x['sold_24h']), reverse=True)

        print('## 1. 🏟 Bảng Trận Địa Bóng Đá (Top Lọc Bằng Thuật Toán)')
        print('| Vị Trí | Sản Phẩm | Giá | Lượt Đánh Giá | Sold 24H | Confidence | Lý do |')
        print('|--------|----------|-----|---------------|----------|------------|-------|')

        for item in hau_ve[:3]:
            print(f"| 🛡 Hậu Vệ | {item['title'][:30]}... | {item['price']} | {item['reviews']} | {item['sold_24h']} | {item['confidence']} | {item['reason']} |")
        for item in tien_ve[:3]:
            print(f"| 🏃‍♂️ Tiền Vệ | {item['title'][:30]}... | {item['price']} | {item['reviews']} | {item['sold_24h']} | {item['confidence']} | {item['reason']} |")
        for item in tien_dao[:3]:
            print(f"| ⚡️ Tiền Đạo | {item['title'][:30]}... | {item['price']} | {item['reviews']} | {item['sold_24h']} | {item['confidence']} | {item['reason']} |")

        print('\n## 2. 🚫 Danh Sách Loại Bỏ')
        if excluded:
            for item in excluded[:5]:
                print(f"- {item['title'][:80]} — {item['reason']} ({item['confidence']})")
        else:
            print('- Không có listing nào bị loại ở lượt quét này.')

        print('\n## 3. ⚔️ Lệnh Tấn Công (Dựa theo AI Agent)')
        print('> Dùng bảng trên để ưu tiên: Tiền Đạo cho đòn lướt sóng, Tiền Vệ cho mùa vụ sắp tới, Hậu Vệ cho ngách bền vững.')
        print('> Nếu confidence thấp, cần kiểm chứng thêm bằng dữ liệu bổ sung hoặc lượt quét sâu hơn.')
        print()

    except Exception as e:
        print(f'Lỗi đọc file: {e}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Sử dụng: python matrix_generator.py <duong_dan_file.csv>')
    else:
        analyze(sys.argv[1])
