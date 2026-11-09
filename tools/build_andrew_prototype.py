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

from shapely.geometry import shape
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

Q = 20             # coastline grid: degrees x 20, so 0.05 degree steps
AQ = 100           # border grid: degrees x 100, so 0.01 degree steps (about 1 km)
COLOURS = 8        # size of the atlas palette


def encode(ring, q=Q):
    """First point, then the step to each next point, on the q grid."""
    out, px, py = [], 0, 0
    for x, y in ring:
        X, Y = round(x * q), round(y * q)
        if out and X == px and Y == py:
            continue
        out += [X - px, Y - py]
        px, py = X, Y
    return out


def clean_ring(ring):
    """Ring as (x, y) tuples, with repeats and the closing point dropped."""
    out = []
    for x, y in ring:
        pt = (x, y)
        if not out or out[-1] != pt:
            out.append(pt)
    if len(out) > 1 and out[0] == out[-1]:
        out.pop()
    return out


def oriented(ring, ccw):
    """Outer rings counter-clockwise, holes clockwise, so the page can fill with the
    nonzero rule: parts of one state that overlap then merge instead of cancelling out."""
    area = sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(ring, ring[1:] + ring[:1]))
    return ring if (area > 0) == ccw else ring[::-1]


class Topology:
    """Store every border line once, at full detail, the way TopoJSON does.

    Cliopatria's shapes are cut from one shared mesh: neighbours and a state's
    successive years reuse the exact same points. So each ring is split at the
    junctions (points where three or more lines meet) into arcs, and each arc is
    kept once. Neighbours then draw the very same line, so no slivers or gaps
    open between them, and the page can afford the source's full detail.
    """

    def __init__(self, rings):
        links = collections.defaultdict(set)
        for r in rings:
            for i, a in enumerate(r):
                b = r[(i + 1) % len(r)]
                links[a].add(b)
                links[b].add(a)
        self.junction = {pt for pt, s in links.items() if len(s) != 2}
        self.arcs, self.arc_index = [], {}
        self.rings, self.ring_index = [], {}

    def _arc(self, chain):
        fwd = tuple(chain)
        rev = fwd[::-1]
        key = min(fwd, rev)
        if key not in self.arc_index:
            self.arc_index[key] = len(self.arcs)
            self.arcs.append(key)
        i = self.arc_index[key]
        return i if key == fwd else ~i

    def _loop(self, ring):
        """A ring with no junctions is one closed arc, started at its lowest point."""
        def canon(c):
            m = min(range(len(c)), key=c.__getitem__)
            return c[m:] + c[:m]
        fwd, rev = canon(ring), canon(ring[::-1])
        key = tuple(min(fwd, rev)) + (min(fwd, rev)[0],)
        if key not in self.arc_index:
            self.arc_index[key] = len(self.arcs)
            self.arcs.append(key)
        i = self.arc_index[key]
        return [i if fwd <= rev else ~i]

    def ring(self, ring):
        """Index of this ring in the shared ring list (each ring is a list of arc refs)."""
        cuts = [i for i, pt in enumerate(ring) if pt in self.junction]
        if not cuts:
            refs = self._loop(ring)
        else:
            s = cuts[0]
            r = ring[s:] + ring[:s] + [ring[s]]
            cuts = [i for i, pt in enumerate(r) if pt in self.junction]
            refs = [self._arc(r[a:b + 1]) for a, b in zip(cuts, cuts[1:])]
        key = tuple(refs)
        if key not in self.ring_index:
            self.ring_index[key] = len(self.rings)
            self.rings.append(refs)
        return self.ring_index[key]

    def encoded_arcs(self):
        return [encode(a, AQ) for a in self.arcs]

    def encoded_rings(self):
        """Runs of neighbouring arc refs (5,6,7 or ~7,~6,~5) shrink to [first, count]."""
        out = []
        for refs in self.rings:
            enc, i = [], 0
            while i < len(refs):
                j, step = i, 0
                if i + 1 < len(refs) and (refs[i] >= 0) == (refs[i + 1] >= 0) and abs(refs[i + 1] - refs[i]) == 1:
                    step = refs[i + 1] - refs[i]
                    while j + 1 < len(refs) and refs[j + 1] - refs[j] == step:
                        j += 1
                enc.append([refs[i], (j - i + 1) * step] if j > i else refs[i])
                i = j + 1
            out.append(enc)
        return out


def polygons(geometry):
    return [geometry["coordinates"]] if geometry["type"] == "Polygon" else geometry["coordinates"]


def build_polities():
    data = json.load(open(CLIO))
    feats = [f for f in data["features"] if f["properties"]["Type"] == "POLITY"]
    names, index, wiki = [], {}, []
    items, buffered, meta = [], [], []

    shapes = []   # per feature: polygons of cleaned rings
    for f in feats:
        polys = []
        for poly in polygons(f["geometry"]):
            rings = [clean_ring(r) for r in poly]
            if len(rings[0]) < 3:
                continue
            rings = [oriented(r, i == 0) for i, r in enumerate(rings) if len(r) >= 3]
            polys.append(rings)
        shapes.append(polys)
    topo = Topology([r for polys in shapes for poly in polys for r in poly])

    for f, polys in zip(feats, shapes):
        if not polys:
            continue
        p = f["properties"]
        name = p["Name"]
        if name not in index:
            index[name] = len(names)
            names.append(name)
            wiki.append(p["Wikipedia"] or "")
        g = shape(f["geometry"])
        if not g.is_valid:
            g = g.buffer(0)
        if g.is_empty:
            continue
        buffered.append(g.buffer(0.05))
        meta.append((index[name], p["FromYear"], p["ToYear"]))
        items.append([index[name], p["FromYear"], p["ToYear"],
                      [[topo.ring(r) for r in poly] for poly in polys]])

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
        "aq": AQ,
        "arcs": topo.encoded_arcs(),
        "rings": topo.encoded_rings(),
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
        raise SystemExit(f"{path.name} is {size / 1e6:.2f} MB, over the 10 MB limit: lower AQ")


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
