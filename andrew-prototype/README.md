# Andrew's version of the prototype

A second take on Sam's prototype in the repo root. It works the same way: Cliopatria borders, an atlas palette, a slider from 3400 BCE to 2024, ‹ › to step through border changes, ▶ to play them, pinch/scroll zoom, and tap a state for its name, years and Wikipedia link.

**To try it, open `index.html` straight from your files.** You don't need a local server, and it works without an internet connection (only the fonts need one).

## How it differs from Sam's version

- **One self-contained file.** The border data, coastlines and d3 are all inside `index.html` (about 9.6 MB). Sam's version loads `data.json` with `fetch`, so it needs a server.
- **Natural Earth coastlines** (50m land, public domain) replace the historical-basemaps placeholder, whose licence doesn't suit a product we sell.
- **Opens on 117 CE**, framed on the Old World from the Atlantic to China, so the Roman Empire at its height fills the screen.
- **Engraved-style waterlines:** several thin strokes follow each coast out to sea, like an old printed atlas.
- **Phone layout (under 560px wide):** the slider gets its own row above the buttons, and every other date label under it is hidden so they don't overlap.
- **Natural Earth projection** (`d3.geoNaturalEarth1`) instead of Equal Earth.
- **Colouring:** states that touch at the same time never share a colour, and each state keeps one colour for its whole life.
- **A build script**, `tools/build_andrew_prototype.py`, regenerates the page from the raw data.

## Rebuilding

The raw data goes in `raw/`, which is gitignored. The script's docstring lists the download commands (Cliopatria, Natural Earth, d3). Then, from the repo root:

```sh
pip install shapely
python3 tools/build_andrew_prototype.py
```

Edit `template.html`, not `index.html`. The build fills in the template's placeholders and refuses to write a page of 10 MB or more.

## Rough spots (mostly shared with Sam's version)

- Cliopatria data quirks: in 1997 the Mali Federation and "(British Empire)" still show, and "Kingdom of Great Britain" labels a patch of Arabia.
- Labels crowd in Europe and can run off the edge of the screen.
- No events or tours yet. Nothing is fact-checked.

## Credits

Borders: [Cliopatria](https://github.com/Seshat-Global-History-Databank/cliopatria), Seshat Global History Databank, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Coastlines: [Natural Earth](https://www.naturalearthdata.com), public domain. [d3](https://d3js.org), ISC licence.
