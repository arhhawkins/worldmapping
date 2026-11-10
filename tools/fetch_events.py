#!/usr/bin/env python3
"""Make andrew-prototype/events.json: major and medium historical events for the map.

Source: Wikidata (CC0). Each event needs a date, a place and an English Wikipedia article.
"How big" is the number of Wikipedia language editions with an article on it (sitelinks),
judged against its own era, since recent events get far more articles than ancient ones.

  python3 tools/fetch_events.py            # use raw/wd_events.json if it's there, else fetch
  python3 tools/fetch_events.py --refetch  # query Wikidata again (a few minutes)
"""
import json
import math
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw/wd_events.json"
OUT = ROOT / "andrew-prototype/events.json"
FIXES = ROOT / "andrew-prototype/event-fixes.json"   # hand corrections from the fact-check
NOW = 2026

# Wikidata classes (an event is an instance of one, or of a direct subclass), with a short kind
CLASSES = {
    "Q178561": "battle", "Q188055": "siege", "Q198": "war", "Q131569": "treaty", "Q10931": "revolution",
    "Q124734": "rebellion", "Q45382": "coup", "Q3882219": "assassination", "Q7944": "earthquake",
    "Q7692360": "eruption", "Q3839081": "disaster", "Q44512": "epidemic", "Q12184": "pandemic",
    "Q2401485": "expedition", "Q3002150": "massacre", "Q8065": "disaster", "Q2223653": "attack",
    "Q1006311": "war", "Q8016240": "war", "Q103495": "war", "Q350604": "war", "Q177716": "invasion",
    "Q2135540": "genocide", "Q868557": "fire", "Q168983": "fire", "Q3241045": "epidemic",
    "Q1361229": "conquest", "Q1323212": "operation", "Q645883": "operation", "Q1261499": "battle",
    "Q4688003": "battle", "Q273120": "protest", "Q1139665": "assassination", "Q625994": "convention",
    "Q1072326": "congress",
}
# Kinds that only make the map when they are major (keeps the map suitable for kids and uncluttered)
MAJOR_ONLY = {"attack", "massacre", "genocide", "protest", "fire"}
# Older caches used longer kind names
ALIASES = {"terrorist attack": "attack", "natural disaster": "disaster", "armed conflict": "war",
           "war of independence": "war", "civil war": "war", "world war": "war", "military operation": "operation",
           "naval battle": "battle", "aerial battle": "battle", "political murder": "assassination",
           "disease outbreak": "epidemic", "conflagration": "fire"}
# Events left out by hand, with the reason (from the fact-check)
EXCLUDE = {
    "Q3119132": "overview of all India-Pakistan wars; Wikidata gives it a 2026 start date",
}
# Order used to pick one kind when an event has several
# (battles are also "armed conflicts", which count as war, so the specific kinds come first)
KIND_ORDER = ["battle", "siege", "invasion", "conquest", "revolution", "war", "treaty", "convention", "congress",
              "assassination", "coup", "rebellion", "expedition", "pandemic", "epidemic", "earthquake",
              "eruption", "disaster", "fire", "operation", "protest", "attack", "massacre", "genocide"]


# A "location" that is a whole country or region would put the dot at its middle (the Russian
# Revolution in Siberia, the Boxer Rebellion in the Gobi), so those locations are ignored.
REGION_TYPES = " ".join("wd:" + q for q in (
    "Q6256", "Q3624078", "Q3024240", "Q5107", "Q82794", "Q7275", "Q1620908", "Q15642541", "Q35657",
    "Q107390", "Q1250464", "Q10864048", "Q417175", "Q28171280", "Q1048835", "Q56061", "Q15617994",
    "Q1763527", "Q12959225", "Q2221906", "Q512187", "Q34876", "Q13220204", "Q1078765", "Q164142",
    "Q3359412", "Q839954", "Q23442", "Q46831", "Q8502", "Q4022", "Q165", "Q1322134", "Q9430"))


def sparql(query):
    url = "https://query.wikidata.org/sparql?" + urllib.parse.urlencode({"query": query})
    req = urllib.request.Request(url, headers={"Accept": "application/sparql-results+json",
                                               "User-Agent": "AtlasOfTimeBuild/0.1 (educational map prototype)"})
    for attempt in range(3):
        try:
            return json.load(urllib.request.urlopen(req, timeout=90))["results"]["bindings"]
        except Exception as ex:  # timeouts happen on big classes; retry
            print("retry", ex, file=sys.stderr)
            time.sleep(5)
    return []


def fetch():
    rows = {}
    for cls, kind in CLASSES.items():
        q = """SELECT ?e ?eLabel ?eDescription ?sl ?pt ?st ?et ?coord ?locCoord ?article WHERE {
 ?e wdt:P31/wdt:P279? wd:%s . ?e wikibase:sitelinks ?sl . FILTER(?sl >= 15)
 OPTIONAL{?e wdt:P585 ?pt} OPTIONAL{?e wdt:P580 ?st} OPTIONAL{?e wdt:P582 ?et}
 OPTIONAL{?e wdt:P625 ?coord}
 OPTIONAL{?e wdt:P276 ?loc. ?loc wdt:P625 ?locCoord.
   FILTER NOT EXISTS { ?loc wdt:P31 ?big . VALUES ?big { %s } } }
 ?article schema:about ?e; schema:isPartOf <https://en.wikipedia.org/> .
 SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } }""" % (cls, REGION_TYPES)
        for b in sparql(q):
            v = {k: x["value"] for k, x in b.items()}
            qid = v["e"].rsplit("/", 1)[1]
            r = rows.setdefault(qid, {"qid": qid, "name": v.get("eLabel"), "desc": v.get("eDescription", ""),
                                      "sl": int(v["sl"]), "kinds": set(), "pt": set(), "st": set(), "et": set(),
                                      "coord": set(), "loc": set(), "article": v["article"]})
            r["kinds"].add(kind)
            for key, src in (("pt", "pt"), ("st", "st"), ("et", "et"), ("coord", "coord"), ("loc", "locCoord")):
                if v.get(src):
                    r[key].add(v[src])
        print(kind, len(rows), file=sys.stderr)
        time.sleep(1)
    out = []
    for r in rows.values():
        for k in ("kinds", "pt", "st", "et", "coord", "loc"):
            r[k] = sorted(r[k])
        out.append(r)
    RAW.write_text(json.dumps(out, ensure_ascii=False))
    return out


def year(s):
    """Year in the map's numbering (-490 = 490 BCE, no year 0). The query service writes dates
    in astronomical numbering, where 0000 is 1 BCE and -0489 is 490 BCE, so BCE years shift by one."""
    if not s or s[0] not in "-+0123456789":
        return None   # Wikidata "unknown value"
    y = int(s.lstrip("-+").split("-")[0])
    if s.startswith("-"):
        return -(y + 1)
    return -1 if y == 0 else y


def point(s):
    m = re.match(r"Point\(([-\d.eE]+) ([-\d.eE]+)\)", s)
    return (float(m.group(1)), float(m.group(2))) if m else None


def place(r):
    """Own coordinates, or the location's when there is one clear place; None for events spread worldwide."""
    own = [p for p in map(point, r["coord"]) if p]
    if own:
        return own[0]
    locs = [p for p in map(point, r["loc"]) if p]
    if not locs:
        return None
    lon = sum(p[0] for p in locs) / len(locs)
    lat = sum(p[1] for p in locs) / len(locs)
    if max(math.hypot(p[0] - lon, p[1] - lat) for p in locs) > 4:
        return None
    return lon, lat


def threshold(y):
    """Sitelinks needed for (medium, major) in a given year: lower in the past, where fewer articles exist."""
    if y < 0:
        return 15, 40
    if y < 500:
        return 18, 45
    if y < 1500:
        return 22, 55
    if y < 1800:
        return 26, 60
    if y < 1946:
        return 34, 70
    return 45, 85


def main():
    rows = fetch() if ("--refetch" in sys.argv or not RAW.exists()) else json.loads(RAW.read_text())
    fixes = json.loads(FIXES.read_text())["fixes"] if FIXES.exists() else {}
    events, skipped = [], {}
    for r in rows:
        name = r["name"] or ""
        if re.fullmatch(r"Q\d+", name) or r["qid"] in EXCLUDE:
            continue
        # overview articles ("India–Pakistan wars and conflicts") aren't one event in one place
        if re.search(r"\bwars and conflicts\b|\bwars and battles\b|^list of", name, re.I):
            continue
        starts = [y for y in map(year, r["st"]) if y is not None]
        points = [y for y in map(year, r["pt"]) if y is not None]
        ends = [y for y in map(year, r["et"]) if y is not None and y <= NOW]
        if starts:
            y0 = min(starts)          # a start time beats a point in time (wars sometimes carry odd ones)
        elif points:
            y0 = min(points)
        else:
            skipped["no date"] = skipped.get("no date", 0) + 1
            continue
        if not -3400 <= y0 <= NOW:
            continue
        raw_kinds = {ALIASES.get(k, k) for k in r["kinds"]}
        kinds = [k for k in KIND_ORDER if k in raw_kinds] or ["event"]
        ongoing = starts and not r["et"] and kinds[0] == "war" and y0 >= 2000 and "offensive" not in name.lower()
        y1 = max(ends) if ends else (NOW if ongoing else y0)
        y1 = max(y0, min(y1, NOW))
        # A treaty is an event on the day it's signed (its end date is when it lapsed), and anything
        # lasting over a dozen years would sit on the map for decades, so those show at their start only.
        if kinds[0] in ("treaty", "convention", "congress") or y1 - y0 > 12:
            y1 = y0
        fx = fixes.get(r["qid"], {}).get("fix")
        ll = (fx["lon"], fx["lat"]) if isinstance(fx, dict) and "lat" in fx else place(r)
        if not ll:
            skipped["no single place"] = skipped.get("no single place", 0) + 1
            continue
        med, big = threshold(y0)
        tier = 2 if r["sl"] >= big else 1 if r["sl"] >= med else 0
        grim = raw_kinds & MAJOR_ONLY or re.search(r"massacre|pogrom|genocide|bombing|attack", name, re.I)
        if tier == 0 or (grim and tier < 2):
            continue
        events.append({"id": r["qid"], "name": name[0].upper() + name[1:], "kind": kinds[0], "tier": tier,
                       "y0": y0, "y1": y1, "lon": round(ll[0], 2), "lat": round(ll[1], 2), "sl": r["sl"],
                       "desc": r["desc"], "wiki": r["article"].rsplit("/wiki/", 1)[1]})
    # hand fixes: better places, names, kinds and dates, or "drop"
    kept = []
    for e in events:
        fx = fixes.get(e["id"], {}).get("fix")
        if fx == "drop":
            continue
        if isinstance(fx, dict):
            e.update({k: v for k, v in fx.items() if k in ("name", "desc", "kind", "lat", "lon", "y0", "y1")})
        kept.append(e)
    events = kept
    events.sort(key=lambda e: (e["y0"], -e["sl"]))
    OUT.write_text(json.dumps({"source": "Wikidata (CC0), via tools/fetch_events.py", "events": events},
                              ensure_ascii=False, indent=0))
    print(f"{len(events)} events ({sum(e['tier'] == 2 for e in events)} major), skipped {skipped}")


if __name__ == "__main__":
    main()
