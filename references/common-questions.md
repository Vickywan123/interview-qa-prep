# Common interview questions (baseline bank)

A ranked baseline of the questions asked in almost any interview, regardless of role. **Every
generated bank starts from this set** (the top N the user picked in the scale gate), then adds
role- and résumé-specific questions on top of it.

Source: Jeff Haden, "27 most common job interview questions and answers." The one-line notes
below are the article's answer angle. When a question also has a detailed structure in
`answer-frameworks.md`, use that structure for the AI answer — this file just says *which*
questions form the baseline and *roughly* how to angle each.

The list is split into three tiers by how universally the question gets asked. The scale gate
maps to these tiers:

- **~10 (essentials)** → Tier 1
- **~20 (thorough)** → Tier 1 + Tier 2
- **~27 / all (exhaustive)** → Tier 1 + Tier 2 + Tier 3

Always adapt the wording and answer to the real candidate and target role; drop any that make
no sense for the role, and never let a baseline question crowd out a strong role-specific one.

---

## Tier 1 — the ~10 asked in almost every interview

1. **Tell me a little about yourself.** — Connect the dots on the résumé: why each move, the
   throughline to *this* role. *(structure: `answer-frameworks.md` → "Tell me about yourself")*
2. **What are your biggest weaknesses?** — A real weakness you're actively fixing; behaviour →
   fix → result. *(structure: `answer-frameworks.md` → "biggest weakness")*
3. **What are your biggest strengths?** — Pick one with direct application to the JD; prove it
   with a short story. *(structure: `answer-frameworks.md` → "greatest strength")*
4. **Why do you want this job?** — Tie the specific role to the candidate's short- and long-term
   goals; show they understand what the job actually is.
5. **Out of all the candidates, why should we hire you?** — Surface qualifications not yet
   discussed; the specific combination they get.
6. **What is your biggest professional achievement?** — Pick one directly relevant to this role;
   real numbers.
7. **Why do you want to leave your current job?** — Forward-looking, never bitter. *(structure:
   `answer-frameworks.md` → "Why did you leave")*
8. **Where do you see yourself in five years?** — Talk about the work and impact, not a title;
   signal you'll stay. *(structure: `answer-frameworks.md` → "Where in 5 years")*
9. **Tell me about a time a co-worker or customer got angry with you.** — Own it, fix it, name
   the lesson; no blame. *(behavioral → CARL in `answer-frameworks.md`)*
10. **What questions do you have for me?** — Thoughtful questions that show genuine interest and
    let the candidate assess fit (see the reverse-questions in Tier 3).

## Tier 2 — the next ~10 (very common)

11. **How did you hear about the opening?** — A referral or targeted company research beats "a
    job board."
12. **Describe your dream job.** — Connect elements of *this* role to long-term aspirations.
13. **What kind of work environment do you like best?** — Align honestly with the company's
    actual culture.
14. **Tell me about the toughest decision you made in the last six months.** — Show judgment:
    both data and human impact. *(behavioral → CARL)*
15. **What is your leadership style?** — Concrete examples of leadership challenges, not generic
    labels. *(behavioral → CARL)*
16. **Tell me about a time you disagreed with a decision.** — Raise concerns professionally, then
    support the call and move forward. *(behavioral → CARL)*
17. **How do you think other people would describe you?** — Authentic; highlight reliability and
    work ethic.
18. **What can we expect from you in your first three months?** — How you'll find value-creating
    work and serve all stakeholders.
19. **What do you like to do outside of work?** — Something showing growth or skill, plus a bit of
    genuine personality.
20. **What was your salary in your last job? / salary expectations?** — Deflect to a desired range
    and ask if the role fits it; don't anchor on a past number.

## Tier 3 — the remaining ~7 (situational + reverse questions to ask them)

21. **Brain-teaser / puzzle** (e.g. "A snail climbs a 30-foot well…"). — They're testing your
    reasoning out loud, not the answer. Think transparently.
22. **What do you expect me to accomplish in the first 90 days?** *(reverse — ask them)* — Shows
    you want to contribute fast and know the success metrics.
23. **What three traits do your top performers share?** *(reverse)* — Learn what drives success
    here, then align.
24. **What really drives results in this job?** *(reverse)* — Understand the highest-impact
    activities.
25. **What are the company's highest-priority goals this year, and how would my role contribute?**
    *(reverse)* — Signals interest in meaningful work.
26. **What percentage of employees were referred by current employees?** *(reverse)* — A read on
    culture and workplace quality.
27. **What do you plan to do if [anticipated business challenge]?** — Forward-thinking; discuss how
    you'd handle a likely challenge for the team/company.

---

**Reverse questions (#10 and 22–26) are "questions to ask the interviewer" — mark them `cat:"F"`**
so the app pulls them into the dedicated "🙋 Questions to ask" section. Phrase them ready-to-say
(the `ai` field is just the question, no model answer). Everything else is a question *they* ask
the candidate → `cat:"Q"`.
