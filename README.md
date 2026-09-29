# explainer

A Claude Code plugin marketplace. This repo is both the marketplace and the one
plugin it currently lists (`explainer`).

## Install

From inside a Claude Code session:

```
/plugin marketplace add eguezgustavo/explainer
/plugin install explainer@explainer
```

Or from a shell:

```
claude plugin marketplace add eguezgustavo/explainer
claude plugin install explainer@explainer
```

## Skills

### `mental-model`

Picks the single best non-linguistic mental model (diagram type, chart
library, animation, simulation, or other non-prose representation) for
explaining, teaching, or building a given concept — then layers it across
abstraction levels the viewer can switch between (ELI5/practitioner/expert,
overview/detail, etc.), builds it, animates it if it's sequential/temporal,
and saves it as a viewable file automatically.

It's grounded in two catalogs, each installing alongside the skill so
updating either only requires editing it here and re-installing/updating
the plugin:

- [`skills/mental-model/references/non-linguistic.xml`](skills/mental-model/references/non-linguistic.xml) —
  ~50 representation techniques, each with a criterion for when it's the
  right fit.
- [`skills/mental-model/references/abstraction-techniques.xml`](skills/mental-model/references/abstraction-techniques.xml) —
  ~18 ways to move between levels of detail/generality (laddering,
  roll-up/drill-down, C4's context→code, audience-tiered ELI5→expert, etc.),
  each with a direction (`up`/`down`/`both`) and a criterion for when it fits.

### `explain`

Teaches you an unfamiliar (typically AI-built) application top-down by
generating an interactive HTML page rather than terminal text. The page walks a
"zoom ladder": purpose → actors → blocks → journey → inside a block → code →
edges. Each level is in plain words with a concrete example from the app, lets
you predict before it reveals the verified answer, shows diagrams (with a
step-through for journeys), and gates the next level behind a
say-it-without-looking check. The text is plain, simple English, with no
metaphors unless you ask. Your notes and progress stay in your browser.

Every claim is verified against the real code before it reaches the page: the
build script refuses to produce the page if a "verified" file, line, snippet or
class name isn't actually in the repo, so AI-invented structure isn't taught as
fact.

Run it as `/explainer:explain`, optionally with a repo path or a scenario
(e.g. `/explainer:explain customer places an order`). Without a scenario it
builds L0–L3 for the whole app; with a block or scenario it builds L3–L6 for
that branch. It's grounded in
[`skills/explain/references/ai-app-learning-playbook.md`](skills/explain/references/ai-app-learning-playbook.md),
which installs alongside the skill.

## Repo layout

```
.claude-plugin/
  plugin.json        # plugin manifest
  marketplace.json    # marketplace manifest (source: "./", points back at this repo)
skills/
  mental-model/
    SKILL.md
    references/
      non-linguistic.xml
      abstraction-techniques.xml
  explain/
    SKILL.md
    scripts/
      build_page.py            # fills the template, verifies claims against the repo
    references/
      ai-app-learning-playbook.md
      template.html            # the learning page (fixed UI)
      data-schema.md           # the data format the page is built from
```
