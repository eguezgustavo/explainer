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
```
