---
name: mental-model
description: Pick the single best non-linguistic mental model (diagram type, chart library, animation, simulation, or other non-prose representation) for explaining, teaching, or building a given concept, layer it across viewer-selectable abstraction levels (ELI5/practitioner/expert, overview/detail, etc.), then build it and save it as a viewable file automatically. Grounded in references/non-linguistic.xml (~50 representation techniques) and references/abstraction-techniques.xml (~18 ways to move between levels of detail), each entry with a "when to use" criterion. Use when the user asks "what's the best way to visualize/diagram/represent/animate X", "what non-linguistic mental model fits this", "how should I show this without words", "give me this at different levels of detail", or whenever several representation or abstraction techniques could plausibly fit and the right one isn't obvious. Also use before building a diagram, chart, simulation, or interactive visual when the choice of technique hasn't already been made.
---

# Mental Model Picker

Selects the best non-linguistic (non-prose) way to represent a concept, and the best way to layer it across abstraction levels the viewer can move between, by matching the concept's structure against two curated catalogs.

## Steps

1. **Read both catalogs.** Read `references/non-linguistic.xml` and `references/abstraction-techniques.xml` in this skill's own directory — fresh every time, not from memory, since either may be edited independently of this file.
   - `non-linguistic.xml`: representation techniques (diagram types, chart libraries, animations, simulations), each with a `<when_to_use>` criterion.
   - `abstraction-techniques.xml`: ways to move between levels of detail/generality (laddering, roll-up/drill-down, C4's context→code, audience-tiered ELI5→expert, etc.), each with a `<direction>` (`up`, `down`, or `both`) and a `<when_to_use>` criterion.

2. **Characterize what needs representing.** Before matching, pin down:
   - What *kind* of structure is being shown: sequential/temporal, hierarchical, relational/networked, part-to-whole, quantitative comparison, spatial/geometric, discrete state+transition, causal/emergent, or flow/volume between stages.
   - Whether it has *a beginning and an end, or otherwise unfolds as a sequence over time* — this shape gets step-through animation in step 7, regardless of which technique is picked.
   - Whether it has natural coarser/finer groupings — could this honestly be told in fewer, bigger strokes as well as in full detail, without just hiding pieces of the same rendering? Almost everything can; this feeds step 4.
   - Whether it needs to be *interactive* (explored, clicked, dragged) or is fine as a *static* image.
   - The audience and output medium (a terminal, a markdown doc, a web artifact, a paper, a notebook, an embedded app) — some techniques assume a specific medium.
   - Any hard constraints already given (must be executable, must be a standalone file, must match a notation standard, must run at 60fps, etc).

3. **Pick the representation technique.** Compare the characterization against every `<when_to_use>` entry in `non-linguistic.xml`, not just the first plausible one — several may partially fit. Pick the single best match. If two or three are genuinely close, say so and give the top pick plus runner-up(s) with the deciding factor between them.

4. **Pick the abstraction technique and define concrete levels.** Match the same way against `abstraction-techniques.xml`, using its `<direction>` too: `up` builds a general case from instances, `down` refines a general statement into specifics, `both` lets the viewer move freely either way — usually the right fit when the viewer will pick their own level interactively. From the chosen technique, define 2–4 concrete, *named-for-this-concept* levels — not the technique's generic label. Examples of the mapping (not a fixed menu):
   - `audience_tiered_rewrite_eli5_practitioner_expert` → ELI5 / Practitioner / Expert.
   - `roll_up_drill_down_olap_group_by` or `semantic_zooming` → Overview / Key Moments / Full Detail.
   - `c4_model_context_container_component_code` → Context / Container / Component / Code.
   - `goal_strategy_tactic_action` → Goal / Strategy / Tactics / Actions.
   Each level must be its own coherent, self-standing account of the concept at that grain — write each level's actual content now, don't defer it to "hide some elements later."

5. **Report both picks.** State: the chosen representation technique and why it beat the runner-up (as before); the chosen abstraction technique, its direction, and the concrete level names derived from it for this concept.

6. **Build it.** Don't stop at the recommendation — produce the actual diagram/chart/animation/simulation for each defined level, using whatever tool fits the chosen representation technique best in this session (inline Mermaid/SVG/ASCII, the Artifact tool for something that wants its own page, a plotting library, an existing diagramming/dataviz skill already available here, etc.). Defer to a more specific skill or tool for the *build* step when one is loaded and fits better, but don't ask permission first just to start building — only pause if the build itself needs something genuinely disruptive (installing a new dependency, an external network call, overwriting an existing file).

7. **Animate sequential/temporal concepts.** If step 2 flagged a beginning/end or a sequence over time, add forward/backward step controls (buttons, plus arrow-key support when the medium is a browser page) that reveal one beat at a time, instead of rendering the whole timeline statically in one shot. For a Mermaid sequence diagram specifically: keep the ordered `(actor, actor, message)` beats as data, re-render the diagram text with `mermaid.render()` for just the beats up to the current step on every click, and show a step counter (`n / total`) plus the current beat's message as a caption. The same rebuild-and-redraw pattern applies to any other animatable technique from the catalog.

8. **Add the abstraction-level selector.** Give the viewer a control (tabs or segmented buttons, one per level named in step 4) to switch between levels. Switching levels swaps in that level's own content — its own beat-list, its own diagram data — and, if step 7 also applies, resets the step position to that level's first beat. The two controls compose rather than one replacing the other: the level picks the granularity, the step controls move through that level's beats.

9. **Produce a viewable artifact automatically — don't wait to be asked.** Inline code (a Mermaid block, an SVG snippet) is not itself something the user can open and view; turn it into an actual file they can look at, in the same turn as the build, without a follow-up round-trip:
   - For anything a browser can render (Mermaid, SVG, an HTML/JS visualization, a chart library), write a single self-contained HTML file that loads what it needs (e.g. the Mermaid.js CDN build) and displays the diagram/chart directly — no separate server, no build step, no new local dependency required to *view* it.
   - For a technique whose natural output is already a standalone file (an image, a `.dot`/`.puml` source, a notebook, a script), produce that file instead of forcing it into HTML.
   - Still ask the user which directory to save it in — don't default to one silently — then save it there and confirm the path back to them. Only skip that ask if they already told you the directory (in this request or a standing preference).
   - This step is about producing something *viewable on disk*, not about publishing to a hosted service — reach for the Artifact tool here only if the user's medium/audience from step 2 actually calls for a shareable hosted page, not as the default.

## Notes

- If nothing in either catalog fits well, say so plainly rather than forcing a weak match — recommend prose (for representation) or a single flat level (for abstraction), or note the gap so the relevant catalog can be extended.
- This skill never edits `references/non-linguistic.xml` or `references/abstraction-techniques.xml` on its own; if the user wants to add/remove/tune an entry in either, treat that as a separate, explicit request.
- Before saving a Mermaid build, scan the label/message text for a bare `;` — Mermaid treats it as a statement terminator even inside a sequence-diagram message, and one occurrence silently breaks the whole diagram's parse (surfaces as a "Syntax error in text" box, not an HTML/JS error). Use a comma or em dash instead. The same caution applies to any other DSL with its own reserved punctuation (Graphviz, PlantUML, etc.) — check the chosen technique's syntax before treating the build as done, not just the surrounding HTML.
