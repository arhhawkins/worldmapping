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
  python3 tools/build_andrew_prototype.py

Output: andrew-prototype/index.html, one self-contained page (just under 10 MB)
that works straight from your files, no local server needed.
"""
import collections
import json
from pathlib import Path

from shapely.geometry import shape, mapping
from shapely.strtree import STRtree

ROOT = Path(__file__).resolve().parent.parent
CLIO = ROOT / "raw/cliopatria/cliopatria_polities_only_v021.geojson"
LAND = ROOT / "raw/ne_50m_land.geojson"
TEMPLATE = ROOT / "andrew-prototype/template.html"
OUT = ROOT / "andrew-prototype/index.html"
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


def main():
    # "<\/" keeps any "</script" inside a name from closing the tag early
    polities = json.dumps(build_polities(), separators=(",", ":")).replace("</", "<\\/")
    land = json.dumps(build_land(), separators=(",", ":"))
    d3 = D3.read_text()
    assert "</script" not in d3
    page = TEMPLATE.read_text()
    # split/join so placeholder text inside the data can never be substituted twice
    head, rest = page.split("__POLITIES__")
    mid, rest = rest.split("__LAND__")
    pre_d3, tail = rest.split("__D3__")
    page = head + polities + mid + land + pre_d3 + d3 + tail
    OUT.write_text(page)
    size = OUT.stat().st_size
    print(f"Wrote {OUT} ({size / 1e6:.2f} MB)")
    if size >= MAX_BYTES:
        raise SystemExit(f"Page is {size / 1e6:.2f} MB, over the 10 MB limit: raise TOL_BIG/TOL_SMALL")


if __name__ == "__main__":
    main()
