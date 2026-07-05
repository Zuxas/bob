---
name: bob
description: Autonomous hybrid-conductor orchestrator. Use ONLY when the user types "/bob" or says "use bob to ...". Two input modes, one entry point -- either point it at a pre-existing tasking doc (`/bob <path>`: a spec, a handoff/primer, or a loose .md) OR give it a free-text goal in quotes (`/bob "add a dark-mode toggle to the settings page"`) and it DRAFTS the definition-of-done itself. Either way it drives the work to a PROVEN-done state (evidence + adversarial refute-council) OR an honest, documented stop with a handoff explaining why -- never "looks done." Runs a conductor in the main loop and fans out 4-20 agents via Workflow for the heavy execute/verify phases. It is a conductor, not a correctness guarantee.
disable-model-invocation: true
---

# /bob -- hybrid-conductor orchestrator

Announce: "Using /bob to drive <doc>: conductor in the main loop, Workflow for fan-out, proven-done-or-honest-stop."

## Before acting

1. Read `references/spine.md` (the 7-phase spine, tiered-by-blast-radius decision table, hot-zone list) and `references/timeout-gate.md` (the human-gate-with-timeout-default procedure). Do NOT act until both are read.
2. Compute `SKILL_DIR` = the directory that contains this file. Call the deterministic helper for ALL claim / run-dir / control / decision mechanics -- never hand-roll them:
   `python "<SKILL_DIR>/scripts/bob_run.py" <cmd> ...`
   Verbs: `init --base <dir> --doc <path>` | `claim --doc <path> --runid <id>` | `check-claim --doc <path>` | `release --doc <path> --runid <id>` | `control --run <run_dir>` | `decision --run <run_dir> --what .. --why .. --source .. --reversal ..`
3. If a `.bob-convention.md` file exists in the project root, read it for project-specific hot zones + PII redaction; otherwise use the generic hot zones in `references/spine.md`. Never fail because a project convention file is missing.

The honest framing, load-bearing, do not soften: `/bob` converts "will the result be up to standard?" into "it is PROVEN up to standard, or it STOPPED and told you why."

Follow the 7 phases IN ORDER. Never skip PLAN+CLAIM. Never write before the user confirms.

---

## 1. INTAKE (read-only -- ZERO writes)

- FIRST classify the argument: `python "<SKILL_DIR>/scripts/bob_run.py" classify-input --arg "<arg>"`.
  - `path` -> DOC MODE. Read the pointed-at doc plus the repo context it references (NO writes), and classify it: (a) spec-with-gates -> adopt its gates verbatim; (b) handoff/primer -> tighten into a checkable definition-of-done; (c) loose `.md` -> derive gates from its intent.
  - `goal` -> GOAL MODE (free text, e.g. `/bob "add a dark-mode toggle"`). YOU draft the definition-of-done: restate the goal, enumerate falsifiable acceptance gates, and identify the independent sub-units + the affected git subproject. This is the `/goal` capture step -- the sentence becomes the spec.
- If deriving/drafting gates needs a REAL decision, or scope is ambiguous, invoke the `brainstorming` skill first; for a contested/irreversible call, run the `council` skill IF the user has one (else the inlined refute-panel -- see Dependency fallbacks) BEFORE proceeding. Free-text goals are looser than docs, so lean on this more readily -- but a genuinely clear goal does NOT need a brainstorm.
- Emit a PLAN: goal restatement, derived gates, the independent sub-units, the agent count (auto-scaled to sub-units, capped at 20), the affected git subproject, and every hot-zone touchpoint flagged up front. In GOAL MODE, also WRITE the drafted definition-of-done to `bob-runs/<runid>/goal-spec.md` at PLAN+CLAIM time (after confirm) so intent is legible and auditable -- never fan out on an unwritten goal.

## 2. PLAN+CLAIM (gate before any write)

- Present the PLAN to the user. Make NO writes until the user confirms.
- GOAL MODE "goes for it" veto window: after presenting the PLAN, ask Go / Adjust / Stop via `AskUserQuestion`. For a NON-hot-zone, unambiguous goal, a no-response within the veto window DEFAULTS to Go (reuse the `references/timeout-gate.md` wait + log a reversible decision) -- this is the low-friction "just go" the user wants. But a HOT-ZONE touchpoint or an ambiguous goal NEVER auto-Goes: it holds for an explicit answer. The user may set the veto window to 0 for pure autonomy on non-hot-zone goals (still never on hot zones).
- Run `bob_run.py check-claim --doc <doc>`. If it returns a live (non-null) claim, REFUSE: name the holding runid + timestamp, tell the user, and STOP. Do not proceed.
- On user confirm ONLY:
  - `bob_run.py init --base <run-base> --doc <doc>` -> capture the `<runid>` and run dir `bob-runs/<runid>/` (STATUS.md, control.md, decisions.md, agents/, evidence/). `<run-base>` MUST be a disposable scratchpad dir OUTSIDE the git subproject tree (so `bob-runs/` never muddies branch isolation and stays a clean handoff source).
  - `bob_run.py claim --doc <doc> --runid <runid>` -> expect `OK`.
  - Cut a dedicated branch in the affected git subproject: `git -C <subproject> switch -c bob/<runid>`. Never branch a non-git parent dir; never touch the subproject's main/shared branch.

## 3. FAN-OUT (delegate to Workflow, in bounded waves)

- Conductor writes a `Workflow` script for a wave of independent sub-units. Each agent prompt MUST include:
  (i) append a one-line worklog to `agents/agent-NN.md` BEFORE each read/write;
  (ii) `Read control.md` at every checkpoint and honor `!pause` / `!kill agent-NN` / `!redirect` / `!stop`;
  (iii) produce a CONCRETE evidence artifact into `evidence/` for its gate.
- At each wave boundary, the conductor re-reads control via `bob_run.py control --run <run_dir>`, honors any intervention, updates `STATUS.md`, then launches the next wave. Interventions land at checkpoints/wave boundaries, not mid-token -- instruct agents on long tasks to checkpoint frequently.
- If a wave dies mid-flight, recover from the agent worklogs/journal, surface the partial, and DECIDE -- never silently continue.

## 4. VERIFY (evidence floor -> adaptive verifier -> blind refute-council)

- Evidence floor FIRST (existence AND substance): a gate CANNOT pass unless `evidence/` holds an artifact that was produced by an INDEPENDENT verifier re-running the check (test output, benchmark numbers, a build/run log) -- NOT the self-report of the agent that did the work. A missing OR hollow/fabricated artifact -> gate fails -> STOP + handoff. No exceptions. (The executor and the verifier must be different agents.)
- Adaptive verifier by task type: code -> the `verify` skill / tests / lint / run; data/analysis -> re-derived numbers; docs -> a read/review. The verifier writes the artifact; it does not trust a claim of success.
- Blind refute-council: spawn 2-3 blind agents each briefed to REFUTE "gate met" AND "the evidence is real and maps to this gate." Majority-refute = FAIL. Prefer the `council` skill IF the user has one; else run the inlined refute-panel; else `advisor()` (see Dependency fallbacks).

## 5. GATE (human, with timeout-default -- follow `references/timeout-gate.md` verbatim)

- Present artifacts + the refute-council verdict to the user via `AskUserQuestion`.
- Timeout path: bound the wait per `references/timeout-gate.md`. On no-response, only auto-proceed if the refute-council POSITIVELY confirmed the gate (verdict PASS with real, independent evidence) -- a mere "not refuted" or a hollow-evidence pass does NOT auto-proceed; that STOPS for the human. When it does auto-proceed, log a reversible decision:
  `bob_run.py decision --run <run_dir> --source timeout-default --what "gate <id> -> <V>" --why "<council rationale>" --reversal "<how to reopen>"`.
- TIERED by blast radius:
  - NON-hot-zone unmet gate -> the council authorizes and the run proceeds (logged).
  - HOT ZONE (see the hot-zone list in `references/spine.md`, or the project's `.bob-convention.md`) -> NEVER auto-default. STOP + write a handoff + request sign-off.

## 6. COMMIT (branch-only, autonomous)

- Guard FIRST, every time: `python "<SKILL_DIR>/scripts/bob_run.py" assert-branch --subproject <subproject> --runid <runid>`. If it exits non-zero (you are NOT on `bob/<runid>` -- a stray checkout, a failed branch cut, or a misidentified subproject), do NOT commit: STOP, surface it, re-establish the branch or hand off. This is a deterministic guard, not a judgement call.
- Then commit ONLY to the `bob/<runid>` branch, always with `git -C <subproject>` (reversible, low blast radius -- this is the user's "commit progress").
- `git push` to a shared branch, force-push, history rewrite, or merge-to-main -> sign-off gate. NEVER autonomous.

## 7. CLOSE

- Propose any session-log / memory-file update text for the user's CLOSE sign-off. If the target file is one the environment auto-formats or holds open (e.g. a note-taking app that corrupts incremental edits), write it FULL-CONTENT only (read whole file -> append in memory -> write whole file); never an edit-block/incremental write, never on a timeout.
- If the run stopped early: write a `/handoff` primer sourced from the run dir so the next session can resume from a clean, evidence-backed state.
- Release the claim: `bob_run.py release --doc <doc> --runid <runid>`.

## Stuck handler

Repeated gate failure, council deadlock, or agent death -> call `advisor()` (and/or a cross-vendor council seat if the user has one), record the consult via `bob_run.py decision`, then replan (non-hot-zone) or STOP + handoff (hot-zone / unresolved). Nothing unproven ships.

## Dependency fallbacks

`advisor` is a tool (always present); `council` and other skills may or may not be installed. Degrade gracefully -- never hard-fail because an optional skill is absent.

- Refute/decision council: prefer a `council` skill IF the user has one (blind parallel subagents + optional cross-vendor seat + chairman synthesis). When absent, INLINE the blind-refute panel via the always-available `Agent`/`Workflow` tools (2-3 blind agents briefed to break "gate met"; majority-refute = FAIL). If even subagent spawning is unavailable, fall back to `advisor()`. The council-gate works in ANY project.
- Handoff on stop: if a `handoff` skill is present, use it; otherwise write a plain primer `.md` sourced from the run dir. Safe to do anywhere.
- Local delegation: if a `delegate` MCP / skill is present it is an optimization for bulk mechanical work; if absent, skip it. It is never a correctness dependency.

## Use your full arsenal (stand on your own; wield whatever is present)

You are an orchestrator, not a soloist. At INTAKE and before every sub-unit, survey the skills actually available to you (the Skill tool menu -- both global and the project's `.claude/skills`) and USE any that fit the work, not only the ones named elsewhere here:
- test-first unit -> a `tdd` skill; bug hunt -> `diagnosing-bugs` / `systematic-debugging`.
- pre-commit correctness/quality -> `code-review` / `verify`; design spike -> `prototype`.
- design-before-build or an ambiguous goal -> `brainstorming` (+ `grilling` to stress it); contested/irreversible call -> a `council` skill; ejecting scope to a fresh session -> a `handoff` skill.

Prefer a purpose-built skill over doing the work raw; the more skills you have, the more you leverage. When a skill materially shaped a sub-unit, name it in that unit's decision-log entry.

STAND ON YOUR OWN. You HARD-depend on none of these -- every essential pattern is built into you and runs on Claude Code's built-in tools alone:
- the refute-council is a pattern you run yourself (blind `Agent` / `Workflow` agents briefed to break "gate met"; majority-refute = fail);
- the stop-handoff is a document you write yourself (its sections live in `references/spine.md`);
- clarifying an ambiguous goal is questions you ask the user yourself.

External skills are UPGRADES, never REQUIREMENTS. Out of the box, with only Claude Code's built-in tools, Bob works.
