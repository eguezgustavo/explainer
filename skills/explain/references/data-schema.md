# Data file for the explain page

`scripts/build_page.py` fills `references/template.html` from one JSON file. The template owns all UI and behaviour; the data file holds only facts about the app. Every string is shown as plain text (never as HTML), so don't put markup in it.

## Top level

```json
{
  "app": { "name": "Corner Shop", "path": "/path/to/repo", "commit": "abc1234", "generatedAt": "2026-09-28" },
  "scenario": "One sentence: the single user action used as the running example.",
  "verification": { "method": "read-only survey of the source; nothing was executed" },
  "glossary": [ { "level": 2, "plain": "The order rules", "term": "Domain logic", "code": "placeOrder()" } ],
  "levels": [ /* see below; any subset of L0..L6, each at most once */ ]
}
```

- `app.name` is required. `scenario` and `verification.method` are strongly recommended: the page shows both, so the reader knows what was and wasn't run.
- `glossary` grows the "Terms so far" table: a row appears once the reader reaches its `level`. `code` is checked against the repo, so it must be a name or file that exists. `plain` is what the reader already understands, `term` is the architecture word, `code` is what the file calls it.

## A level

```json
{
  "id": "L2", "title": "Blocks", "scope": "whole app",
  "question": "What are the big parts?",
  "predict": { "prompt": "Sketch the big parts and which one depends on which." },
  "answer": {
    "summary": "Plain-words answer, 1-3 sentences.",
    "example": "The same idea using a concrete, real-looking case from the app's own data or tests.",
    "points": ["Optional list: actors, blocks, files in call order, rules."],
    "diagram": { "title": "Blocks", "kind": "mermaid", "source": "flowchart LR\n  UI --> Logic" },
    "journey": { "title": "Place an order", "steps": [ { "from": "Staff", "to": "Handler", "text": "Submit the order" } ] }
  },
  "evidence": [ { "claim": "Handler calls placeOrder", "where": "src/routes.ts:3-5", "contains": "placeOrder", "status": "verified", "how": "read" } ],
  "unverified": ["Things you could not confirm, in plain words."],
  "metaphor": { "text": "Optional. See the rules in SKILL.md.", "mapping": [["Thing in the metaphor", "Thing in the app"]] },
  "check": { "prompt": "Draw the blocks and their dependencies.", "goodAnswerIncludes": ["Concrete point 1", "Concrete point 2"] }
}
```

`id` is `L0`..`L6`. `title`, `question`, `predict.prompt` and `check.prompt` fall back to the playbook wording if omitted. `scope` is a short label such as `whole app` or `block: Auth`.

### What goes in each level

| Level | `answer` | Format |
|---|---|---|
| L0 Purpose | one plain sentence a non-engineer would get, plus a concrete example | sentence |
| L1 Actors | who uses it and what each wants (`points`), outside systems it touches | list, or a `flowchart LR` context diagram |
| L2 Blocks | the big parts and what depends on what, mapped to real folders | `flowchart` diagram |
| L3 Journey | one scenario across the blocks, in order | `journey` (step-through) |
| L4 Inside a block | rules, entities, and the states an entity moves through, marking where each rule is enforced | `stateDiagram-v2` diagram plus `points` |
| L5 Code | the files and functions the scenario touches, in call order, one line each | `points`, with `evidence` per file |
| L6 Edges | one failure per step and two rejected alternatives, each with the reason | `points` |

## Evidence rules (this is what makes it safe to trust)

- `status: "verified"` means you looked at the real code for that claim. It requires `where`: `path`, `path:line` or `path:start-end`, relative to the repo. `contains` is an optional snippet that must appear in that file (or in those lines). `how` is `read`, `grep` or `run`.
- The build script checks every verified pointer: the file exists, the line range is inside it, the snippet is there. A failed check stops the build. Fix the data or downgrade the claim to `"status": "unverified"`. Do not weaken the check.
- `unverified` claims are shown to the reader with a warning badge. Use them for anything you inferred rather than saw, and for anything only a run could confirm.
- Never cite `.env*`, key or credential files. The script refuses them.

## Diagram source

Mermaid text. Keep labels short and avoid `;` and `#` in them (Mermaid treats a bare `;` as a statement break and one breaks the whole diagram). Journey step text is cleaned automatically, but `diagram.source` is passed through as written.
