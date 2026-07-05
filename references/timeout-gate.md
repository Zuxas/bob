# Timeout-default human gate (conductor procedure)

This is the exact procedure the GATE phase runs when a gate needs human sign-off
but the human may not answer in time. It is the highest-risk mechanism in /bob.
Follow it verbatim.

1. Run the refute-council on "gate <id> is met". Capture the verdict V (PASS/FAIL)
   plus the evidence paths the council leaned on (artifacts under evidence/).
   AUTO-PROCEED IS ONLY AVAILABLE WHEN V IS A POSITIVE PASS backed by real,
   independent evidence. If the council merely "did not refute", or the evidence is
   hollow/self-reported, the gate does NOT auto-proceed on timeout -- it holds for
   the human.

2. Present V + evidence to the user via AskUserQuestion. Options: Accept / Reject / Hold.

3. Start a bounded wait. NOTE: the wait runs in the CONDUCTOR (main loop), which has
   the ScheduleWakeup tool -- subagents do NOT, so this step never lives inside a
   Workflow. Use ScheduleWakeup(delaySeconds=1200, reason="bob gate <id> timeout");
   if ScheduleWakeup is unavailable in the current surface, fall back to a Monitor
   poll, or (last resort) re-prompt once and treat a second no-response as the
   timeout. This mechanism is PROVE-FIRST -- validate it in isolation before
   trusting it.
   - If the user answers first, honor the answer and cancel the fallback wakeup.
   - If the wait elapses with no answer AND V is a positive evidence-backed PASS:
     DEFAULT to V, then call
     python "$SKILL_DIR/scripts/bob_run.py" decision --source timeout-default \
       --what "gate <id> -> <V>" \
       --why "<council rationale + evidence paths>" \
       --reversal "<how to reopen>"

4. Never default a HOT-ZONE gate. If the gate touches a hot zone (see the hot-zone
   list in spine.md, or the project's .bob-convention.md -- e.g. secrets/.env, auth,
   DB migrations/schema, production deploys/infra, package publish/release, or any
   git push to a shared branch / force-push / history rewrite / merge-to-main), a
   timeout means STOP + write a handoff for sign-off, NOT default-proceed. Only
   non-hot-zone gates auto-default to the council verdict.
