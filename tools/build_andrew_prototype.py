#!/usr/bin/env python3
"""Build andrew-prototype/index.html from the raw data.

Needs (both go in raw/, which is gitignored):
  raw/cliopatria/cliopatria_polities_only_v021.geojson
      git clone --depth 1 https://github.com/Seshat-Global-History-Databank/cliopatria.git raw/cliopatria
      cd raw/cliopatria && unzip cliopatria.geojson.zip
  raw/ne_50m_land.geojson
      curl -o raw/ne_50m_land.geojson https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_land.geojson
  raw/d3.min.js   (inlined so the page works with no network)
      curl -o raw/d3.min.js https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js

Run from the repo root:
  pip install shapely
  python3 tools/build_andrew_prototype.py            # full build (about 2 minutes)
  python3 tools/build_andrew_prototype.py --fast     # reuse the processed borders in raw/build-cache/

Output, each one self-contained page (just under 10 MB) that works straight from your files:
  andrew-prototype/index.html   the atlas         (from template.html)
  andrew-prototype/game.html    Atlas of Time     (from game-template.html + game-content.json)

The build checks game-content.json first and stops with a list of problems if anything is wrong,
including any checkpoint a player could never earn enough Insight to unlock.
"""
import collections
import json
import sys
from pathlib import Path

from shapely.geometry import shape, mapping
from shapely.strtree import STRtree

ROOT = Path(__file__).resolve().parent.parent
CLIO = ROOT / "raw/cliopatria/cliopatria_polities_only_v021.geojson"
LAND = ROOT / "raw/ne_50m_land.geojson"
TEMPLATE = ROOT / "andrew-prototype/template.html"
OUT = ROOT / "andrew-prototype/index.html"
GAME_TEMPLATE = ROOT / "andrew-prototype/game-template.html"
GAME_CONTENT = ROOT / "andrew-prototype/game-content.json"
GAME_OUT = ROOT / "andrew-prototype/game.html"
CACHE = ROOT / "raw/build-cache"
D3 = ROOT / "raw/d3.min.js"
MAX_BYTES = 10_000_000

Q = 20             # coordinate grid: degrees x 20, so 0.05 degree steps
COLOURS = 8        # size of the atlas palette
TOL_BIG, TOL_SMALL = 0.2, 0.09   # simplification, degrees (keeps the page under 10 MB)


def encode(ring):
    """First point, then the step to each next point, on the Q grid."""
    out, px, py = [], 0, 0
    for x, y in ring:
        X, Y = round(x * Q), round(y * Q)
        if out and X == px and Y == py:
            continue
        out += [X - px, Y - py]
        px, py = X, Y
    return out


def simplify_ring(coords, n_points):
    line = shape({"type": "LineString", "coordinates": coords})
    tol = TOL_BIG if n_points > 40 else TOL_SMALL
    return list(line.simplify(tol).coords)


def build_polities():
    data = json.load(open(CLIO))
    feats = [f for f in data["features"] if f["properties"]["Type"] == "POLITY"]
    names, index, wiki = [], {}, []
    items, buffered, meta = [], [], []

    for f in feats:
        p = f["properties"]
        name = p["Name"]
        if name not in index:
            index[name] = len(names)
            names.append(name)
            wiki.append(p["Wikipedia"] or "")
        g = shape(f["geometry"])
        if not g.is_valid:
            g = g.buffer(0)
        first = g.simplify(0.04 if p["Area"] > 20000 else 0.015, preserve_topology=True)
        if first.is_empty:
            continue
        buffered.append(g.buffer(0.05))
        meta.append((index[name], p["FromYear"], p["ToYear"]))

        m = mapping(first)
        polys = [m["coordinates"]] if m["type"] == "Polygon" else m["coordinates"]
        out_polys = []
        for poly in polys:
            rings = []
            for ring in poly:
                ring = [list(pt) for pt in ring]
                if len(ring) < 4:
                    continue
                enc = encode(simplify_ring(ring, len(ring)))
                if len(enc) >= 8:
                    rings.append(enc)
            if rings:
                out_polys.append(rings)
        if out_polys:
            items.append([index[name], p["FromYear"], p["ToYear"], out_polys])

    # Colour so that states touching at the same time never share a colour,
    # and each state keeps one colour for its whole life.
    tree = STRtree(buffered)
    adj = collections.defaultdict(set)
    for i, g in enumerate(buffered):
        for j in tree.query(g):
            if j <= i:
                continue
            a, b = meta[i], meta[j]
            if a[0] == b[0]:
                continue
            if a[1] <= b[2] and b[1] <= a[2] and g.intersects(buffered[j]):
                adj[a[0]].add(b[0])
                adj[b[0]].add(a[0])
    colour = {}
    for n in sorted(range(len(names)), key=lambda n: -len(adj[n])):
        used = {colour[x] for x in adj[n] if x in colour}
        free = [c for c in range(COLOURS) if c not in used]
        colour[n] = free[n % len(free)] if free else n % COLOURS

    return {
        "names": names,
        "wiki": wiki,
        "color": [colour.get(i, 0) for i in range(len(names))],
        "f": items,
        "q": Q,
    }


def build_land():
    data = json.load(open(LAND))
    polys = []
    for f in data["features"]:
        g = shape(f["geometry"]).simplify(0.03)
        parts = g.geoms if g.geom_type == "MultiPolygon" else [g]
        for p in parts:
            rings = [encode(list(p.exterior.coords))] + [encode(list(r.coords)) for r in p.interiors]
            rings = [r for r in rings if len(r) >= 8]
            if rings:
                polys.append(rings)
    return polys


def validate_content(content, polities):
    """Return a list of problems with the game content (empty when it's fine)."""
    errs = []
    cps = content["checkpoints"]
    cp_ids = [c["id"] for c in cps]
    disc = {d["id"]: d for d in content["discoveries"]}
    ids = cp_ids + list(disc) + [c["id"] for c in content["challenges"]]
    for dup in {i for i in ids if ids.count(i) > 1}:
        errs.append(f"duplicate id: {dup}")
    years = [c["year"] for c in cps]
    if years != sorted(years):
        errs.append("checkpoints must be in date order")
    names = polities["names"]
    for d in disc.values():
        if d["checkpoint"] not in cp_ids:
            errs.append(f"{d['id']}: unknown checkpoint {d['checkpoint']}")
        if not d.get("sources") or not all(src["url"].startswith("https://") for src in d["sources"]):
            errs.append(f"{d['id']}: needs at least one https source")
        loc = d["location"]
        if not (-90 <= loc["lat"] <= 90 and -180 <= loc["lon"] <= 180):
            errs.append(f"{d['id']}: bad coordinates")
        if d.get("status") not in ("draft", "reviewed"):
            errs.append(f"{d['id']}: status must be draft or reviewed")

    def cp_of(ch):
        if ch.get("discovery"):
            return cp_ids.index(disc[ch["discovery"]]["checkpoint"]) if ch["discovery"] in disc else None
        return cp_ids.index(ch["checkpoint"]) if ch.get("checkpoint") in cp_ids else None

    count = collections.Counter()
    for ch in content["challenges"]:
        cid, kind = ch["id"], ch["type"]
        i = cp_of(ch)
        if i is None:
            errs.append(f"{cid}: needs a known discovery or checkpoint")
            continue
        count[i] += 1
        if kind == "two-truths-lie":
            if len(ch["claims"]) != 3 or ch["lie"] not in (0, 1, 2) or not ch.get("explanation"):
                errs.append(f"{cid}: needs 3 claims, a lie index 0-2 and an explanation")
        elif kind == "map-detective":
            t = ch["target"]
            if t["kind"] == "place":
                if not (0 < t["radiusKm"] <= 1500) or ch["answer"] not in range(len(ch["choices"])):
                    errs.append(f"{cid}: place target needs radiusKm and a valid answer choice")
            elif t["kind"] == "state":
                y = cps[i]["year"]
                on_map = any(names[n] == t["name"] and a <= y <= b for n, a, b, _ in polities["f"])
                if not on_map:
                    errs.append(f"{cid}: '{t['name']}' isn't on the map in {y}")
            else:
                errs.append(f"{cid}: unknown target kind")
        elif kind == "when-am-i":
            a, b = ch["range"]
            if not (a < b <= cps[i]["year"]):
                errs.append(f"{cid}: range must end by its checkpoint year, so it never shows the future")
        else:
            errs.append(f"{cid}: unknown type {kind}")

    rw = content.get("rewards", {})
    if not all(isinstance(rw.get(k), int) for k in ("perfect", "retry", "review")):
        errs.append("rewards needs whole numbers for perfect, retry and review")
        return errs
    if not rw["perfect"] >= rw["retry"] >= rw["review"] > 0:
        errs.append("rewards must go perfect >= retry >= review > 0")

    # No dead ends. Worst case: a player gets every challenge wrong at first, earns nothing,
    # then gets each one right in its review round. The Insight from those reviews before
    # each checkpoint must still cover all the unlock costs up to and including it.
    base = rw["review"]
    earned = spent = 0
    for i in range(1, len(cps)):
        earned += count[i - 1] * base
        spent += cps[i]["cost"]
        if earned < spent:
            errs.append(f"dead end: {cps[i]['id']} needs {spent} Insight in total but only {earned} can be earned before it")
    return errs


def render(template, parts):
    """Fill __NAME__ placeholders in order, with split/join so data is never substituted twice."""
    page = template.read_text()
    out = []
    for key, value in parts:
        head, page = page.split(f"__{key}__", 1)
        out += [head, value]
    out.append(page)
    return "".join(out)


def write(path, page):
    path.write_text(page)
    size = path.stat().st_size
    print(f"Wrote {path.relative_to(ROOT)} ({size / 1e6:.2f} MB)")
    if size >= MAX_BYTES:
        raise SystemExit(f"{path.name} is {size / 1e6:.2f} MB, over the 10 MB limit: raise TOL_BIG/TOL_SMALL")


def main():
    fast = "--fast" in sys.argv[1:]
    if fast and (CACHE / "polities.json").exists():
        polities = json.loads((CACHE / "polities.json").read_text())
        land = json.loads((CACHE / "land.json").read_text())
        print("Reusing processed borders from raw/build-cache/")
    else:
        polities, land = build_polities(), build_land()
        CACHE.mkdir(parents=True, exist_ok=True)
        (CACHE / "polities.json").write_text(json.dumps(polities, separators=(",", ":")))
        (CACHE / "land.json").write_text(json.dumps(land, separators=(",", ":")))

    content = json.loads(GAME_CONTENT.read_text())
    problems = validate_content(content, polities)
    if problems:
        raise SystemExit("game-content.json has problems:\n  " + "\n  ".join(problems))

    # "<\/" keeps any "</script" inside the data from closing the tag early
    js = lambda obj: json.dumps(obj, separators=(",", ":")).replace("</", "<\\/")
    d3 = D3.read_text()
    assert "</script" not in d3
    write(OUT, render(TEMPLATE, [("POLITIES", js(polities)), ("LAND", js(land)), ("D3", d3)]))
    write(GAME_OUT, render(GAME_TEMPLATE, [("POLITIES", js(polities)), ("LAND", js(land)),
                                           ("CONTENT", js(content)), ("D3", d3)]))


if __name__ == "__main__":
    main()
