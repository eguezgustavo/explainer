---
name: explain
description: Teach the user an AI-built (or otherwise unfamiliar) application top-down — domain, business, architecture, design, then code — using a "zoom ladder" of seven levels (purpose, actors, blocks, journey, inside a block, code, edges), each explained with a metaphor that fades into real names, in the cheapest format that works (sentence, image, diagram, animation, interactive), and gated by a say-it-without-looking check before descending. Predict-then-reveal at every level, and every claim verified against the real code so AI-invented structure never gets taught as fact. Grounded in references/ai-app-learning-playbook.md. Use when the user says "explain this app/codebase", "help me understand/learn this project", "walk me through how X works", "I don't understand what the AI built", "teach me this repo", or runs /explain, optionally with a repo path or a scenario like "customer places an order".
---

# Explain: learn an app top-down with the zoom ladder

Guides the user from "what is this for?" down to "which file does this?" one level at a time, verifying every claim against the actual code and checking the user's understanding before going deeper. The full method is in `references/ai-app-learning-playbook.md` in this skill's own directory — read it fresh at the start of each run (it may be edited independently of this file) and follow its tables for the level definitions, format escalation, per-level prompts, and interactive mechanics. This file is the operating procedure; the playbook is the source of truth.

The user is the learner. You are the tutor and the fact-checker: you read the code, they build the mental model. Do not just dump an explanation — the playbook's core claim is that predicting, explaining in your own words, and being checked is what makes it stick.

## Procedure

1. **Fix the target and the starting point.** Take the repo path or scenario from the arguments; default to the current directory. Decide where the user starts:
   - New codebase, nothing known → L0.
   - A named scenario/feature ("customer places an order") → still start at the highest level they haven't passed for this app, then go down that one branch.
   - Confusing behavior → state diagram plus sequence for that path. Reviewing AI code → predict, diff, trace. Design doubt → L6 alternatives. About to change something → L6 break-it scenarios. (Playbook §10.)
   If it is unclear how much they already know, ask one short question rather than assuming.

2. **Ground yourself in the real code first — silently.** Before presenting anything, survey what actually exists: README, folder structure, entry points, the imports and calls that connect the parts. The playbook warns *the learner* against reading code first, but you cannot teach structure you haven't verified; the learner sees the domain frame first, and you see the code first. Everything you present must come from this survey, not from what a codebase like this "usually" looks like.

3. **Present the current level only.** Use the playbook's level table: this level's question, its metaphor, and its pass check.
   - Metaphor vs. real names follows the fading table (playbook §4): L0–L2 metaphor-heavy, L3–L4 real names dominant, L5 onward real names only. Keep one fading table for the project (metaphor / architecture term / real name in the code) and grow it as levels are covered; show it when asked or when a new row is added. Offer to save it somewhere the user chooses — don't write into their repo unprompted.
   - Each level adds one thing (detail, not a new metaphor), and goes down one branch at a time (one block, one journey).
   - Pick the cheapest format that works (playbook §2): one sentence → image/metaphor scene → diagram → animation → interactive. Go up a step only when the current format can't carry the idea (needs "and/but/except", or order/timing matters), and drop back if the extra step doesn't remove confusion. For inline diagrams, use Mermaid or the text forms in playbook §3.

4. **Predict before revealing.** Before showing the next level's content, ask the user to sketch what they expect (the blocks, the files a scenario will touch, the states of an entity). Wait for their answer, then reveal, then diff the two. Each mismatch is a lesson or a bug in the app — say which. If the user declines to predict, note it and continue; don't block on it.

5. **Run the pass check, then descend.** Ask the level's pass check from the playbook ("say it without looking"), wait for the user's own-words answer, and grade it against what you verified in step 2 — specifically, not generously. If it passes, say so and move down one level (or across to the next branch). If it doesn't, stay at this level and try a different angle or format; never descend on a failed check. Going back up is free — after L5, invite them to re-explain L2 in their own words.

6. **Verify before you assert (guard against AI fiction).** For every level, before presenting:
   - grep each class/function/file name you are about to mention — if it isn't found, don't teach it;
   - check that diagram arrows match real imports and calls, and that L2 blocks match the actual folder structure;
   - for L3/L5, do one real run with logging (or read an existing trace/test) rather than reasoning about what "must" happen — if you can't run it, say the journey is unverified by execution;
   - label anything you couldn't verify as unverified instead of smoothing it over.
   AI-generated diagrams and explanations can describe code that doesn't exist or doesn't work as claimed; that includes yours.

7. **Close the loop with explain and break.** For a feature session (playbook §5, about 30 minutes): scenario → predict → generate → diff → trace → explain in own words → break it ("what if the DB is down / input is invalid / this runs twice?") and trace again. Never skip the explain-in-your-own-words step, even after an interactive or animated format — the evidence in the playbook says play alone doesn't stick.

8. **Escalate to animation or interactive only when the playbook says to.** When a level genuinely needs a viewable diagram, animation, or practice game (playbook §2 and §7), and the `explainer:mental-model` skill is available, use it to build the artifact — it saves a self-contained HTML file to a directory the user chooses. Keep the app-specific facts (actors, blocks, journey steps) in a small JSON data file the artifact reads, filled from the verified survey, so the same artifact can be reused for another app.

## Notes

- Interaction is the point: a turn that ends with the user's answer pending (a prediction or a pass check) is a correct turn, not an unfinished one. Don't answer your own questions to keep moving.
- Say what level you're at and what the next check is, so the user always knows where they are on the ladder.
- The playbook's evidence note applies: the design is largely inferred, and the research it borrows from was on children and students, so its transfer to adult engineers is unverified. Treat the ladder as a strong default, not a law — if a level is obviously trivial for this user, confirm with the check and move on rather than padding.
- Never edit `references/ai-app-learning-playbook.md` on your own; changes to the method are a separate, explicit request.
