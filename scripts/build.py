#!/usr/bin/env python3
"""
Build an interactive interview Q&A prep HTML from a spec JSON.

Usage:
    python build.py spec.json output.html

The spec JSON schema:
{
  "page_title": "Acme · PM — Interview Prep",   # browser tab title
  "header_h1":  "Acme · Product Manager — Interview Question Bank",
  "header_sub": "Acme Corp · R1 Recruiter  R2 Hiring Manager  R3 Panel",  # plain text or simple HTML
  "categories": {"Q":"Questions", "F":"Questions to ask"},   # two fixed keys: Q = normal, F = reverse questions to ask
  "rounds": {"1":"R1 · HR", "2":"R2 · Hiring Manager", "3":"R3 · Panel"},  # any count; labels shown in the filter

  "jd_html": "<h3>About</h3><ul><li>...</li></ul>",   # the job description as light HTML
  "questions": [
    {
      "id": "Q1",              # unique, flat sequential (Q1, Q2, …); internal key, never shown
      "cat": "Q",              # "Q" = normal question; "F" = reverse "question to ask the interviewer"
      "grp": "intro",          # theme (cat "Q" only): intro|experience|behavioral|craft|company
      "q": "Tell me about yourself",
      "rounds": [1,2,3],       # which interview rounds this belongs to
      "status": "todo",        # "todo" or "risk" (risk = high-stakes, shown red)
      "par": "A0",             # optional: id of the parent question if this is a follow-up
      "st": "Strategy text...",       # how to approach the answer (1-3 sentences)
      "bp": "point 1\npoint 2...",    # 3-5 short scannable bullet points (optional)
      "ai": "Draft answer text...",   # the model-written answer
      "fu": [                    # follow-up questions, each with a strategy + short answer (optional)
        {"q": "Follow-up question?", "st": "One-line strategy.", "ai": "A concise 2-4 sentence answer."},
        {"q": "Another follow-up?", "st": "...", "ai": "..."}
      ]                          # (a plain "line1\nline2" string still works for bare probes)
    }
  ]
}

Everything the builder writes is a DEFAULT layer. When the user edits anything
in the page, their edits live in the browser's localStorage and always override
these defaults, so re-generating the file never destroys their work.
"""
import json
import re
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 3:
        print("Usage: python build.py spec.json output.html", file=sys.stderr)
        sys.exit(1)

    spec_path, out_path = Path(sys.argv[1]), Path(sys.argv[2])
    spec = json.loads(spec_path.read_text(encoding="utf-8"))

    template_path = Path(__file__).resolve().parent.parent / "assets" / "template.html"
    html = template_path.read_text(encoding="utf-8")

    # --- validate lightly, fail loud on the common mistakes ---
    cats = spec.get("categories") or {}
    if not cats:
        sys.exit("spec.categories is required and must be non-empty")
    questions = spec.get("questions") or []
    if not questions:
        sys.exit("spec.questions is required and must be non-empty")

    seen = set()
    for q in questions:
        qid = q.get("id")
        if not qid:
            sys.exit(f"a question is missing an id: {q}")
        if qid in seen:
            sys.exit(f"duplicate question id: {qid}")
        seen.add(qid)
        if q.get("cat") not in cats:
            sys.exit(f"question {qid} has cat={q.get('cat')!r} not in categories")
        # normalize: strip empty optional (string) fields so the page stays clean
        for k in ("sub", "par", "st", "bp", "ai"):
            if k in q and not (q[k] or "").strip():
                del q[k]
        # fu may be a string (one per line) or a list of {q, st, ai, bp}; drop if empty
        if "fu" in q:
            fu = q["fu"]
            if (isinstance(fu, str) and not fu.strip()) or (isinstance(fu, list) and not fu):
                del q["fu"]
        q.setdefault("rounds", [])
        q.setdefault("status", "todo")
        if q.get("status") not in ("todo", "risk"):
            q["status"] = "todo"
        # keep only known keys, in a stable order
    parents = {q["id"] for q in questions}
    for q in questions:
        if q.get("par") and q["par"] not in parents:
            # a dangling parent link would just render a dead chip; drop it
            del q["par"]

    # rounds referenced by questions must exist in the round map, or they'd be
    # unfilterable and uncheckable in the UI. Warn loudly rather than silently drop.
    defined_rounds = {int(k) for k in (spec.get("rounds") or {"1": "", "2": "", "3": ""})}
    for q in questions:
        stray = [r for r in q.get("rounds", []) if r not in defined_rounds]
        if stray:
            print(f"warning: {q['id']} references round(s) {stray} not in "
                  f"spec.rounds {sorted(defined_rounds)}", file=sys.stderr)

    # DATA is injected as a JS array literal. json.dumps produces valid JS.
    # rounds: map of round-number(str) -> label OR a richer object with metadata
    # {"label","who","goal","minutes","count","focus"}. Default to a 3-round ladder.
    raw_rounds = spec.get("rounds") or {"1": "R1", "2": "R2", "3": "R3"}
    rounds_label, rounds_meta = {}, {}
    for k, v in raw_rounds.items():
        k = str(k)
        if isinstance(v, dict):
            rounds_label[k] = v.get("label") or ("R" + k)
            rounds_meta[k] = {mk: v[mk] for mk in ("who", "goal", "minutes", "count", "focus")
                              if v.get(mk) not in (None, "")}
        else:
            rounds_label[k] = v
            rounds_meta[k] = {}

    # A per-file localStorage namespace so edits in one prep bank never bleed into
    # another (question IDs like A1/B1 collide across jobs otherwise). Derived from
    # the title so the same bank keeps its edits across re-generations.
    slug = re.sub(r"[^a-z0-9]+", "-", (spec.get("header_h1") or "bank").lower()).strip("-")[:48]
    store_key = "iprep_" + (slug or "bank")

    # logo mark: 2-letter initials. Explicit spec.mark wins; else derive from the
    # company (text before the first "·" in the title), else first 2 letters.
    mark = spec.get("mark")
    if not mark:
        company = (spec.get("header_h1") or "").split("·")[0]
        words = re.findall(r"[A-Za-z0-9]+", company)
        if len(words) >= 2:
            mark = (words[0][0] + words[1][0]).upper()
        elif words:
            mark = words[0][:2].upper()
        else:
            mark = "IP"

    data_js = json.dumps(questions, ensure_ascii=False)
    cats_js = json.dumps(cats, ensure_ascii=False)
    rounds_js = json.dumps(rounds_label, ensure_ascii=False)
    roundmeta_js = json.dumps(rounds_meta, ensure_ascii=False)

    # JD goes inside a template literal — escape backslash, backtick, ${ }
    jd = spec.get("jd_html", "")
    jd = jd.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")

    def esc_attr(x):  # header/title are plain text or trusted light html; keep simple
        return (x or "").replace("\\", "\\\\")

    replacements = {
        "__PAGE_TITLE__": spec.get("page_title", "Interview Question Bank"),
        "__HEADER_H1__": spec.get("header_h1", "Interview Question Bank"),
        "__HEADER_SUB__": spec.get("header_sub", ""),
        "__CATS__": cats_js,
        "__ROUNDS__": rounds_js,
        "__ROUNDMETA__": roundmeta_js,
        "__DATA__": data_js,
        "__JD__": jd,
        "__STOREKEY__": store_key,
        "__MARK__": mark,
    }
    for k, v in replacements.items():
        html = html.replace(k, v)

    out_path.write_text(html, encoding="utf-8")
    n_ask = sum(1 for q in questions if q.get("cat") == "F")
    n_risk = sum(1 for q in questions if q.get("status") == "risk")
    print(f"Built {out_path}")
    print(f"  {len(questions)} questions | {n_ask} to-ask | {n_risk} high-risk")


if __name__ == "__main__":
    main()
