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

Teaches you an unfamiliar (typically AI-built) application top-down using a
"zoom ladder": purpose → actors → blocks → journey → inside a block → code →
edges. Each level uses a metaphor that fades into real names, the cheapest
format that works (sentence, image, diagram, animation, interactive), a
predict-then-reveal step, and a say-it-without-looking check before you
descend. Every claim is verified against the real code so AI-invented
structure isn't taught as fact.

Run it as `/explainer:explain`, optionally with a repo path or a scenario
(e.g. `/explainer:explain customer places an order`). It's grounded in
[`skills/explain/references/ai-app-learning-playbook.md`](skills/explain/references/ai-app-learning-playbook.md),
which installs alongside the skill. When a level needs a viewable diagram or
animation it hands off to `mental-model`.

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
    references/
      ai-app-learning-playbook.md
```
