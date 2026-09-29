# Playbook: Learning an AI-Built App Fast

**Goal:** understand the domain, business, architecture, design, and code of an AI-generated application, top-down.

**Evidence note:** The design is mostly inferred. Cited research was on children/students, and its transfer to adult engineers is unverified. Carried-over ideas:
- Interactive simulations helped kindergarteners with physics concepts (small study).
- Predict-then-test cycles are supported by simulation research.
- Concrete-to-abstract fading is studied for transfer of knowledge.
- Caveat: play alone didn't stick. Students updated written descriptions but not visual ones after an interactive analogy, so always add an explain-in-your-own-words step.

---

## 1. Core idea: the zoom ladder

Start at the highest abstraction with a metaphor. At each level, swap metaphor for real names and add detail. Don't descend until you pass that level's check.

| Level | Question | Metaphor | Pass check (say it without looking) |
|---|---|---|---|
| L0 Purpose | Why does this exist? | "A restaurant for X" | Explain it to a non-engineer in 10 seconds |
| L1 Actors | Who uses it? What external systems does it touch? | Diners, suppliers, inspector | Name every actor and its goal |
| L2 Blocks | What are the big parts? | Waiters, kitchen, pantry | Draw the blocks and their dependencies |
| L3 Journey | How does one action cross the blocks? | An order's path, table to plate | Narrate one scenario, block by block |
| L4 Inside a block | What rules, entities, states live here? | Recipe book, menu, order status | List the rules and the entity lifecycle |
| L5 Code | Which files and functions do this? | Named staff and stations | Predict the files, then check |
| L6 Edges | What breaks? Why this design? | Kitchen fire, rush hour | State one failure and one rejected alternative |

### Rules of descent
1. Never go down until you pass the check.
2. Each level adds one thing: detail, not new metaphors.
3. Go down one branch at a time (one block, one journey).
4. Predict before revealing: sketch the next level, then have AI show it. The gap is the lesson.
5. Going back up is free: after L5, re-explain L2 in your own words.

---

## 2. Format escalation: use the cheapest format that works

| Step | Format | Use when | Escalate when |
|---|---|---|---|
| 1 | One sentence | One subject, one verb, one consequence | You need "and", "but", or "except" to finish it |
| 2 | Image / metaphor scene | The idea is about shape or relationship: what contains or sits next to what | You need to say "then" or "if" while pointing at it |
| 3 | Diagram (boxes, arrows, states) | The idea has parts and rules: dependencies, layers, entities, lifecycles | Order or timing matters and a still diagram hides it |
| 4 | Animation | The idea is a sequence, flow, or change over time | You need to practice, not just understand |
| 5 | Interactive / game | You want to test yourself: predict the next step, break a rule | Never required; opt in |

**Quick test:** if your explanation takes a breath, go up one step. If the extra step doesn't remove confusion, drop back down.

### Typical landing format per level (adjust freely)

| Level | Usual format | Why |
|---|---|---|
| L0 | Sentence (+ metaphor) | If it doesn't fit in one sentence, the purpose is unclear |
| L1 | Sentence list or context diagram | Few actors, few links |
| L2 | Diagram | Parts with dependency rules |
| L3 | Diagram; animation if branching or async | Order matters |
| L4 | State diagram | Fixed states and transitions |
| L5 | Sentence per file + call trace | Detail lives in the code |
| L6 | Sentence; animation for cascading failures | Most edge cases are one-liners |

### Decision helper
- One sentence possible? Words.
- About shape? Image.
- About parts and rules? Diagram.
- About sequence or change? Animation.
- Need practice? Interactive.

---

## 3. Simple diagrams (text form)

**L1 Context**
```
[Customer] --> ( App ) --> [Payments API]
[Staff]    --> ( App ) --> [Database]
```

**L2 Blocks** (Clean Architecture; arrows = "depends on")
```
UI/Controllers --> Use Cases --> Domain
Adapters (DB, APIs) --> Ports <-- Use Cases
```

**L3 Journey**
```
Customer -> Controller -> UseCase -> Port -> Adapter -> DB
```

**L4 Lifecycle**
```
Draft -> Submitted -> Approved -> Fulfilled
              \-> Rejected
```

**Entities**
```
Customer 1--* Order 1--* OrderLine *--1 Product
```

---

## 4. Fading table (keep one per project)

Fill column 1 first. Stop using it as you learn columns 2 and 3.

| Metaphor | Architecture term | Real name in the code |
|---|---|---|
| Waiter | Controller / inbound adapter | `OrderController` |
| Recipe book | Use case | `PlaceOrder` |
| Kitchen rules | Domain rules | `Order.validate()` |
| Pantry door | Port (interface) | `OrderRepository` |
| Pantry shelves | Adapter (implementation) | `PostgresOrderRepository` |

Metaphor use: L0 to L2 metaphor-heavy, L3 to L4 real names dominant, L5 onward real names only.

---

## 5. Session flow (about 30 min per feature)

1. **Scenario:** pick one user action ("customer places an order").
2. **Predict:** sketch layers and files you expect. Write it down before opening code.
3. **Generate:** have AI produce the context diagram, then the sequence for that scenario.
4. **Diff:** compare with your prediction. Each mismatch is a lesson or a bug.
5. **Trace:** run with sample data and log each layer boundary.
6. **Explain:** state the flow and the reason for each layer, in your own words.
7. **Break:** ask "what if the DB is down / input is invalid / this runs twice?" and trace again.

**Cadence:**
- First pass: L0 to L3 for the whole app (about 1 hour).
- Per feature: L3 to L5.
- Before any change: L6.

---

## 6. Prompts per level

- **L0:** "Describe this app in one sentence and one restaurant-style metaphor."
- **L1:** "List the actors, their goals, and external systems. Nothing about code."
- **L2:** "List the blocks and dependency arrows. Map each to a metaphor and a folder."
- **L3:** "Trace <scenario> through the blocks as a numbered list, then a sequence diagram."
- **L4:** "For <block>: rules, entities, states. Mark which rules are enforced in code and where."
- **L5:** "Which files does <scenario> touch, in call order? One line each."
- **L6:** "What happens if <X> fails at each step? Give 2 alternative designs and why they were rejected."

---

## 7. Optional animation and game layer

Use only when the escalation table says so.

| Level | Interactive format | Mechanic |
|---|---|---|
| L0 | Animated metaphor scene | Click to "run a day" |
| L1 | Drag-and-drop matching of actors to goals | Score for correct matches |
| L2 | Build-the-diagram puzzle | Wrong dependency arrow flashes red and shows why |
| L3 | Animated packet through blocks, step/pause | Predict the next block before it moves |
| L4 | Clickable state machine | Find the input the domain rejects |
| L5 | File-tree hunt: click the files you think are touched | Replay the real trace, score accuracy |
| L6 | Chaos toggles: "DB down", "duplicate request" | Fix the design so the scenario survives |

**Animation vocabulary:** moving dot = request/event; color change = state transition; shake or red flash = rule violation; fading metaphor label = mastered concept.

**Build tip:** one HTML file plus a JSON data file (actors, blocks, journey steps) that AI fills from the repo. Swap the JSON to reuse it for another app.

---

## 8. Guard against AI fiction

AI diagrams and explanations can describe code that doesn't exist or doesn't work as claimed. Verify each level:
- grep every class or function name the AI mentions
- do one real run with logging (L3/L5)
- check that diagram arrows match actual imports and calls
- check that L2 blocks match the folder structure

---

## 9. Failure modes

- Reading code first: anchors on details without the domain frame.
- Accepting a diagram without a trace: it may be plausible fiction.
- Escalating format too early: sentences often suffice.
- Skipping the explain step: you feel fluent but can't reproduce it.
- Learning everything at once: take one vertical slice at a time.
- Play without explaining: interaction without understanding.

---

## 10. Quick chooser

- New codebase: L0 sentence, context diagram, one scenario story.
- Confusing behavior: state diagram plus sequence for that path.
- Reviewing AI code: predict, diff, trace.
- Design doubt: alternatives table (L6).
- Before changing anything: break-it scenarios.
