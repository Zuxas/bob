---
name: handoff
description: Write a scoped handoff doc that captures ONE workload with enough context for a fresh agent (or Bob) to pick it up cold. Use ONLY when the user types "/handoff" or asks to hand off / eject / spec a slice of work for another session or tool. disable-model-invocation.
disable-model-invocation: true
---

# /handoff -- eject a scoped workload to a fresh agent

Write ONE self-contained markdown doc that a cold reader -- a new session, another
tool (a different model or CLI), or the Bob skill -- can pick up without any of
your current context.

## When to use

- Ejecting a slice of out-of-scope work mid-session so it does not pollute the
  current thread (and so this session sharpens back onto its own task).
- Specing a workload for another agent to execute later -- then point Bob at it.
- Cross-tool relay: hand a slice to a different model/CLI as plain markdown, the
  cleanest carrier between agents.

## What to write

Save to a disposable location (a scratch / handoffs directory -- not committed).
Use this structure:

```markdown
# Handoff: <one-line purpose>

- **Goal:** what "done" means, in a sentence or two.
- **Scope:** what is in; what is explicitly out.
- **Current state:** what exists now -- branch, commits, what works, what does not.
- **Artifacts (by path -- do NOT restate):** the files, specs, data, and URLs the
  receiver needs. Reference them; never paste their contents.
- **Next steps:** the ordered, concrete moves to take.
- **Gotchas / hot zones:** what will bite the receiver; anything irreversible to
  avoid without sign-off.
- **Suggested skills:** which skills the next session should invoke first (list
  only skills that exist; never invent one).
```

## Rules

- POINT at artifacts by path; never duplicate their content into the handoff.
- REDACT secrets and any private PII before writing -- this doc may be pasted
  elsewhere or into a committed artifact.
- Keep it scoped: ONE workload, not a brain-dump. A good handoff is short and
  complete, not long and vague.

## Pairs with Bob

A handoff doc IS a valid Bob input. Write one, then hand it straight to the
foreman:

```text
/bob path/to/your-handoff.md
```

Any agent can write the handoff; Bob (or a fresh session) reads it and drives the
work to proven-done or an honest stop.
