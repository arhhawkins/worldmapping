# Worldmapping

An interactive historical atlas: drag a slider from 3400 BCE to today and watch the world's borders change.

This is a rough prototype. It's one web page (`index.html`) and one data file (`data.json`).

## Try it

The page loads `data.json` with `fetch`, so opening `index.html` straight from your files won't work. Run a tiny local server instead:

```sh
python3 -m http.server 8000
```

Then open http://localhost:8000.

Or turn on **GitHub Pages** (Settings → Pages → Deploy from branch → `main`, root) to get a public link.

## What it does

- **Slider:** 3400 BCE to 2024 CE. The scale is stretched so recent centuries get more room.
- **‹ / ›:** jump to the previous or next year a border changed. **▶** plays through them.
- **Pinch, scroll or drag** to zoom and pan.
- **Tap a state** to see its name, the years it was on the map, and a Wikipedia link.

## How it's built

- [d3](https://d3js.org) (loaded from a CDN) draws the map on a `<canvas>` using the Equal Earth projection.
- `data.json` is a shrunk-down version of the 170 MB Cliopatria dataset. Shapes are simplified and coordinates are rounded to a 0.05° grid:
  - `q`: grid size (coordinates are stored as degrees × q)
  - `names`: `[name, colour index, Wikipedia title]`
  - `items`: `[name index, from year, to year, label lon, label lat, area km², polygons]`
  - `land`: coastline polygons
  - Each ring is `[x0, y0, dx1, dy1, ...]`: the first point, then the step to each next point.

## Known rough spots / ideas to work on

- **Data cleanup:** some names are wrong or oddly written. For example, the Mali Federation still shows after 1960, and Russia appears as "(Russian Federation)".
- **Coastlines are a placeholder** from historical-basemaps, whose license doesn't suit a product we sell. Swap in [Natural Earth](https://github.com/nvkelso/natural-earth-vector) (public domain).
- **Simplified shapes:** small islands and states look rough.
- **Labels overlap** in busy regions like Europe and crowd the modern end.
- **Not built yet:** events, guided tours, fuzzy/uncertain borders. Nothing is fact-checked.
- **No build script yet** for regenerating `data.json` from the raw data.

## Credits

Borders: [Cliopatria](https://github.com/Seshat-Global-History-Databank/cliopatria), Seshat Global History Databank, licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Shapes simplified for this prototype.
