# /bob reliability spine

This reference is loaded by SKILL.md at the start of every run. It defines the
fixed phase spine, the tiered-by-blast-radius decision rule, the hot-zone list,
and the dependency-fallback rules. ASCII-only.

The honest framing (load-bearing): /bob converts the question "will the result
be up to standard?" into "it is proven up to standard, or it stopped and told
you why." It is a conductor, not a correctness guarantee.

## The 7-phase spine

Follow these phases in order. Never skip PLAN+CLAIM. FAN-OUT and VERIFY delegate
their heavy work to the Workflow tool in bounded waves; the rest runs in the main
conductor loop.

1. INTAKE (read-only) - Two input modes (classify via bob_run.py classify-input):
   DOC MODE (`/bob <path>`) reads the doc + repo context and adopts/derives its
   gates; GOAL MODE (`/bob "free text"`) drafts the definition-of-done from the
   sentence (the /goal capture step). Either way make ZERO writes here and produce
   the checkable gates + independent sub-units. Goal mode writes its drafted
   goal-spec.md into the run dir at PLAN+CLAIM (after confirm), never earlier.
2. PLAN+CLAIM - Present the PLAN to the user and make no writes until confirm;
   on confirm, scaffold the run dir, drop the claim/lockfile, and cut a dedicated
   branch in the affected git subproject.
3. FAN-OUT - Write a Workflow script per wave; each agent worklogs to
   agents/agent-NN.md, polls control.md at checkpoints, and drops an evidence
   artifact into evidence/ per gate.
4. VERIFY - Per sub-unit, enforce the evidence floor, run the adaptive verifier
   by task type, then a blind refute-council that tries to break "gate met";
   majority refute = fail. The evidence floor is EXISTENCE-AND-SUBSTANCE, not just
   existence: the artifact must be produced by an INDEPENDENT verifier that
   re-runs the check (test/benchmark/build), not self-reported by the agent that
   did the work, and the refute-council must explicitly attack "is this evidence
   real and does it map to this gate" -- a non-empty but hollow/fabricated file
   does NOT satisfy the floor.
5. GATE (human, timeout-default) - Present artifacts plus the refute-council
   verdict; on no-response within the window, default to that verdict for
   non-hot-zone gates and log a reversible decision (hot-zone gates never
   auto-default).
6. COMMIT - Commit only to the run's dedicated branch (autonomous, reversible);
   push to a shared branch / merge-to-main is always a sign-off gate, never
   autonomous.
7. CLOSE - Propose any session-log / memory-file update for the user's sign-off
   (write it FULL-CONTENT only if the file is auto-formatted / held open by
   another app, see below); write a /handoff primer if the run stopped early;
   then release the claim/lockfile.

Stuck handler (spans phases): repeated gate failure, council deadlock, or agent
death -> call advisor() (and/or a cross-vendor council seat if the user has one),
record the consult in decisions.md, then replan (non-hot-zone) or stop+handoff
(hot-zone or unresolved). Nothing unproven ships.

## Tiered by blast radius (decision table)

When a gate is unmet, or a proposed action is reached, the response is tiered by
blast radius:

| Situation                        | Response                                                                 |
|----------------------------------|--------------------------------------------------------------------------|
| Non-hot-zone unmet gate          | Council authorizes and proceeds. The refute-council / decision-council   |
|                                  | verdict is the authority; append a reversible entry to decisions.md and  |
|                                  | continue. Low blast radius, reversible on the dedicated branch.          |
| Hot zone (any touchpoint below)  | STOP. Do not edit. Write a /handoff primer from the run dir requesting   |
|                                  | sign-off, and wait. Never auto-default a hot-zone gate on timeout.       |

## Hot-zone list (generic, verbatim)

Any touchpoint on the following forces STOP + handoff for sign-off, never an
autonomous edit. If a `.bob-convention.md` file exists in the project root, add
its project-specific hot zones to this list; otherwise this generic list stands
alone:

- secrets / credentials / `.env` files (anything that grants access)
- auth / identity / login code
- database migrations and schema changes
- production deploys and infrastructure-as-code
- package publish / release / version bumps
- any `git push` to a shared branch, force-push, or history rewrite (rebase,
  reset --hard, filter-branch) -- and any merge-to-main

Note: /bob never autonomously touches a hot zone. The only bridge into a hot zone
is a human-gated sign-off after a handoff.

Auto-formatted / held-open files: some memory or note files are held open by an
external app whose auto-formatter CORRUPTS them on incremental edits. When CLOSE
proposes an update to such a file, it (a) surfaces the proposed text for the
user's sign-off, and (b) writes it with a FULL-CONTENT write only (read the whole
file, append in memory, write the whole file) -- never an incremental/edit-block
write. A timeout never auto-writes such a file.

## Dependency-fallback rules

/bob leans on a few optional skills, so it must degrade gracefully and never
hard-fail when one is absent:

- Refute-council / decision-council: prefer a `council` skill IF the user has one
  (blind parallel subagents + optional cross-vendor seat + house verdict format).
  When absent, inline the same pattern via the always-available Agent/Workflow
  tools: spawn 3 blind subagents each briefed to REFUTE "gate met", majority-refute
  = fail. If even subagent spawning is unavailable, fall back to advisor(). Net:
  the council gate works in ANY project.
- Handoff on stop: if a `handoff` skill is present use it; otherwise write a plain
  primer `.md` from the run dir. Safe anywhere.
- Local delegation: a `delegate` MCP / skill (bulk mechanical work on a local
  model) is an optimization. If absent, skip it; it is not a correctness dependency.
- advisor is a tool, always present; it is the last-resort fallback for the council
  gate and the stuck handler.
