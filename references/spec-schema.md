# Spec JSON schema

The spec is a single JSON file you write, then feed to `scripts/build.py`. It is the only
thing you author; the app shell is fixed.

## Top level

| field        | type            | required | notes |
|--------------|-----------------|----------|-------|
| `page_title` | string          | no       | Browser tab title. |
| `header_h1`  | string          | yes      | Big title in the masthead. |
| `mark`       | string          | no       | 2-letter logo mark in the masthead. Defaults to initials derived from the company (text before the first "·" in `header_h1`). |
| `header_sub` | string (light HTML ok) | no | One-line subtitle. Good place to spell out the round map, e.g. `"Acme · <b>R1</b> Recruiter  <b>R2</b> Hiring Manager  <b>R3</b> Panel"`. |
| `categories` | object          | yes      | **Use exactly two fixed keys:** `{"Q":"Questions", "F":"Questions to ask"}`. Cat `"Q"` = normal questions (grouped into theme sections via each question's `grp`). Cat `"F"` = the **reverse questions the candidate asks the interviewer**; the app pulls them into a dedicated "🙋 Questions to ask" section with its own sidebar toggle. Don't invent other category keys. |
| `rounds`     | object          | no       | Map of round number (string) → **label string** OR a **round object** (below). **Any number of rounds** — 2, 3, 6, whatever the real process is. Defaults to a 3-round ladder. Each question's `rounds` array must reference numbers defined here. |

### Round object (recommended — powers the Process page)

Instead of a plain label string, give each round an object so the app can render a **Process**
overview page and a round-info banner:

```json
"rounds": {
  "1": {"label":"R1 · Recruiter screen", "who":"Recruiter", "goal":"Fit & motivation", "minutes":30, "count":6, "focus":"Background, motivation"},
  "2": {"label":"R2 · Coding challenge", "who":"Online / HackerRank", "goal":"Pass the automated test", "minutes":90, "count":2, "focus":"Data structures, algorithms"},
  "3": {"label":"R3 · Onsite", "who":"Panel + manager", "goal":"System design & behavioral", "minutes":240, "count":8, "focus":"System design, leadership"}
}
```

| round field | meaning |
|-------------|---------|
| `label`   | shown everywhere (filter, badges, headers). Required if using the object form. |
| `who`     | who runs the round. |
| `goal`    | what the round is trying to decide. |
| `minutes` | rough duration. |
| `count`   | rough number of questions/problems asked in that round. |
| `focus`   | one-line focus areas. |

Mixing forms is fine (some rounds objects, some plain strings). If no round has any metadata,
the Process page is hidden automatically.
| `jd_html`    | string (light HTML) | no   | The job description rendered on the "Job Description" page. Use `<h3>`, `<ul><li>`, `<p>`. Keep it readable, not the raw scrape. |
| `questions`  | array           | yes      | The question objects below. |

## Question object

| field    | type      | required | notes |
|----------|-----------|----------|-------|
| `id`     | string    | yes      | Unique, flat sequential: `Q1`, `Q2`, `Q3`, … in the order you write them. **No category letters** (never `A1`/`B2`). IDs are internal keys only — never shown to the user. |
| `cat`    | string    | yes      | `"Q"` for normal questions (the vast majority). `"F"` **only** for reverse "questions to ask the interviewer" — those get pulled into the dedicated "🙋 Questions to ask" section. Never other values. |
| `grp`    | string    | yes (for cat `"Q"`) | The interview theme — one of `"intro"` / `"experience"` / `"behavioral"` / `"craft"` / `"company"`. The app renders theme **sections in that fixed order** (this is the only grouping). Assign the theme the question truly belongs to. Not needed for cat `"F"` (those form their own section). |
| `q`      | string    | yes      | The question text. |
| `rounds` | int array | yes      | Which interview rounds, e.g. `[2,3]`. Use `[1,2,3,4]` for "any round". |
| `status` | string    | no       | `"todo"` (default) or `"risk"` (high-stakes; renders red, has its own filter). |
| `par`    | string    | no       | **Don't set this in the spec.** Follow-ups belong in the parent's `fu` field. `par` is used internally by the app when the user promotes a follow-up line into its own question. |
| `st`     | string    | no       | Strategy: how to approach the answer (1–3 sentences). |
| `bp`     | string    | no       | Bullet points: 3–5 short scannable points distilled from the answer, one per line (`\n`-separated). The user edits these. |
| `ai`     | string    | no       | The draft answer. Use `\n\n` between paragraphs. |
| `fu`     | array     | no       | Follow-up questions, **each with its own strategy and short answer** so opening one isn't blank. An array of `{"q": "...", "st": "...", "ai": "..."}` objects (`st` = a one-line strategy; `ai` = a concise 2–4-sentence model answer; `bp` optional). A plain `"line1\nline2"` string still works for bare probes with no prepared content. |

Do **not** set `my` (the user's own answer) — that field is the user's to fill in the browser.

## Escaping

Write the JSON normally (as data). `build.py` handles JS-escaping when it injects `jd_html`
into the page. In `ai`/`st` (and each follow-up's `ai`), plain text is fine — newlines as `\n`. Don't pre-escape
HTML entities; the app escapes text at render time.

## Minimal example

```json
{
  "page_title": "Acme · PM — Interview Prep",
  "header_h1": "Acme · Product Manager — Interview Question Bank",
  "header_sub": "Acme Corp · <b>R1</b> Recruiter  <b>R2</b> Hiring Manager  <b>R3</b> Panel",
  "categories": {"Q":"Questions", "F":"Questions to ask"},
  "rounds": {"1":"R1 · Recruiter", "2":"R2 · Hiring Manager", "3":"R3 · Panel"},
  "jd_html": "<h3>About the role</h3><ul><li>Own the checkout roadmap.</li><li>Partner with data on metrics.</li></ul>",
  "questions": [
    {"id":"Q1","cat":"Q","grp":"intro","q":"Tell me about yourself","rounds":[1,2,3],
     "st":"Two minutes, clear arc: background → most relevant role → why this next.",
     "ai":"I started in ①… then ②… which led me to ③…",
     "fu":[{"q":"Give the 30-second version.","st":"Compress ruthlessly — one line each on what you do, your best proof, the fit.","ai":"A tight three-sentence version: what I do, my strongest proof point, why this role."},
           {"q":"Why this role?","st":"Lead with their need, not your CV.","ai":"Tie the role's core to my track record and what I want to do next."}]},
    {"id":"Q2","cat":"Q","grp":"experience","q":"Walk me through your biggest launch","rounds":[2,3],
     "status":"risk",
     "st":"Story arc. Name your exact role vs the team's — they may probe it.",
     "ai":"Context: … Action: … Result: … Learning: …",
     "fu":[{"q":"What was YOUR part vs the team's?","st":"Be specific about what YOU owned; vague 'we' invites doubt.","ai":"I owned ①②③; the team owned the build."},
           {"q":"What would you do differently?","st":"Name one concrete change + the learning — growth, not defensiveness.","ai":"I'd do X differently, and here's what it taught me."}]},
    {"id":"Q3","cat":"F","q":"What does success look like for this role in the first year?","rounds":[2,3],
     "st":"A reverse question you ASK the interviewer — cat \"F\" pulls it into the 'Questions to ask' section.",
     "ai":"(This is a question you ask them — phrase it ready to say out loud.)"}
  ]
}
```

## Build

```bash
python3 scripts/build.py spec.json "Acme_Interview_Prep.html"
```

The builder prints a summary (question count, questions-to-ask count, high-risk count) and writes the
self-contained HTML file.
