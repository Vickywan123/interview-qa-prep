---
name: interview-qa-prep
description: >-
  Turn a job description plus the candidate's resume/background into an interactive,
  editable HTML interview Q&A prep app: a question bank grouped by interview theme where
  every question carries a strategy, a draft answer, likely follow-ups, and an interview-round
  tag — all filterable, sortable, and editable in the browser with autosave.
  Use this whenever someone is preparing for a job interview and gives you a JD (link,
  pasted text, or file) and any description of their background, or asks to "build
  interview questions", "prep me for this interview", "make an interview question bank",
  "generate likely interview questions and answers", "help me practice for this role" — even if they don't explicitly ask for an HTML
  tool. Produce the tool by default; it is the deliverable.
---

# Interview Q&A Prep

Turn a **job description + the candidate's background** into a self-contained, editable
HTML app for interview preparation. The app is the deliverable — a single file the user
opens in any browser, no internet needed, that they can filter, sort, edit, and export.

## What the finished app gives the user

- A **home page that is the interview pipeline**: one card per interview round (badge, who
  runs it, duration, question count, focus, must-prep/mastered counts) in a top-to-bottom flow
  with connectors — tap a round to see its questions, or "Browse all". This is the landing view.
- A **question bank** grouped into **interview-theme sections** (Intro & motivation, Experience,
  Behavioral, Role skills, Company & industry, and Questions to ask) in a natural interview
  order — no priority, no letter IDs — with a sidebar (a slide-in drawer on mobile) to filter by
  interview round, a high-risk toggle, and a "Questions to ask" toggle, plus search. Drag any
  question to reorder it (the candidate's own way to prioritize).
- Each question opens as its **own full-page view** (not a cramped accordion) with five
  editable sections: **Strategy**, **Bullet points**, **AI answer**, **My answer**,
  **Follow-up questions**, plus per-question **round** checkboxes (one per interview round),
  also editable inline from the list.
- Everything the builder writes is a **default layer**. The moment the user edits a field,
  their text is saved to the browser's localStorage and overrides the default forever —
  so regenerating the file never destroys their work. They also get **Export all (.md)**
  (a readable copy of the whole bank) and **Backup/Import (.json)** for moving between
  devices.

You never hand-write the HTML. You produce a **spec JSON** and run `scripts/build.py`,
which injects it into `assets/template.html`. Your real work is **generating a great
question bank and great draft content** — the app shell is already built and tested.

## Workflow

Two gates, otherwise automatic: **(1)** if the candidate's background is missing, ask once;
**(2)** confirm the interview *process* (rounds, who, goal), the interview *language*, **and how
many common baseline questions to include** (see the scale choice in step 4) before generating,
because different job families interview completely differently and a wrong process shape wastes
the whole output. Everything else — questions, answers, themes — you generate without
stopping; the user refines in the app.

### 1. Gather inputs (gate 1)

- **The JD** — a link (fetch it), an image (read it), pasted text, or a file. Read it fully.
- **The candidate's background** — resume, portfolio (for design/art/creative roles, a
  portfolio URL or images), pasted text, or an earlier part of the conversation. **If you
  have nothing about them, ask once.** If they have no resume, **degrade gracefully**: still
  generate the full bank and strategies, but write answers as skeletons with explicit
  `[Fill in …]` placeholders, and say the answers are scaffolds to complete.

### 2. Classify the job family, then research the process

Interview processes are shaped by role type, so first **classify** from the JD/resume/
portfolio: engineering, design/UX, art (game/visual), data/ML, product, marketing, sales,
operations, research, etc. The job family drives both the interview pipeline *and* which
question areas the bank needs to cover.

Then **research the typical process** with web search — you often don't know a specific
company's or role's real pipeline, and it's very searchable. Search things like
`"{company} {role} interview process"` and `"{job family} interview rounds stages"`. You're
looking for: how many rounds, who runs each, each round's goal, and any role-specific stages
that a generic ladder would miss. Examples of what this surfaces:

- **Engineering** — recruiter screen → online coding challenge → technical/algorithm
  interviews → onsite (system design + behavioral).
- **Design / UX** — recruiter screen → portfolio review → design challenge / whiteboard →
  onsite (craft + collaboration + behavioral).
- **Art / visual design** — recruiter screen → portfolio review → **art/design exercise**
  (take-home) → panel with the creative lead.
- **Product** — recruiter → hiring manager → product-sense + analytics/execution rounds →
  onsite panel.
- **Marketing / Sales** — recruiter → hiring manager → skills/case or mock exercise → panel.

Skip or shortcut the search only when the user already told you the exact process.

### 3. Assemble the questions: common baseline + role research

Every bank is built from **two layers**:

1. **The common baseline** — `references/common-questions.md` holds the universal questions asked
   in almost any interview (tell me about yourself, weaknesses, why this job, why leaving, biggest
   achievement, questions to ask, etc.), ranked into tiers. **Always include this baseline**, at
   the size the user picks in the step-4 scale gate (~10 / ~20 / ~all). Adapt each to the real
   candidate and role; drop any that genuinely don't fit.
2. **Role- and résumé-specific questions** — layered *on top* of the baseline. For roles with a
   well-known canon (coding/algorithms, system design, product sense, consulting cases), **search
   for the frequently-asked questions** (`"{job family} most common interview questions"`,
   `"{company} interview questions"`) and fold the real recurring ones in. Then add the
   **résumé/portfolio-specific** questions (step 5) — the candidate's own history is where
   interviews are won.

The baseline keeps every bank solid; the role/résumé layer makes it *theirs*. Neither alone is
enough — always ship both.

### 4. Confirm the process AND the interview language (gate 2)

Before generating, present the researched pipeline compactly and let the user correct it —
they know their real process, you're proposing a well-researched default. Show, per round:
**label · who runs it · its goal · rough duration · rough number of questions**. For example:

> Here's the process I'll build around (from research on {company}/{role}) — tell me what to fix:
> - **R1 · Recruiter screen** — recruiter · fit & motivation · ~30 min · ~6 questions
> - **R2 · Coding challenge** — online · pass the automated test · ~90 min · ~2 problems
> - **R3 · Technical interviews** — engineers · live algorithms · ~60 min · ~3 questions
> - **R4 · Onsite** — panel + manager · system design & behavioral · ~4 hrs · ~8 questions

**Always confirm the interview language** in the same step — you cannot guess it reliably. An
English JD at a multinational may still interview in the local language, and many processes are
**mixed** (recall a China/APAC role where the local-manager round is in Mandarin but the global
round is in English). Ask explicitly, e.g. "What language will the interview be in — English,
Chinese, or mixed by round?" If it varies by round, note which round is which language.

**In the same step, confirm the baseline scale** — how many of the common questions to include.
Offer three choices (the role-specific questions from step 3/5 are always added *on top* of
whichever they pick):

> How many common baseline questions should I include (I'll add role- and résumé-specific ones
> on top of any of these)?
> - **~10 essentials** + role-specific — a focused, fast-to-prep bank
> - **~20 thorough** + role-specific — solid coverage of the usual ground *(a good default)*
> - **~26 / all common** + role-specific — exhaustive; leave nothing to chance

Map their pick to the tiers in `references/common-questions.md` (~10 = Tier 1; ~20 = Tier 1+2;
all = Tier 1+2+3). If they don't care, default to ~20.

Once confirmed, encode each round in the spec's `rounds` map **as an object** with
`label, who, goal, minutes, count, focus` — the app renders a **Process** overview page and a
round-info banner from this. Use the per-round `count` and `minutes` to **size the bank**: a
90-minute coding round with ~2 problems needs a handful of strong coding questions, not
twenty; a 4-hour onsite needs broad coverage. Let the real process set how many questions land
in each round.

### 5. Find the landmines

Before writing content, scan JD × resume for **high-stakes questions** — where a weak answer
could sink the candidacy: layoffs, a project that underperformed, a metric that looks
inflated, a claim the interviewer can verify (e.g. a former colleague now works there),
employment gaps. Mark each `"status":"risk"` and, in its Strategy, name the trap plainly.
These are the questions the whole tool exists to defuse — don't bury them.

### 6. Generate the question bank

This is the heart of the skill. Think like an experienced interviewer for *this specific
role at this specific company*, cross-referenced with *this specific candidate's* history.

**Start from the common baseline, then layer role/résumé questions on top.** First lay in the
chosen tier of `references/common-questions.md` (the scale the user picked in step 4), each
adapted to the real candidate and role. Then add the role canon (step 3) and the
résumé/portfolio-specific questions (step 5) on top. The total is baseline + role-specific — so
"~20 common" plus, say, 30–50 role/résumé questions is a full, substantial bank. Assign each
question to the round(s) it actually belongs in (step 4), and size each round by its real length.

**The two things you assign per question are its interview round(s) and its theme (`grp`).**
Every normal question gets `rounds` (R1 / R2 / R3 / R4 … — step 4) and a `grp` — one of a small
fixed set of interview themes: **`intro`** (Intro & motivation), **`experience`** (Experience
deep-dive), **`behavioral`**, **`craft`** (Role skills), **`company`** (Company & industry). The
app groups the bank into those theme **sections in that fixed order** — so it reads like a natural
interview flow — and filters it by round. **There is no priority** (no P1/P2/P3, no Must prep) — if
a candidate wants to prioritize, they just drag questions to reorder. Everything else about a
question (wording, answer, round, theme) is the **user's to edit afterward**; you just give a
strong, complete starting point.

**Do NOT use A/B/C/D letters or per-run category names.** The `grp` themes are a fixed set — you
don't invent new ones. Assign each question the theme it truly belongs to (a weakness question is
`behavioral`, a "why this company" is `intro`, a system-design question is `craft`, etc.). Write
questions within a theme in a sensible order; the app keeps that authored order inside each section.

**"Questions to ask the interviewer" use `cat:"F"` (not a `grp`).** These are the reverse
questions the *candidate* asks (not questions they answer). Mark each one `cat:"F"` and the app
pulls them into a dedicated "🙋 Questions to ask" section at the end, with its own sidebar toggle.
Give them a `rounds` value (so they sort by which round to ask in); their `ai` field is just the
question phrased ready to say out loud (no model answer). Everything else stays `cat:"Q"` with a `grp`.

Cover the areas that fit the job family:

- **Engineering** — Coding & Algorithms · System Design · CS fundamentals · Project deep-dive.
- **Design / UX** — Portfolio walkthrough · Design process & craft · Design challenge/critique
  · Collaboration.
- **Art / visual design** — Portfolio & style range · Exercise debrief · Pipeline & tools ·
  Art direction fit.
- **Product** — Product sense · Analytics & execution · Strategy · Project deep-dive.
- **Marketing / Sales / others** — the craft competencies named in the JD, asked as
  "how do you…" and "walk me through…".

These coverage areas map directly onto the `grp` themes — almost every bank covers all of them:
- **`intro`** — Intro & motivation (tell me about yourself, why this role/company, why leaving,
  gaps, salary, 5 years, first-90-days).
- **`experience`** — Experience / portfolio deep-dive. **This should be one of the biggest
  sections, not an afterthought — it's where most interviews are won or lost.** Give each major
  project, role, or achievement on the résumé its **own top-level question** (a general "walk me
  through your background / your last role" plus one per significant piece). Do NOT bury the whole
  deep-dive inside follow-ups — the probes (their exact role vs the team's, the real numbers, what
  they'd change) go in `fu`, but the projects themselves are standalone `experience` questions. A
  résumé-heavy role should have roughly 4–8 experience questions, comparable to craft and intro.
- **`behavioral`** — disagreement, failure, conflict, ambiguity, weakness, strength, influence.
- **`craft`** — the role-specific skill questions above (coding, system design, product sense,
  funnel analysis, etc.).
- **`company`** — Company & industry (product, market, competitors — some requiring homework).
- **`cat:"F"`** — Questions to ask the interviewer (the reverse questions the candidate asks).

**Minimum 5 questions per theme.** Every generation must give **each** theme — `intro`,
`experience`, `behavioral`, `craft`, `company` — **at least 5 substantive questions**, and at
least 5 questions-to-ask (`cat:"F"`) too. No thin sections. The two that tend to come out thin
are `experience` (see above — one top-level question per project/role) and `company` — for
`company`, get to 5 with *real* questions (their product, competitors, market, ideal customer,
GTM, recent news, why-them-specifically), never filler. If you genuinely can't find 5 real
questions for a theme, that's a signal to research the role/company more, not to pad.

**Follow-ups matter, and each one gets its own strategy AND prepared answer.** Real interviewers
rarely accept the first answer. For every substantial question, add 1–3 follow-ups in that
question's **`fu` field** — as an **array of `{"q": "...", "st": "...", "ai": "..."}` objects**:
`st` is a **one-line strategy** (how to approach it / the pitfall to avoid), and `ai` is a
**concise 2–4 sentence model answer** (shorter than a main answer — a follow-up is a drill-down).
The strategy is what makes a follow-up genuinely useful, so don't skip it. This way, when the user
taps a follow-up to open it, it's already prepped with both coaching and an answer, not blank.
Do **not** create separate `par` questions for follow-ups — they live inside the parent, and in
the app tapping a follow-up promotes it into its own full card (carrying its prepared answer) on
demand. So even a high-stakes follow-up (e.g. a metric-level drill-down on a weak result) goes in
the parent's `fu` with its own short answer. Carry the landmines from step 5 into the bank as
`"status":"risk"` questions.

### 7. Write the content for each question

Write every answer in the **interview language confirmed in step 4** — not the chat language.
An English interview → English answers even if you're chatting in Chinese; a Mandarin
interview → Chinese answers. If the process is **mixed by round**, write each question's
Strategy/AI-answer in the language of the round(s) it belongs to (e.g. a Mandarin local-manager
round gets Chinese answers; the English global round gets English).

**Right length per field:** the AI answer is a **read-only reference in the app** (the user
studies it and writes their own in "My answer"), so make it a **complete, interview-ready model
answer** — the full arc, spoken-length, genuinely usable as-is, not a compressed sketch. The
**Strategy** stays tight (1–3 sentences of coaching) and **Bullet points** are the terse
scannable version — brevity lives there, not in the AI answer.

**First check `references/answer-frameworks.md`.** It holds proven, question-specific
structures (e.g. a 4-part "Tell me about yourself"). When a question matches one there, use
that structure for its answer — it beats the generic recipe below. Otherwise fall back to the
type-recipe here.

**Each field has a fixed shape by question TYPE — but fill it with this candidate's real
history, so answers stay consistent without turning formulaic.** Match the recipe to the
question; don't force one template onto everything.

- **Strategy (`st`)** — always 1–3 sentences: the angle + the structure to reach for + the
  pitfall to avoid. For risk questions, name the trap plainly. This is coaching, not the
  answer.
- **AI answer (`ai`)** — a **complete, interview-ready model answer** the candidate can study
  and speak from. Full and self-contained, not a sketch. Pick the shape by question type:
  | Question type | Answer shape |
  |---|---|
  | Motivation / *why* (why this company/role, why leaving) | the full spoken answer (~150–200 words): 3 reasons, each developed with real evidence, points numbered ①②③ |
  | Behavioral / *tell me about a time* | a complete Context → Action → Result → Learning story (CARL — see answer-frameworks.md), prose, most of it on *your* Action, ending on the Learning |
  | Craft / *how do you… / walk me through…* | a **named framework**, its steps fully explained, and a concrete worked example |
  | Technical / knowledge (coding, system design, "explain X") | the real, correct, complete technical content — the approach, the key steps, and the trade-off, enough to actually answer |
  | Resume / portfolio deep-dive | the full story of the project with real metrics, and the your-role-vs-team boundary |
  | Questions to ask | the actual question(s) to say, phrased ready-to-use |
- **Bullet points (`bp`)** — seed **3–5 short scannable points** distilled from the AI answer
  (one idea per line) — the at-a-glance version the user rehearses from. Keep them terse
  (fragments, not sentences). The user will edit these, so give a strong starting point, not
  a wall of text.
- **Follow-up questions (`fu`)** — an array of `{"q": "...", "st": "...", "ai": "..."}`: the
  question, a **one-line strategy**, and a **concise 2–4 sentence model answer**. **Never add ID
  cross-references like `(→ B3)`** — question IDs are not shown anywhere in the app.

**Ground every answer in the candidate's *real* history.** When only the candidate knows a
number or a name you can't invent, write the surrounding answer and leave an explicit
placeholder like `[Fill in the exact D7 retention number before the interview]`. Honest
placeholders beat fabricated specifics — in the AI answer *and* the bullet points.

### 8. Assign rounds and theme

- **`rounds`** — which interview rounds each question fits (using the round numbers you
  confirmed in step 4). Screening/motivation → early rounds; deep craft and problem-solving →
  later rounds; verification of resume claims → whoever can actually check (often the hiring
  manager who knows the space).
- **`grp`** — the interview theme: `intro` / `experience` / `behavioral` / `craft` / `company`
  (or `cat:"F"` for questions-to-ask). This is the only grouping — the app renders the bank as
  theme sections in that order, so it reads like a real interview. Assign the theme each question
  genuinely belongs to; don't invent new theme names. **No priority** — the candidate drags to
  reorder if they want to prioritize.

### 9. Build and deliver

Write the spec to a JSON file and run the builder:

```bash
python3 scripts/build.py spec.json "<Company>_Interview_Prep.html"
```

Save the output where the user can find it (the Desktop is a good default on a personal
machine, or ask). Then tell them, briefly:
- what they got (a question bank they can filter/edit, N questions, the high-risk count),
- that their edits autosave and survive re-generation,
- to click **Backup edits (.json)** once in a while, and **Export all (.md)** to send you
  the whole thing if they want you to revise it later,
- and call out any `[Fill in …]` placeholders — the real numbers only they know.

The exact spec JSON schema is documented at the top of `scripts/build.py` and in
`references/spec-schema.md`. Read the schema before writing the spec.

## Notes

- **The app shell carries a considered, tested design — don't re-design it per run.** The
  template ("Interview War-Room" design): a masthead with a company logo mark + title, a home
  page that lays out the interview rounds as a pipeline (the landing view), a left sidebar of
  filters (round / high-risk / questions-to-ask) that becomes a slide-in drawer on mobile,
  inline-editable round chips, drag-to-reorder, and a full-page detail view. Navy/slate
  palette, serif headers, responsive and theme-aware. Generating good-looking output is the
  template's job — do **not** invoke a frontend-design pass or hand-roll HTML per generation;
  that produces inconsistent, untested results. Your effort goes into content quality.
- **If the design genuinely needs to change**, edit `assets/template.html` once (it's the
  shared layer, so every future build inherits the fix), then rebuild a sample and verify it
  in a browser before considering it done. That's rare.
- **One file, works offline, private.** No data leaves the machine; edits live only in that
  browser. That's a feature — say so if privacy comes up.
- **Regenerating is safe.** If the user later gets more resume detail or a changed JD, you
  can rebuild from an updated spec; their in-browser edits still win over your new defaults.
