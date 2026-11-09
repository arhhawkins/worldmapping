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

## Atlas of Time (the game prototype)

**Open `game.html`**, which is also self-contained. It turns the atlas into a game with two modes:

- **Adventure:** start in 3400 BCE. Tap the pins, play challenges to earn ✦ Insight, and spend 70 to unlock the next checkpoint (3200 BCE, then 3000 BCE). The map sweeps forward and shows what's new. You earn +30 for any new challenge and +10 more for getting it right first time; replays earn nothing. The Journal lists everything, and has Restart.
- **Free roam:** the atlas with every discovery's story open, plus an endless **When Am I?** (guess the year of a map).

Three mini-games:

- **Two Truths & a Lie:** pick the false claim.
- **Map Detective:** tap a *place* (within a few hundred km counts, and a miss tells you which way to go) or a whole *state* from the border data. It has hints, a list-based alternative and "Show me".
- **When Am I?:** the map at a secret year, with the year hidden. Guess when it is.

Progress saves in the browser (`localStorage`), so a refresh or coming back later picks up where you left off.

### Files

- `game-content.json` holds all the checkpoints, discoveries, challenges and sources. **Edit this to change the game.** Every item is `"status": "draft"` and shows a "Draft – not yet fact-checked" tag until a person checks it against its sources and sets it to `"reviewed"`.
- `game-template.html` is the page's code (plain JavaScript and d3). It copies the atlas's map code rather than sharing it, so the atlas stays untouched.
- `game.html` is built output, like `index.html`. Don't edit it by hand.
- `../docs/game-plan.md` is the game plan, revised to v0.2 with what changed while building this (see its "Revision notes").

### Rebuilding after an edit

```sh
python3 tools/build_andrew_prototype.py --fast
```

`--fast` reuses the processed borders in `raw/build-cache/` and takes a few seconds; the first build takes about 2 minutes. The build checks `game-content.json` first and stops with a list of problems if it finds any: missing sources, a state target that isn't on the map at its checkpoint, a When Am I? range that would show the future, or a checkpoint that a player could never earn enough Insight to unlock.

### Game rough spots

- Only Chapter 1's first three checkpoints exist, and no content has been fact-checked yet.
- Then / Now, the History Passport and optional unlocks aren't built. Insight left over at 3000 BCE has nothing to spend it on yet.
- Before 3000 BCE the border data has very few states, so When Am I? in Chapter 1 is mostly reading whether Elam, Egypt and the Indus have appeared.
- The map code is duplicated between `template.html` and `game-template.html`. Two fixes made for the game also apply to the atlas, but haven't been copied there: keeping the view on resize or rotation, and skipping waterlines while the map moves.

## Rough spots (mostly shared with Sam's version)

- Cliopatria data quirks: in 1997 the Mali Federation and "(British Empire)" still show, and "Kingdom of Great Britain" labels a patch of Arabia.
- Labels crowd in Europe and can run off the edge of the screen.
- No events or tours yet. Nothing is fact-checked.

## Credits

Borders: [Cliopatria](https://github.com/Seshat-Global-History-Databank/cliopatria), Seshat Global History Databank, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Coastlines: [Natural Earth](https://www.naturalearthdata.com), public domain. [d3](https://d3js.org), ISC licence.
