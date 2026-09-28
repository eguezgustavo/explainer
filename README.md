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
explaining, teaching, or building a given concept.

It's grounded in [`skills/mental-model/references/non-linguistic.xml`](skills/mental-model/references/non-linguistic.xml),
a curated catalog of ~50 representation techniques, each with a criterion for
when it's the right fit. That file installs alongside the skill, so updating
the catalog only requires editing it here and re-installing/updating the
plugin.

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
```
