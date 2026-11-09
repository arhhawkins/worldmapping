# World History Map Game
## Actionable Product & Development Plan

**Working title:** Atlas of Time (placeholder)  
**Version:** 0.2 — First playable prototype  
**Status:** Prototype built: `andrew-prototype/game.html` (see Revision notes)  
**Development approach:** Incremental, modular, non-destructive

---

# Revision notes (v0.2)

Changes made while building the first playable prototype. The rest of the plan is unchanged except where a section says "v0.2".

1. **Free roam is part of the MVP, not a future idea.** The existing atlas already is free roam (slider, borders, tap a state). The game page has two modes sharing one map: **Adventure** (progression) and **Free roam** (everything open). See §20 G.
2. **The real borders are used as gameplay.** The page knows thousands of Cliopatria state shapes and can tell which one was tapped, so Map Detective can ask for a *state* as well as a *place* (§5.2), and a new data-driven mini-game, **When Am I?**, needs no authored questions (§5.7).
3. **The first loop is 3400 → 3200 → 3000 BCE**, not 3400 → 3200. Cliopatria shows 1 state at 3400 BCE (Sumer), 2 at 3200 BCE (+ Elam) and 4 at 3000 BCE (+ Egypt, + Indus). The second jump is the first one where the map visibly fills in (§3.2).
4. **A checkpoint means "the world around year X".** Discoveries attached to it happened roughly within a century or two of X, and their real dates are always shown.
5. **Every authored item is tagged "Draft – not yet fact-checked"** in the interface until a person reviews it (§12, rule 13).
6. **Discovery pins must fill the border data's gaps.** Cliopatria has nothing in the Americas, China or most of Africa before about 1500 BCE, so pins deliberately cover those regions (Liangzhu, Norte Chico) (§12, rule 14).
7. **The technical plan follows this repository**, which is single-file pages plus a Python build script, not a React/TypeScript app. Content lives in one structured JSON file that the build validates (§13).
8. **Open question: who is the main player?** The 60–120-word stories suit teens and adults. A younger audience needs shorter text and more map-tapping (§20 H).

---

# 1. Executive Summary

Build a gamified world history exploration experience centered around an interactive map and timeline.

Players begin around **3400 BCE**, near the emergence of some of the earliest known writing systems, and progress through approximately 5,400 years of recorded history to reach the present.

The central mechanic:

**Explore history → Complete mini-games → Earn points → Unlock time → Discover new eras.**

Players encounter historical figures, events, civilizations, archaeological discoveries, artworks, and geographical mysteries.

By interacting with historical content and successfully completing challenges, they earn a currency called **Insight Points**.

These points unlock additional years on the timeline, historical discoveries, media, and optional exploration content.

The map changes as history unfolds.

### Core design philosophy

**The map is the game board. Time is the progression mechanic. Historical knowledge is the reward.**

The experience should feel like discovering and unlocking an enormous historical world rather than completing a conventional history quiz.

### Important historical consideration

3400 BCE represents a reasonable starting point for a game focused on recorded history, not the beginning of human history.

The interface should acknowledge that humans, civilizations, settlements, and cultures existed long before writing developed.

Eventually, a prehistoric expansion could extend gameplay much further backward.

---

# 2. The Core Gameplay Loop

```text
PLAYER STARTS IN 3400 BCE
          |
          v
EXPLORE HISTORICAL WORLD MAP
          |
          v
DISCOVER HISTORICAL CLUES AND EVENTS
          |
          v
READ STORY / EXAMINE HISTORICAL EVIDENCE
          |
          v
COMPLETE A MINI-GAME
          |
          v
EARN INSIGHT POINTS
          |
          v
CHOOSE HOW TO SPEND POINTS
          |
          +----> UNLOCK EVENTS
          |
          +----> UNLOCK ARTIFACTS / IMAGES
          |
          +----> UNLOCK MAP LAYERS
          |
          +----> ADVANCE TIME
                       |
                       v
              HISTORICAL WORLD CHANGES
                       |
                       v
              NEW DISCOVERIES APPEAR
                       |
                       v
                  REPEAT
```

## Primary player objective

Reach the present day by progressively unlocking historical checkpoints.

## Secondary objectives

- Discover historical events.
- Collect historical artwork and artifacts.
- Complete mini-games.
- Explore different regions of the world.
- Unlock civilizations and historical map layers.
- Collect achievements.
- Discover connections between seemingly unrelated events.
- Build a personal historical collection.

## Desired session lengths

**Quick session:** 3–5 minutes  
**Standard session:** 10–15 minutes  
**Extended exploration:** 20–30 minutes or more

Players should be able to make meaningful progress in short sessions.

---

# 3. Historical Progression and Eras

## 3.1 Timeline structure

The world history timeline should be divided into chapters.

These chapters are navigational conveniences rather than claims that civilizations everywhere entered the same historical era simultaneously.

### Suggested era progression

| Chapter | Years | Era |
|---|---|---|
| 1 | 3400–2500 BCE | Cities, Writing & Early States |
| 2 | 2500–1200 BCE | Bronze Age Civilizations |
| 3 | 1200–500 BCE | Iron Age Transformations |
| 4 | 500 BCE–500 CE | Classical & Interconnected Worlds |
| 5 | 500–1000 CE | New States, Faiths & Connections |
| 6 | 1000–1450 CE | Trade, Scholarship & Expanding Networks |
| 7 | 1450–1650 CE | Ocean Crossings, Encounter & Conquest |
| 8 | 1650–1800 CE | Science, Trade & Revolutions |
| 9 | 1800–1914 CE | Industry, Migration & Empire |
| 10 | 1914–1945 CE | World Wars & Global Transformation |
| 11 | 1945–1991 CE | Decolonization & Cold War |
| 12 | 1991–Present | The Interconnected Present |

These dates are approximate.

## 3.2 Historical checkpoints

Rather than requiring players to unlock every individual year, use curated historical checkpoints.

For example:

```text
3400 BCE — Starting Point
    |
    | +200 years
    v
3200 BCE — New Discoveries
    |
    | +200 years
    v
3000 BCE — New Discoveries
    |
    | +300 years
    v
2700 BCE — New Discoveries
    |
    | +200 years
    v
2500 BCE — Next Chapter
```

As the player moves forward, checkpoints can become more frequent.

Ancient history may advance in jumps of hundreds of years.

Modern history may advance by decades or individual years.

Every checkpoint should introduce something interesting.

**v0.2: prototype checkpoints.** 3400 BCE (start) → 3200 BCE (70 Insight) → 3000 BCE (70 Insight). The border data drives this choice: the map shows 1 state at 3400 BCE, 2 at 3200 BCE and 4 at 3000 BCE, so the jump to 3000 BCE is the first where new civilizations visibly appear. Each checkpoint stands for "the world around that year": its discoveries happened within roughly a century or two of it, and each shows its real date.

### Acceptance criteria

- [ ] Players can see their current historical year.
- [ ] Players can see the next unlockable checkpoint.
- [ ] The required point cost is displayed.
- [ ] The number of years advanced is displayed.
- [ ] Players cannot accidentally skip required progression.
- [ ] Previously unlocked periods remain accessible.
- [ ] The BCE-to-CE transition is correctly handled.
- [ ] Approximate historical dates are appropriately labeled.

**Technical note:** Conventional BCE/CE chronology does not contain a year zero.

---

# 4. Point Economy

## 4.1 Insight Points

Create a single gameplay currency:

**Insight Points**

Players earn Insight through historical activities.

They spend Insight on unlocking additional historical content and advancing time.

Avoid introducing multiple currencies during the MVP.

## 4.2 Suggested initial point values

| Activity | Points |
|---|---:|
| Complete a new mini-game | +30 |
| Correct first attempt | +10 bonus |
| Complete a new optional challenge | +30 |
| Unlock next historical checkpoint | -70 |
| Unlock optional event deep dive | -20 |
| Unlock optional artifact or gallery card | -15 |
| Replay previously completed challenge | 0 |

These values are placeholders and should be adjusted through playtesting.

## 4.3 Progression rules

1. Players earn points for completing a new challenge, even when their first answer is incorrect.
2. Correct answers award bonus points.
3. Every challenge explains the correct answer.
4. Replaying the same question does not repeatedly generate points.
5. Every checkpoint must provide enough opportunities to earn the Insight needed to advance.
6. Players must never become permanently stuck.
7. Historical learning should never require perfect accuracy.

### Example

A player begins at 3400 BCE.

They complete:

- Two Truths & a Lie: +40
- Map Detective: +30
- Then / Now: +40

**Total earned: 110 Insight**

The next checkpoint costs 70 Insight.

The player advances 200 years and retains 40 Insight.

They may spend remaining points on optional content or save them for future progression.

## 4.4 Important balancing principle

The primary objective is learning through exploration, not punishing players for mistakes.

Avoid mechanics that discourage experimentation.

---

# 5. Mini-Games

The mini-games should make the best possible use of the map, timeline, historical writing, and historical imagery.

## 5.1 Two Truths & a Lie

**Priority:** P0 — MVP

### Concept

The player encounters a historical event, person, civilization, geographical location, or artifact.

They read a short historical story.

Then three claims appear.

Two claims are accurate.

One claim is false.

The player must identify the lie.

### Gameplay flow

1. Player selects a historical discovery.
2. A story panel opens.
3. Player reads a short historical narrative.
4. Three statements appear.
5. Player identifies the false statement.
6. The correct answer is revealed.
7. An explanation and historical source are displayed.
8. Insight Points are awarded.

### Recommended content length

Historical story: 60–120 words.

Statements: One or two sentences each.

Explanation: 30–100 words.

### Interface

```text
+------------------------------------+
|        HISTORICAL DISCOVERY        |
|                                    |
|             3200 BCE               |
|                                    |
|    THE EMERGENCE OF EARLY WRITING  |
|                                    |
| [Historical Image / Artifact]      |
|                                    |
| Short historical story...          |
|                                    |
|       WHICH CLAIM IS FALSE?        |
|                                    |
| [ A. Historical Statement ]        |
|                                    |
| [ B. Historical Statement ]        |
|                                    |
| [ C. Historical Statement ]        |
|                                    |
|        INSIGHT REWARD: +40         |
+------------------------------------+
```

### Requirements

- [ ] Three answer choices.
- [ ] Exactly one clearly false statement.
- [ ] Explanation after the answer.
- [ ] Historical source attribution.
- [ ] Points awarded correctly.
- [ ] Completed questions recorded.
- [ ] Responsive mobile interface.
- [ ] Support multiple difficulty levels.

### Historical accuracy requirement

Avoid ambiguous claims, disputed interpretations, misleading absolute statements, or trick questions.

All three claims should be checked against reputable historical sources.

**Initial target:** 12 authored and reviewed rounds.

---

## 5.2 Map Detective

**Priority:** P0 — MVP

### Concept

The player receives a geographical or historical clue and must identify the corresponding location on the map.

This should feel like a historical scavenger hunt.

### Example

A clue describes an ancient civilization that developed around a river system.

The player navigates the map and selects the correct historical region.

### Gameplay flow

1. Historical clue appears.
2. The map becomes interactive.
3. Player explores candidate locations.
4. Player taps a location.
5. The game confirms or rejects the answer.
6. The corresponding historical story appears.
7. Points are awarded.

### Difficulty levels

**Easy:** Candidate location pins are visible.

**Medium:** The player receives regional hints.

**Hard:** Player explores a broader map area before receiving hints.

### Hint system

- Hint 1: Identify the continent or broad region.
- Hint 2: Identify a nearby geographical feature.
- Hint 3: Reveal candidate locations.

### Requirements

- [ ] Display clue overlay.
- [ ] Interactive map selection.
- [ ] Large mobile-friendly targets.
- [ ] Optional hint system.
- [ ] Correct/incorrect feedback.
- [ ] Location information.
- [ ] Historical source reference.
- [ ] Accessible list-based alternative to map interaction.

Avoid requiring pixel-perfect selections of uncertain ancient borders.

**v0.2: two target types.**

- **Place:** the player taps the map, and any tap within a set distance of the target (300–400 km in the prototype) counts. A wrong tap reports roughly how far off it was and which compass direction to try.
- **State:** the player taps a whole state from the border data (for example "the kingdom that united Upper and Lower Egypt"). The targets are large, so there's no pixel-perfect guessing.

State labels and discovery pins are hidden while a Map Detective round is running, because they would give the answer away. The list-based alternative offers the authored choices for a place target, or the states on the map for a state target.

**Initial target:** 12 rounds distributed across several regions.

---

## 5.3 Then / Now

**Priority:** P0 — MVP

### Concept

Compare a historical location, object, map, or landscape with its present-day equivalent.

Use authentic historical evidence whenever possible.

### Example experiences

**Ancient city**

A scholarly reconstruction of an ancient city is compared with present-day archaeological ruins.

**Historical building**

A 19th-century photograph is compared with a modern photograph of the same location.

**Geographical change**

Two historical maps show how a city, coastline, transportation system, or settlement pattern evolved.

### Potential mini-games

- Identify which image is older.
- Find a historical feature that still exists.
- Identify something that has changed.
- Match an ancient artifact with its present-day museum image.
- Predict what an archaeological site looks like today.

### Visual interaction

Use side-by-side images initially.

Where the images are sufficiently aligned, optionally introduce a draggable comparison slider.

### Requirements

- [ ] Two images with descriptions.
- [ ] Historical date or period shown.
- [ ] Source and copyright information.
- [ ] Interactive question.
- [ ] Correct answer explanation.
- [ ] Image accessibility text.
- [ ] Responsive layout.

### Important

Do not present modern artistic reconstructions as contemporary pictures of ancient life.

Clearly distinguish:

- Historic photographs
- Contemporary photographs
- Historical paintings
- Archaeological artifacts
- Scholarly reconstructions
- Modern artistic interpretations

**Initial target:** 9 curated comparisons.

---

## 5.4 Timeline Tangle

**Priority:** P1

### Concept

The player receives several historical events and must arrange them in chronological order.

### Example interface

```text
PLACE THESE EVENTS IN ORDER

[ Historical Event A ]

[ Historical Event B ]

[ Historical Event C ]

        DRAG TO REORDER

           SUBMIT
```

### Possible variations

- Three events for beginners.
- Five events for advanced players.
- Mix events from distant geographical regions.
- Include events that happened around the same time.
- Compare developments that players might incorrectly assume were centuries apart.

### Educational value

Strengthens historical chronology and reinforces the central time progression system.

---

## 5.5 Cause & Consequence

**Priority:** P1

### Concept

Connect historical developments to their consequences.

Players investigate relationships between historical events.

### Potential interactions

- Match a historical development with an outcome.
- Identify factors contributing to an event.
- Arrange a chain of historically supported developments.
- Distinguish correlation from causation.

### Important

Avoid presenting historical events as inevitable or assigning complex events a single simplistic cause.

---

## 5.6 Trade Route Explorer

**Priority:** P2

### Concept

Players uncover historical trade networks using the map.

They identify cities, goods, regions, and historically supported connections.

### Example

A player investigates the historical movement of a commodity through multiple geographical regions.

The corresponding connections gradually appear on the map.

### Features

- Historical network lines.
- Connected cities and trading regions.
- Goods or technologies associated with trade.
- Discovery cards.
- Optional route-completion achievements.

This could become one of the most visually distinctive mini-games because it uses the geographical nature of the app.

---

## 5.7 When Am I?

**Priority:** P0 in the v0.2 prototype

### Concept

The player sees the border map at a secret year, with the state names showing but the year hidden, and drags a guess slider to say when it is. Scoring depends on how close the guess is.

### Why it fits

- It is generated from the border data, so it needs no authored questions and is endless in Free roam.
- It is factual by construction, since it shows the dataset as it is (Cliopatria's known quirks still apply).
- It trains exactly the skill the atlas is about: reading a map as a moment in time.

### Rules in the prototype

- **Adventure:** one 3-round challenge at the 3000 BCE checkpoint, limited to 3400–3000 BCE so it never shows the future. Completing it gives +30, and an average score of 500 or more out of 1000 gives the +10 bonus.
- **Free roam:** endless 5-round games over "All of history" or "Since 1000 CE", with the best score saved.
- Closeness is measured on the slider's stretched scale, so being 100 years off in 1900 counts for more than being 100 years off in 2500 BCE.

---

# 6. Unlockable Content

Organize unlocks into three categories.

## 6.1 Primary progression unlocks

These unlocks are directly related to the player's objective of reaching the present.

### A. Time

The primary unlock.

Players spend Insight to advance to the next historical checkpoint.

### B. Historical eras

New chapters become available as the player advances.

Each era introduces historical content and a new visual identity.

### C. Historical discoveries

New places, events, people, and stories appear on the map.

Core discoveries required for progression must remain accessible.

---

## 6.2 Optional exploration unlocks

### A. Historical event deep dives

Detailed explorations of specific historical topics.

### B. Historical map layers

Possible overlays:

- Historical settlements
- Trade networks
- Migration routes
- Archaeological sites
- Approximate historical political regions
- Historical city locations
- Transportation routes

Historical boundaries and locations must indicate uncertainty when appropriate.

### C. Historical connections

Connections between events, technologies, people, and regions.

### D. Alternative perspectives

Additional context from different geographical regions or historical sources.

---

## 6.3 Collectible unlocks

### A. Historical images

Paintings, drawings, photographs, maps, and archival documents.

### B. Archaeological artifacts

Collectible cards representing objects such as sculptures, writing tablets, ceramics, tools, and other material culture.

### C. Historical map collection

Players collect maps associated with different centuries and civilizations.

### D. Achievements

Examples:

- First Discovery
- First Century Advanced
- Ancient World Explorer
- Cartographer
- Artifact Collector
- Chronology Master
- Global Explorer

### E. Cosmetic unlocks

Possible future rewards:

- Map color palettes
- Historical map frames
- Different timeline themes
- Collection book designs

Cosmetic rewards should not create gameplay advantages.

---

# 7. The Interactive World Map

The map should remain the central interface.

Avoid building a game that uses the map merely as a decorative background.

## 7.1 Map interface

### Header

Display:

- Current historical year
- Current era
- Insight Points
- Progress toward next chapter

### Main map

Display:

- Historical discoveries
- Active mini-games
- Available historical clues
- Previously discovered locations
- Optional historical overlays

### Bottom timeline

Display:

- Current year
- Previous unlocked checkpoints
- Next checkpoint
- Advancement cost
- Locked historical eras

### Discovery panel

When selecting a map marker, show:

- Historical title
- Date
- Story
- Image, when available
- Source
- Mini-game
- Related discoveries

---

# 8. Historical World Transformation

One of the most important experiences is watching the map evolve when advancing through time.

## 8.1 Timeline transition

When the player purchases the next checkpoint:

1. The timeline begins moving forward.
2. The year display changes.
3. Existing map markers transition.
4. New discoveries appear.
5. A short historical context message appears.
6. The player sees what has changed.

### Example

```text
3400 BCE
   |
   | ADVANCE 200 YEARS
   |
   v
3200 BCE

NEW DISCOVERIES AVAILABLE!

+ Early writing practices
+ Developing urban settlements
+ New archaeological evidence
```

## 8.2 Visual treatment

Possible effects:

- Scrolling dates
- Newly illuminated map markers
- Subtle map transitions
- Era-specific colors
- Historical artwork
- Animated trade networks

Transitions should feel rewarding without becoming slow or repetitive.

Include reduced-motion accessibility support.

## 8.3 Historical accuracy

Do not imply that modern countries existed in ancient periods.

Separate modern geographical references from historical political entities.

Do not invent precise historical borders where evidence is insufficient.

---

# 9. The History Passport

**Priority:** P1

Create a personal collection interface that records the player's historical journey.

Working name:

**History Passport** or **Museum Collection**

## Contents

### Discovered historical eras

A visual overview of completed chapters.

### Historical discoveries

Events, places, and people encountered.

### Collected artifacts

Museum-style collectible cards.

### Historical artwork

An image gallery containing unlocked media.

### Completed mini-games

Records of previously solved challenges.

### Achievements

Milestone rewards.

## Design direction

The collection should resemble a beautifully designed museum archive, explorer's journal, or historical atlas.

Potential visual elements:

- Archival paper
- Antique cartographic typography
- Carefully arranged artwork
- Museum-style labels
- Subtle illustrated details

The collection should be enjoyable to browse independently of gameplay.

---

# 10. Additional Gameplay Ideas

## 10.1 One World, One Year

**Priority:** P1

At any unlocked year, the player can explore what was happening in several world regions simultaneously.

For example, selecting a historical date could reveal discoveries across:

- Africa
- East Asia
- South Asia
- Europe
- The Americas
- Oceania

This is especially valuable for demonstrating that history is not a single linear story.

It also makes excellent use of the world map.

---

## 10.2 Historical Ripples

**Priority:** P1

Show connections between historical developments across geographical space and time.

Examples include connections involving:

- Trade
- Migration
- Technology
- Ideas
- Languages
- Political changes
- Environmental developments

When viewing a historical event, related discoveries could become highlighted on the map.

Lines connecting relevant locations illustrate the relationship.

Connections must be evidence-based and distinguish direct influence from broader association.

---

## 10.3 Fact, Myth, or Unknown?

**Priority:** P2

A mini-game exploring the difference between established historical evidence, popular myths, and unresolved historical questions.

Players choose:

- Supported Fact
- Historical Myth
- Still Unknown / Disputed

This teaches historical reasoning rather than simple memorization.

---

## 10.4 Historical Mystery

**Priority:** P2

A short multi-step investigation based on archaeological or historical evidence.

The player:

1. Discovers a clue.
2. Investigates another location.
3. Examines an artifact.
4. Answers questions.
5. Unlocks the historical explanation.

This could become a more substantial adventure mode.

---

## 10.5 Historical Collections

**Priority:** P1

Players complete thematic collections.

Examples:

- Ancient Writing Systems
- Historical Maps
- Early Cities
- Great Libraries
- Ancient Trade Networks
- Historic Architecture
- Exploration and Navigation
- Inventions and Technologies

A completed collection unlocks a badge, visual reward, or optional historical deep dive.

---

## 10.6 Regional Expeditions

**Priority:** P2

Allow players to specialize in a particular geographical region while continuing through the global timeline.

For example:

- Ancient Mesopotamia
- The Nile Valley
- Mesoamerica
- West African Kingdoms
- South Asian Civilizations
- East Asian Civilizations
- Pacific Navigation

These should remain optional.

A player's chosen region should not imply that other regions were historically inactive.

---

## 10.7 Historical Map Comparison

**Priority:** P1

Players compare the same region at different historical checkpoints.

Potential features:

- Side-by-side maps
- Historical and modern layers
- Settlement growth
- Changing transportation networks
- Approximate political boundaries
- Trade route changes

This feature could also operate outside game mode.

---

## 10.8 Collector's Cabinet

**Priority:** P1

Create a visually rich interface where players arrange discovered artifacts, maps, artwork, and historical documents.

It might resemble a virtual museum wall.

Long-term potential:

Players could generate shareable or printable compositions using their collected discoveries.

---

# 11. Historical Content Strategy

This project requires a scalable historical content system.

The same historical discovery should be reusable across multiple features.

## 11.1 One historical discovery, multiple uses

A single historical content record should be capable of appearing as:

- Timeline event
- Map marker
- Historical story
- Mini-game source
- Artifact collection entry
- Then / Now comparison
- Historical connection
- Related discovery

Avoid duplicating historical descriptions throughout the codebase.

## 11.2 Suggested discovery schema

Each discovery should contain:

- Unique ID
- Title
- Short description
- Detailed description
- Historical date or date range
- Approximate-date flag
- Era identifier
- Coordinates or geographical region
- Location precision
- Associated civilizations or peoples
- Themes and categories
- Source references
- Historical image references
- Related discoveries
- Associated mini-games
- Editorial review status

## 11.3 Media information

For each image, preserve:

- Title
- Creator
- Original date or approximate date
- Hosting institution
- Source URL
- Copyright/license information
- Attribution requirements
- Alt text
- Whether the image is an original work or reconstruction

## 11.4 Potential historical content sources

Research appropriate content from:

- Museum collections
- University collections
- Archaeological institutions
- Wikimedia Commons
- Wikidata as a research index
- Library of Congress
- National libraries
- Public-domain archives
- Scholarly historical resources

Check licenses at the individual item level.

The Library of Congress is particularly valuable for later historical periods, while ancient content will rely more heavily on archaeology, museums, and scholarly reconstructions.

---

# 12. Editorial and Historical Accuracy Rules

These rules should apply to all authored historical content.

1. Every published historical fact should have a trustworthy source.
2. Historical interpretations must be distinguished from established evidence.
3. Approximate or disputed dates must be labeled.
4. Historical geographical boundaries must not imply unjustified precision.
5. Ancient civilizations must not be represented as equivalent to modern countries.
6. Mini-game answers must be clear and defensible.
7. Avoid excessively Eurocentric historical progression.
8. Present simultaneous developments across multiple world regions.
9. Historical artwork and reconstructions must be identified accurately.
10. Sensitive events require contextual and respectful treatment.
11. Historical sources and media rights must be preserved.
12. AI-generated historical claims must undergo editorial review before publication.
13. **v0.2:** Until reviewed, every authored item carries `"status": "draft"`, and the interface shows a "Draft – not yet fact-checked" tag on it. Only a person changes it to `"reviewed"`.
14. **v0.2:** The Cliopatria border data is uneven in its early years: before about 1500 BCE it has no states in the Americas, China or most of Africa. Discovery pins must deliberately cover regions the borders leave empty, so the map doesn't tell a Mesopotamia-only story.

### Sensitive historical subjects

War, slavery, genocide, colonialism, oppression, and other subjects involving mass suffering should not be trivialized through playful trivia.

They can be explored through respectful historical storytelling, evidence, and contextual explanations.

---

# 13. Technical Architecture

**v0.2: how this maps onto the actual repository.** The prototype doesn't use the `src/features/...` structure below, because this repo has no app framework. Instead:

- `andrew-prototype/game-template.html` is the game page: plain JavaScript and d3, built into `andrew-prototype/game.html` with the border data embedded, so it opens straight from a file.
- `andrew-prototype/game-content.json` holds all the authored content (checkpoints, discoveries, challenges, sources) in one place.
- `tools/build_andrew_prototype.py` builds both pages and **validates the content**: unique IDs, sources present, each state target actually on the map at its checkpoint year, and enough Insight available to unlock every checkpoint (no dead ends).
- Progress is saved in the browser's `localStorage` under a versioned key.
- The game duplicates the atlas's map code instead of sharing it, which keeps the atlas untouched. Sharing it is a later clean-up.

## Integration approach

The existing map application should remain intact.

Implement the game as an **optional, modular mode**.

Do not rewrite existing map or timeline systems unnecessarily.

Reuse current application components when appropriate.

## Suggested route

```text
/play/history
```

Alternatively, use an existing feature-flag or experimental-mode architecture.

## Proposed directory organization

Adapt this structure to the existing repository.

```text
src/
  features/
    history-game/
      data/
        eras.json
        checkpoints.json
        discoveries.json
        challenges.json

      components/
        GameHUD
        EraTimeline
        DiscoveryPin
        DiscoveryPanel
        ChallengeModal
        TwoTruthsLie
        MapDetective
        ThenNowCompare
        CollectionBook

      engine/
        progression.ts
        chronology.ts
        challengeScoring.ts
        contentValidation.ts

      hooks/
        useGameProgress.ts

      routes/
        HistoryGamePage
```

Do not introduce unnecessary architecture or dependencies.

---

# 14. Suggested Data Models

These TypeScript definitions are conceptual and may need adjustment to the existing application.

## Historical date

```typescript
type HistoricalDate = {
  // Astronomical year numbering:
  // 1 BCE = 0
  // 2 BCE = -1
  // 1 CE = 1

  year: number;
  approx?: boolean;
};
```

## Discovery

```typescript
type Discovery = {
  id: string;
  eraId: string;

  title: string;
  summary: string;

  start: HistoricalDate;
  end?: HistoricalDate;

  location: {
    lat: number;
    lon: number;
    precision:
      | "site"
      | "city"
      | "region"
      | "approximate";
  };

  sourceUrls: string[];
  mediaIds: string[];
  challengeIds: string[];

  editorialStatus:
    | "draft"
    | "reviewed"
    | "published";
};
```

## Player progress

```typescript
type PlayerProgress = {
  currentCheckpointId: string;

  highestUnlockedCheckpointId: string;

  insight: number;

  completedChallengeIds: string[];

  unlockedDiscoveryIds: string[];

  unlockedMediaIds: string[];

  schemaVersion: number;
};
```

## Challenge

```typescript
type Challenge = {
  id: string;

  discoveryId: string;

  type:
    | "two-truths-lie"
    | "map-detective"
    | "then-now"
    | "timeline-tangle";

  difficulty:
    | "easy"
    | "medium"
    | "hard";

  reward: number;

  completed: boolean;
};
```

Persist challenge completion separately from authored challenge definitions in the final implementation.

---

# 15. Save and Resume

## MVP requirements

Use local storage or the existing application's persistence system.

Players should be able to:

- Leave the game.
- Return later.
- Resume at their current checkpoint.
- Retain earned Insight.
- Retain unlocked discoveries.
- Retain collected media.
- Review previously completed activities.

## Requirements

- [ ] Persistent player progress.
- [ ] Versioned save data.
- [ ] Protection against duplicate rewards.
- [ ] No negative Insight balance.
- [ ] Graceful handling of corrupted save data.
- [ ] Ability to restart the adventure.
- [ ] No accidental deletion of unrelated application data.

Optional account synchronization can be added later.

Do not require account creation before the player can begin.

---

# 16. Development Roadmap

## PHASE 0 — Repository Review and Preparation

**Priority: P0**

### Tasks

- [ ] Inspect existing map architecture.
- [ ] Inspect existing historical event data.
- [ ] Inspect timeline implementation.
- [ ] Identify reusable components.
- [ ] Identify existing persistence mechanisms.
- [ ] Define the feature boundary.
- [ ] Decide how game mode will be activated.
- [ ] Establish historical chronology helpers.
- [ ] Establish content and media schemas.
- [ ] Establish feature flags.

### Definition of done

The existing app operates exactly as before with game mode disabled.

A new, isolated game route can load successfully.

No unrelated features have been modified.

---

## PHASE 1 — First Playable Vertical Slice

**Priority: P0**

### Scope

Build a small but complete gameplay experience:

**3400 BCE → 3200 BCE**

### Tasks

- [ ] Create game landing screen.
- [ ] Initialize player at 3400 BCE.
- [ ] Display current historical year.
- [ ] Add a basic era timeline.
- [ ] Display 3–5 historical discovery pins.
- [ ] Add historical story panels.
- [ ] Implement Two Truths & a Lie.
- [ ] Add correct/incorrect feedback.
- [ ] Award Insight Points.
- [ ] Display Insight balance.
- [ ] Add checkpoint advancement button.
- [ ] Require 70 Insight to advance.
- [ ] Advance timeline by 200 years.
- [ ] Update map discoveries after advancement.
- [ ] Save player progress.
- [ ] Restore progress on reload.
- [ ] Add basic advancement animation.

### Definition of done

A new player can:

1. Start at 3400 BCE.
2. Explore historical discoveries.
3. Complete three challenges.
4. Earn at least 70 Insight.
5. Unlock 3200 BCE.
6. Watch the map update.
7. Refresh the page.
8. Resume from their saved position.

**This is the most important milestone.**

**v0.2 scope actually built:** 3400 → 3200 → 3000 BCE, 10 discoveries, 15 challenges (Two Truths & a Lie, Map Detective with place and state targets, When Am I?), Free roam mode, a discovery journal, save and resume, and restart. Then / Now is deferred to Phase 2, because it needs properly licensed photo pairs.

Do not build the entire historical timeline before this experience works.

---

## PHASE 2 — Expand Core Mini-Games

**Priority: P0**

### Tasks

- [ ] Implement Map Detective.
- [ ] Implement Then / Now.
- [ ] Add hint system.
- [ ] Add credited historical media.
- [ ] Add basic collectible gallery.
- [ ] Expand the initial historical content.
- [ ] Add additional checkpoints.
- [ ] Introduce chapter milestones.
- [ ] Add optional artifact unlocks.
- [ ] Add optional event deep dives.

### Initial content targets

- Approximately 30 historical discoveries.
- Approximately 35 mini-game prompts.
- 9 Then / Now comparisons.
- 6–9 historical checkpoints.
- Three early historical chapters.

These are development targets, not strict launch requirements.

### Definition of done

Players can experience all three primary mini-games and complete a full early chapter without becoming stuck.

---

## PHASE 3 — Visual Polish and Game Feel

**Priority: P1**

### Tasks

- [ ] Refine map marker design.
- [ ] Improve discovery panels.
- [ ] Add rewarding timeline transitions.
- [ ] Create chapter-introduction screens.
- [ ] Improve the Insight display.
- [ ] Add visual feedback for discoveries.
- [ ] Improve mobile layout.
- [ ] Add accessible interaction alternatives.
- [ ] Add reduced-motion settings.
- [ ] Refine historical typography.
- [ ] Improve artwork presentation.
- [ ] Polish collectible gallery.

### Design objective

The experience should feel like interacting with a beautiful historical atlas.

Not a conventional educational dashboard.

Not a generic trivia website.

---

## PHASE 4 — Test and Balance

**Priority: P0 before public launch**

### Tasks

- [ ] Conduct playtests with 5–10 new users.
- [ ] Verify progression clarity.
- [ ] Measure time to first interaction.
- [ ] Measure time to first checkpoint unlock.
- [ ] Record where players get confused.
- [ ] Identify unnoticed map features.
- [ ] Test point economy.
- [ ] Verify no progression dead ends.
- [ ] Verify historical accuracy.
- [ ] Audit source attribution.
- [ ] Audit media licenses.
- [ ] Test BCE/CE transitions.
- [ ] Test mobile devices.
- [ ] Test keyboard navigation.
- [ ] Test screen reader compatibility.
- [ ] Test saved progress and restoration.

### Definition of done

Players understand how to explore, earn Insight, and unlock time without extensive instructions.

---

## PHASE 5 — Historical Content Expansion

**Priority: P1**

### Tasks

- [ ] Expand historical checkpoints.
- [ ] Add additional civilizations and regions.
- [ ] Add more map discoveries.
- [ ] Introduce additional mini-games.
- [ ] Add historical map overlays.
- [ ] Add One World, One Year.
- [ ] Add historical connections.
- [ ] Add thematic collections.
- [ ] Add regional expeditions.
- [ ] Add collection achievements.

### Long-term objective

Build a comprehensive world history exploration system spanning the earliest playable period to the present.

Expand gradually rather than attempting to populate all historical years immediately.

---

# 17. Initial Historical Content Assignments

The following are suggested research topics.

They are not yet approved game questions.

Each topic must be researched, sourced, and assigned to an appropriate checkpoint.

| Topic | Mini-Game | Region |
|---|---|---|
| Early accounting and writing practices | Two Truths & a Lie | Mesopotamia |
| Growth of Uruk | Map Detective | West Asia |
| Early Egyptian state formation | Map Detective | Northeast Africa |
| Early Indus region settlements | Then / Now | South Asia |
| Early complex societies in the Caral region | Map Detective | South America |
| Bronze Age exchange networks | Trade Route Explorer | Multiple regions |
| Early Chinese archaeological cultures | Artifact Comparison | East Asia |
| Stonehenge and its changing landscape | Then / Now | Europe |

These discoveries occurred at different times.

**v0.2: content in the prototype** (all `draft`, sources attached in `game-content.json`):

| Checkpoint | Discovery | Challenges | Region |
|---|---|---|---|
| 3400 BCE | Uruk and the first writing | Two Truths, Map Detective (place) | Mesopotamia |
| 3400 BCE | Ötzi the Iceman | Two Truths, Map Detective (place) | Alps, Europe |
| 3400 BCE | Tomb U-j at Abydos | Two Truths | Upper Egypt |
| 3200 BCE | Newgrange | Two Truths | Ireland |
| 3200 BCE | Liangzhu | Map Detective (place) | Eastern China |
| 3200 BCE | Elam and Susa | Map Detective (state) | South-west Iran |
| 3000 BCE | Narmer and a united Egypt | Two Truths, Map Detective (state) | Nile Valley |
| 3000 BCE | Early towns of the Indus | Map Detective (state) | South Asia |
| 3000 BCE | The first Stonehenge | Two Truths | Britain |
| 3000 BCE | Norte Chico and Caral | Two Truths, Map Detective (place) | Peru |
| 3000 BCE | (checkpoint challenge) | When Am I? | Whole map |

Do not assign all of them to the 3400 BCE starting point.

---

# 18. UI / UX Design Direction

## Desired aesthetic

An immersive, beautiful, modern historical atlas.

Potential influences:

- Antique cartography
- Historical atlases
- Museum exhibition design
- Archival documents
- Illustrated historical encyclopedias
- Elegant strategy-game interfaces

## Interface priorities

1. The map remains dominant.
2. Historical information is easy to read.
3. The current year is always apparent.
4. Points are clearly visible.
5. The next objective is obvious.
6. Timeline advancement feels rewarding.
7. Mini-games are intuitive.
8. Historical imagery receives generous visual space.
9. Mobile interactions are carefully considered.
10. The interface avoids clutter.

## Important principle

The game should feel rewarding through discovery and meaningful progression.

Avoid relying on excessive gamification effects, unnecessary notifications, or manipulative engagement mechanics.

---

# 19. Features to Avoid During MVP

Do not prioritize:

- Multiplayer
- Competitive leaderboards
- Account systems
- Daily streak requirements
- Energy systems
- Premium currencies
- Procedurally generated historical questions without review
- Fully animated historical political boundaries
- Complete historical world simulation
- Expensive 3D environments
- Complex artificial intelligence systems

These features increase complexity without necessarily improving the core experience.

Focus on making the basic loop enjoyable.

---

# 20. Important Product Decisions

## A. Exploration vs. education

**Recommendation:** Exploration first, learning through play.

Players should feel curious rather than tested.

## B. Correct answers vs. participation

**Recommendation:** Award baseline Insight for completing new challenges.

Give bonuses for correct answers.

## C. Timeline advancement

**Recommendation:** Authored historical checkpoints with clearly displayed year jumps.

## D. Global historical scope

**Recommendation:** Include parallel historical developments across regions.

Do not make world history a sequential tour of only the most famous civilizations.

## G. Free roam (v0.2)

**Decision:** Free roam ships with the MVP as the second mode of the same page. It's the existing atlas plus every discovery pin and story, with no locks and no Insight. The campaign is one way in, not the only one (this was "Free Explore mode" in §22).

## H. Audience (v0.2, open)

**To decide:** who the main player is. The prototype's stories (60–120 words) assume a confident reader aged about 10 and up. A younger audience would need shorter stories, read-aloud support and more map-tapping than reading.

## E. Existing application integration

**Recommendation:** Additive, modular game mode.

Do not replace or destabilize the existing app.

## F. Content quality

**Recommendation:** Structured, sourced, editorially reviewed content.

Historical accuracy should be a core product feature.

---

# 21. MVP Acceptance Checklist

The initial playable MVP is complete when:

- [ ] The game starts around 3400 BCE.
- [ ] Current historical year is clearly displayed.
- [ ] Historical discoveries appear on an interactive map.
- [ ] Discovery panels contain short stories.
- [ ] Two Truths & a Lie works.
- [ ] Map Detective works.
- [ ] Then / Now works.
- [ ] Correct answers provide explanations.
- [ ] Historical sources are accessible.
- [ ] Players earn Insight.
- [ ] Insight can unlock time.
- [ ] Insight can unlock optional historical content.
- [ ] Historical map discoveries change with time.
- [ ] Players can revisit earlier periods.
- [ ] Progress is saved locally.
- [ ] Refreshing does not reset progress.
- [ ] Repeating completed questions does not farm Insight.
- [ ] No checkpoint can become permanently inaccessible.
- [ ] Historical sources and media licenses are verified.
- [ ] Mobile interaction works.
- [ ] The existing app remains unaffected when game mode is off.

---

# 22. Future Expansion Opportunities

Once the basic game proves enjoyable, consider:

### Historical campaigns

Thematic adventures that reuse existing content:

- History of Cities
- History of Writing
- History of Astronomy
- History of Navigation
- History of Democracy
- History of Art
- History of Trade
- History of Technology

### More advanced historical maps

Create optional historical overlays showing developments that can be supported by reliable map data.

### Illustrated historical collections

Allow players to assemble and share collections of historical imagery and discoveries.

### Historical poster generation

Use unlocked historical maps, artifacts, and discoveries to generate beautiful printable historical posters.

This could complement a map-focused application's existing print or poster functionality.

### Educational mode

Allow teachers or students to explore historical material without spending points or completing challenges.

### Free Explore mode

**v0.2:** Promoted to the MVP as "Free roam" (§20 G).

Let users disable progression locks entirely.

The gamified campaign should be an optional way to experience the application, not the only way to access historical information.

---

# 23. Recommended Immediate Development Task

## Build the first five-minute playable loop

**Scope: 3400 BCE → 3200 BCE**

### Deliverables

1. History Adventure landing screen.
2. Interactive map displaying three discoveries.
3. Historical story cards.
4. Two Truths & a Lie component with multiple authored questions.
5. Insight Points balance.
6. Challenge scoring and completion tracking.
7. A 70-Insight advancement button.
8. Timeline transition from 3400 BCE to 3200 BCE.
9. New discoveries revealed after advancing.
10. Local save and resume.

### Implementation constraints

- Reuse existing components where possible.
- Avoid large architectural refactors.
- Keep the feature isolated.
- Preserve existing map functionality.
- Use structured content data.
- Keep historical citations attached to content.
- Ensure all progression rules are testable.

### Success criteria

A first-time player should be able to open the game, understand the objective, explore the map, complete challenges, earn points, and advance to the next checkpoint.

The first advancement should be visually satisfying.

The player should immediately want to discover what happens next.

---

# 24. Guiding Product Vision

The ultimate experience is not simply answering historical trivia.

It is watching the world unfold.

The player begins thousands of years in the past, with only a handful of historical discoveries available.

As they explore, the historical map fills with people, places, cities, artifacts, stories, ideas, and connections.

The player gradually unlocks centuries and eventually millennia.

They learn not just what happened, but where it happened, when it happened, and how events in distant parts of the world were connected.

Their collection becomes a personal museum of human history.

**The game should reward curiosity, encourage exploration, and make historical discovery feel exciting.**

---

# END OF DEVELOPMENT PLAN
