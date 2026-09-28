---
name: mental-model
description: Pick the single best non-linguistic mental model (diagram type, chart library, animation, simulation, or other non-prose representation) for explaining, teaching, or building a given concept, then build it. Grounded in references/non-linguistic.xml, a curated list of ~50 techniques each with a "when to use" criterion. Use when the user asks "what's the best way to visualize/diagram/represent/animate X", "what non-linguistic mental model fits this", "how should I show this without words", or whenever several representation techniques could plausibly fit a concept and the right one isn't obvious. Also use before building a diagram, chart, simulation, or interactive visual when the choice of technique hasn't already been made.
---

# Mental Model Picker

Selects the best non-linguistic (non-prose) way to represent a concept, by matching the concept's structure against a curated catalog of representation techniques.

## Steps

1. **Read the catalog.** Read `references/non-linguistic.xml` in this skill's own directory (do not summarize it from memory — read it fresh every time, since it may be edited independently of this file). Each entry is a technique (e.g. `mermaid_js_flowcharts_sequence_diagrams`, `sankey_data_flow_diagrams`, `finite_state_machine_automators`) with a `<when_to_use>` criterion describing the shape of concept it fits.

2. **Characterize what needs representing.** Before matching, pin down:
   - What *kind* of structure is being shown: sequential/temporal, hierarchical, relational/networked, part-to-whole, quantitative comparison, spatial/geometric, discrete state+transition, causal/emergent, or flow/volume between stages.
   - Whether it needs to be *interactive* (explored, clicked, dragged) or is fine as a *static* image.
   - The audience and output medium (a terminal, a markdown doc, a web artifact, a paper, a notebook, an embedded app) — some techniques assume a specific medium (e.g. LaTeX TikZ assumes a LaTeX doc; Mermaid assumes a renderer that supports it).
   - Any hard constraints already given (must be executable, must be a standalone file, must match a notation standard like UML/BPMN/C4, must run at 60fps, etc).

3. **Match against the catalog.** Compare that characterization against every `<when_to_use>` entry, not just the first plausible one — several may partially fit. Pick the single best match. If two or three are genuinely close, say so and give your top pick plus the runner-up(s) with the deciding factor between them, rather than silently picking one.

4. **Report the pick.** State:
   - The chosen technique (its tag name from the XML, in plain words).
   - The one or two words of its `<when_to_use>` that clinched it.
   - Why it beats the next-closest alternative from the catalog, in one sentence.

5. **Build it.** Don't stop at the recommendation — produce the actual diagram/chart/animation/simulation using whatever tool fits the chosen technique best in this session (inline Mermaid/SVG/ASCII in the reply, the Artifact tool for something that wants its own page, a plotting library, an existing diagramming/dataviz skill already available here, etc.). Defer to a more specific skill or tool for the *build* step when one is loaded and fits better, but don't ask permission first just to start building — only pause if the build itself needs something genuinely disruptive (installing a new dependency, an external network call, overwriting an existing file) that would warrant confirmation on its own.

## Notes

- If nothing in the catalog fits well, say so plainly rather than forcing a weak match — recommend prose, or note the gap so the catalog (`references/non-linguistic.xml`) can be extended.
- This skill never edits `references/non-linguistic.xml` on its own; if the user wants to add/remove/tune a technique, treat that as a separate, explicit request.
