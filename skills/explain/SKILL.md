---
name: explain
description: Teach the user an AI-built (or otherwise unfamiliar) application top-down by generating an interactive HTML learning page, not terminal text. The page walks a seven-level "zoom ladder" (purpose, actors, blocks, journey, inside a block, code, edges) in plain words with a concrete example from the app, lets the reader predict before seeing each verified answer, and gates each level behind a say-it-without-looking check. Every claim is verified against the real code before it reaches the page, so AI-invented structure never gets taught as fact. Grounded in references/ai-app-learning-playbook.md. Use when the user says "explain this app/codebase", "help me understand/learn this project", "walk me through how X works", "I don't understand what the AI built", "teach me this repo", "explain the architecture of X", or runs /explain, optionally with a repo path or a scenario like "customer places an order".
---

When writing text, write it in plain, simple English, as if for a non-native speaker.
- Short sentences. Common words. One idea per sentence.
- No idioms or phrasal verbs (no "ring them", "pencil in", "set aside", "kick off").
- No metaphors unless I ask. If a technical term is needed, use it and define it in one short sentence.
- Say what things do, not what they are like.
- Give a concrete example instead of an analogy.
- If a sentence needs re-reading, rewrite it.

# Explain: learn an app top-down, on a page

Generates one self-contained HTML page that teaches the user an app level by level, from "what is this for?" down to "which file does this?". The full method is in `references/ai-app-learning-playbook.md` in this skill's own directory; read it at the start of each run (it may be edited independently of this file). This file says how to turn that method into a page.

**The output is the page, not a chat lesson.** The user does not want a tutorial in the terminal. Do not explain the app in your reply, and do not quiz the user in chat. The page has the predictions, the answers, the diagrams and the pass checks. Your final reply is at most three lines: the file path, which levels it contains, and how many claims were left unverified.

You are the fact-checker; the page is the tutor. Read the code, verify, write the data, build the page.

## Files in this skill

- `references/template.html` — the page. Fixed and tested; do not edit it per run.
- `references/data-schema.md` — the data format and what goes in each level. Read it before writing the data.
- `scripts/build_page.py` — fills the template from the data and refuses to build if a "verified" claim isn't really in the repo.
- `references/ai-app-learning-playbook.md` — the method.

## Procedure

1. **Fix the target and the scope.** Take the repo path or scenario from the arguments; default to the current directory.
   - Whole app, or nothing known → build **L0–L3** for the whole app (the playbook's first pass).
   - A named block or scenario ("Auth", "customer places an order") → build **L3–L6** for that one branch as its own page, with `scope` set to it. Go down one branch at a time.
   - The user asks for "the architecture" → that is L2, but still build from L0 so L2 lands on a base; they can open it directly on the page.
   Ask where to save the page, once, with a single AskUserQuestion (offer `~/Downloads`), unless they already said. Never write into the scanned repo unless they ask. Save the data file next to the page as `<app>-explained.data.json`, so a later run can extend it instead of starting over.

2. **Survey the code, read-only and silently.** README, folder structure, entry points, and the imports and calls that connect the parts. Read the tests and seed data for real examples. Never open `.env*`, key or credential files. Only run something (an existing test suite, say) when it is safe and local; never point anything at production data or real credentials. If you don't run anything, say so in `verification.method`.

3. **Write the data file** in a scratch location outside the repo (`$CLAUDE_JOB_DIR/tmp` in a background job, otherwise the system temp dir), following `references/data-schema.md`. Content rules:
   - **Text budget: one small paragraph and a visual.** When the reader reveals a level, they see only the `summary` and one visual. The `summary` is at most 60 words, in 2–3 short sentences, and the build fails above that. Never put a list in it. Every level gets a visual: a `diagram` or a `journey`. L0 gets a small flow of the main cycle. L5 gets a `journey` of the files in call order. L6 gets a diagram of where each failure ends up. Everything else (`example`, `points`, evidence, unverified notes, terms) stays closed until the reader clicks it. Keep each point under 25 words and use at most 8. If you want to add a second paragraph, draw it instead, or move it into `example` or `points`.
   - **Plain words first.** Each level's `summary` must make sense to someone who has never seen the code, with no metaphor and no jargon that isn't in the glossary yet. Short sentences.
   - **A concrete example from the app's own data**, not an abstract statement: a real-looking client, order or record taken from the seed data, fixtures or tests. Use one running `scenario` across every level.
   - **No metaphors unless the user asks.** Leave `metaphor` out of every level by default, even though the playbook uses them. If the user does ask, add `metaphor` only as an explicit two-column mapping (thing in the metaphor → thing in the app) where every row is obviously true, and never default to a restaurant. The page keeps metaphors collapsed. When a technical term is needed, use it and define it in one short sentence, in the glossary and where it first appears.
   - **Prefer a picture to more text.** If an idea has parts, order or direction, draw it (`diagram` or `journey`) instead of describing it. Use the step-through `journey` for anything that happens in order. This replaces the playbook's "cheapest format" ladder for the page: the reader asked for less text, so the visual is the default, not an escalation.
   - **Every claim gets `evidence`.** Mark it `verified` only if you saw it in the code, with `where` (path and lines) and a `contains` snippet where you can. Anything you inferred goes in `unverified`. Check the level table in the schema for what each level must contain.
   - **Pass checks the reader can self-grade:** `check.goodAnswerIncludes` lists 2–5 concrete points, specific to this app, that a correct own-words answer would cover.
   - **Glossary:** add a row (plain words / architecture term / name in the code) whenever a level introduces a term, so metaphor and jargon fade into real names as the reader descends (playbook §4).

4. **Build the page and let the script check you.**
   `python3 <this skill's directory>/scripts/build_page.py --data <data.json> --repo <repo> --out <page.html>`
   If it reports errors, the data contained something not in the repo (a missing file, an out-of-range line, a snippet that isn't there, an invented class name). Fix the data or downgrade the claim to `unverified`, then rebuild. Never loosen the script. The build succeeds only when every verified pointer is real.

5. **Report in at most three lines,** then stop: the path, the levels included, the number of unverified claims, and `open <path>`. No summary of the app, no follow-up quiz.

## Notes

- Deviations from the playbook, on purpose: there are no metaphors unless the user asks (user feedback: the restaurant-style metaphors were hard to follow), the predict / reveal / check loop happens on the page rather than in chat, and a revealed level shows one small paragraph plus a visual, with everything else opt-in (user feedback: a sudden block of text on reveal is the thing they dislike most). The playbook itself is not edited here; changes to the method are a separate, explicit request.
- The page's gating (a level unlocks after you pass the one above, with an "open anyway" override) and its predict-first, explain-in-your-own-words steps are the playbook's own guards against feeling fluent without being able to reproduce it. Don't remove them to make the page shorter.
- The playbook's evidence note applies: the design is largely inferred and the research behind it was on children and students, so treat the ladder as a strong default, not a law.
- The playbook's game layer (§7: drag-and-drop, chaos toggles) isn't built by this skill. If the user asks for it, use `explainer:mental-model` and feed it the same verified data.
- The page needs the network once to load the diagram library; without it the diagram source is shown as readable text instead of failing.
