#!/usr/bin/env python3
"""Build nearby.json (places for the "附近500公尺" sheet) from an Overpass export.

Usage:
  curl -X POST https://overpass-api.de/api/interpreter --data-urlencode "data@tools/nearby_query.overpassql" -o raw.json
  python3 tools/build_nearby.py raw.json nearby.json
Data: © OpenStreetMap contributors, ODbL. Keep the classification in sync with nearCat/nearKind/nearScore in index.html.
"""
import json, math, re, sys, datetime

BBOX = [18.762, 98.952, 18.818, 99.012]  # S, W, N, E: old city, Nimman, Night Bazaar, Jing Jai, airport

def cat(t):
    shop, am = t.get('shop', ''), t.get('amenity', '')
    if am in ('cafe', 'ice_cream') or re.fullmatch(r'coffee|tea|bakery|pastry', shop): return 'cafe'
    if am in ('restaurant', 'fast_food', 'food_court'): return 'food'
    if shop == 'massage' or am == 'spa' or t.get('leisure') == 'spa': return 'spa'
    if am == 'marketplace' or shop in ('mall', 'department_store', 'gift', 'craft'): return 'market'
    return 'sight'

def kind(t, c):
    if t.get('amenity') == 'place_of_worship': return '寺廟'
    if t.get('tourism') == 'museum': return '博物館'
    if t.get('tourism') == 'gallery': return '藝廊'
    if t.get('historic'): return '古蹟'
    if t.get('tourism'): return '景點'
    if c == 'food': return '餐廳・' + t['cuisine'].split(';')[0].replace('_', ' ') if t.get('cuisine') else '餐廳'
    if c == 'cafe': return '烘焙' if t.get('shop') == 'bakery' else '冰品' if t.get('amenity') == 'ice_cream' else '咖啡'
    if c == 'spa': return '按摩'
    if t.get('amenity') == 'marketplace': return '市集'
    return '購物'

def score(t):
    s = 0
    if t.get('wikidata') or t.get('wikipedia'): s += 30
    if t.get('tourism') in ('attraction', 'museum'): s += 20
    if t.get('amenity') == 'place_of_worship': s += 12
    if t.get('historic'): s += 10
    if t.get('name:en') or t.get('name:zh'): s += 4
    if t.get('opening_hours'): s += 3
    if any(t.get(k) for k in ('website', 'contact:website', 'facebook', 'contact:facebook', 'contact:instagram')): s += 3
    if t.get('cuisine'): s += 2
    return s

def name(t):
    for k in ('name:zh-Hant', 'name:zh-TW', 'name:zh', 'name:en', 'name'):
        if t.get(k): return t[k]

def metres(a, b, c, d):
    r = math.pi / 180
    x = math.sin((c - a) * r / 2) ** 2 + math.cos(a * r) * math.cos(c * r) * math.sin((d - b) * r / 2) ** 2
    return 6371000 * 2 * math.atan2(math.sqrt(x), math.sqrt(1 - x))

raw = json.load(open(sys.argv[1], encoding='utf-8'))
items, kept = [], {}
for e in raw['elements']:
    t = e.get('tags', {})
    lat = e.get('lat', e.get('center', {}).get('lat'))
    lng = e.get('lon', e.get('center', {}).get('lon'))
    if lat is None or not t.get('name'): continue
    if t.get('amenity') == 'place_of_worship' and t.get('religion') not in (None, 'buddhist') and not t.get('wikidata'): continue
    n = name(t); key = n.lower()
    if any(metres(lat, lng, a, b) < 80 for a, b in kept.get(key, [])): continue  # same place mapped twice
    kept.setdefault(key, []).append((lat, lng))
    c = cat(t)
    wiki = t.get('wikidata') or t.get('wikipedia', '')
    desc = (t.get('description:zh') or t.get('description:en') or t.get('description') or '')[:200]
    items.append([n, t['name'] if t['name'] != n else '', round(lat, 5), round(lng, 5), c, kind(t, c), score(t), t.get('opening_hours', '')[:60], wiki, desc, t.get('cuisine', '')[:40]])

out = {'source': '© OpenStreetMap contributors (ODbL)', 'built': datetime.date.today().isoformat(), 'bbox': BBOX,
       'fields': ['name', 'local', 'lat', 'lng', 'cat', 'kind', 'score', 'hours', 'wiki', 'desc', 'cuisine'], 'items': items}
json.dump(out, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(len(items), 'places')
