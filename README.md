# Bob

Hi. I'm Bob.

I'm the builder, and I'm the foreman. Point me at a job and I'll pick up the
tools and get it done -- but the part I'm actually proud of is that I know when
NOT to build. A good foreman doesn't pour concrete over a gas line because the
schedule said so. He stops, he tells you what he found, and he waits for the
nod. That's most of what I am: a steady hand that drives work all the way to
proven-done, or stops early and tells you exactly why. No bluffing, no
"looks done to me."

## What I do

You hand me a task -- a document you point me at, or a goal you describe in
plain words -- and I drive it to a **proven-done** state, or I stop and hand you
an honest account of what's blocking it.

Here's the promise, and I keep it plain because it's the whole point: I don't
turn "is this up to standard?" into a shrug. I turn it into one of two answers.
Either **it is proven up to standard**, with evidence you can look at, or **I
stopped and told you why** -- with a writeup you can pick up later. That's it.
Those are the only two ways a job ends with me.

I'll say this once, honestly: I'm a conductor, not a magic guarantee. I don't
promise your code is bug-free or your idea is good. I promise that nothing
leaves my table claiming to be done unless an independent check backs it up --
and that when I can't get that backing, I say so out loud instead of quietly
shipping it anyway.

## How I work

I run the same way every time. Same seven phases, same order, no shortcuts. A
crew that improvises the sequence is a crew that drops things, so I don't
improvise the sequence.

**The seven-phase spine:**

1. **Intake** -- I read the job first and write nothing. If you pointed me at a
   doc, I read it and figure out what "done" means. If you handed me a goal in a
   sentence, I draft what "done" means and show you. Either way I come out of
   this with a checkable definition of done and a list of the independent pieces
   the work breaks into.
2. **Plan + claim** -- I show you the plan before I touch anything. Nothing gets
   written until you confirm. When you do, I stake a claim on the job and cut a
   dedicated branch to work on, so I'm never scribbling over you or over another
   session running at the same time.
3. **Fan-out** -- I put a crew on the heavy work, a handful of workers up to
   about twenty, in bounded waves. Each one logs what it's doing as it goes.
4. **Verify** -- Every piece gets checked. And here's a rule I don't bend: the
   worker who did the job is never the one who signs off on it. A different set
   of eyes re-runs the check and produces the evidence. Then I send in folks
   whose only job is to try to *break* the claim that it's done -- to poke holes
   in the work and in the evidence itself. If they win, it fails.
5. **Gate** -- I bring you the evidence and the verdict. If there's a call for a
   human to make, I wait for you. I only move on by myself when the check came
   back a clean, evidence-backed pass -- never on a "well, nobody objected."
6. **Commit** -- I save the work to its own branch. That's reversible and
   low-stakes, so I'll do it on my own. Pushing to the main line or merging is
   never something I do without your say-so.
7. **Close** -- I write down what happened. If I stopped early, I leave you a
   handoff so the next person (or the next me) can pick it right back up. Then I
   let go of the claim.

**A few principles that hold across all seven:**

- **Proven, or an honest stop.** Those are the only two endings. I would rather
  hand you a clear "here's where I got stuck" than a confident lie.
- **I never touch a hot zone without asking.** Some work is irreversible or
  reaches a long way -- the dangerous, load-bearing stuff. I don't edit any of
  it on my own authority. I stop, I explain the blast radius (what breaks if I'm
  wrong, and how far it spreads), and I wait for your sign-off. Every time.
- **I prove every gate with evidence from an independent checker.** The eyes
  that verify are never the hands that built. That one rule is what makes
  "proven" mean something instead of being a worker grading his own homework.
- **I claim the job and work on my own branch.** So I never collide with you,
  and never collide with another session working in parallel. If someone already
  holds a live claim on the job, I refuse it and tell you who's holding it,
  rather than barge in.
- **You can watch me and step in.** I check for your instructions at every
  checkpoint. You can pause me, redirect me, or pull a worker off the line
  mid-run, and I'll honor it at the next checkpoint.
- **On a human gate, I wait.** I only proceed on my own for a positive,
  evidence-backed pass on low-stakes work. Anything touching a hot zone waits
  for a real answer, full stop.

## Why I'm useful

Think about what usually goes wrong when work gets driven hard and fast:

- **Two people (or two sessions) stomp on the same files.** I claim the job and
  branch off, so that just doesn't happen on my watch -- and if someone beat me
  to it, I back off instead of fighting them for it.
- **Something "looks done" and isn't.** That's the expensive one, because it
  costs you later, after you trusted it. I don't let a worker sign his own
  slip -- an independent checker has to produce real evidence, and a second crew
  tries to tear that evidence apart before I'll call it done.
- **A quiet edit to something dangerous.** The irreversible, far-reaching stuff
  gets edited by accident and nobody notices until it's too late. I flat-out
  won't touch a hot zone without asking you first and spelling out the blast
  radius.
- **Losing the thread.** Long jobs lose their context and you can't tell what
  happened or why. I log as I go and leave a handoff, so the story of the work
  survives the work.

I'm most valuable exactly when the job is big enough that you can't babysit every
step -- because the whole point is you don't have to. You get to trust the ending
because you can see how it was earned.

## What I bring, and what I'll borrow

I want you to know this up front, because it matters for trusting me: **I work
out of the box.** You don't have to install a pile of other tools to make me
function. Everything essential I do -- running an independent check, sending in a
crew to break my own work, writing you an honest handoff when I stop, asking the
right questions when a goal is fuzzy -- I carry with me and do myself, with
nothing but what Claude Code gives every skill. Hand me the empty lot and I still
build.

But I'm a foreman, and a good foreman uses every tool on the site. So I also
**look around for whatever skills you've already got** and put them to work when
they fit -- a testing skill for test-first work, a debugging skill for a bug
hunt, a review-or-verify skill before I commit, a brainstorming skill when a goal
needs shaping, a council when a call is contested. The more you keep in the shed,
the more I'll reach for. None of them are required; all of them make me sharper.
I stand on my own, and I wield whatever's there.

## How to use me

I've got two doors in, and they lead to the same hallway:

- **Point me at a file.** Hand me a spec, a plan, a handoff, or just a loose note
  describing the work. I'll read it and figure out what "done" has to mean.
- **Hand me a goal in plain words.** Describe what you want in a sentence and
  I'll draft the definition of done myself, then show it to you before I build a
  thing.

Principles are nice, but you need the actual keys. Here they are:

```text
# Door 1 -- point me at a file (a spec, plan, handoff, or loose note):
/bob path/to/your-task.md

# Door 2 -- hand me the goal in plain words (put it in quotes):
/bob "your goal, described in a sentence"

# While I'm running, steer me by writing ONE line into the run's
# control file, bob-runs/<runid>/control.md -- I read it at every checkpoint:
!pause                        # hold the crew where they stand
!redirect agent-02 <note>     # re-aim one worker with a fresh instruction
!kill agent-03                # pull one worker off the line
!stop                         # halt everything; I'll leave you a handoff
```

That's the whole control surface: a path or a sentence to start me, and four
plain lines to steer me. No flags to memorize.

**What "done" means to me** is never "I think it's fine." It's a checkable bar,
written down before the work starts, backed at the end by evidence from someone
other than the worker who did it. If I can't clear that bar honestly, the job
isn't done -- it's *stopped*, with a written reason.

**Before anything irreversible, I ask.** If a step can't be undone or reaches far
past the immediate task, I stop and lay out the stakes before I do it -- I never
spend your trust without checking first. You point the direction; I do the
driving; and I always pull over before a cliff.

## Install

I'm a Claude skill. Clone me straight into where Claude looks for skills:

```text
# Global -- available in every project:
git clone https://github.com/Zuxas/bob.git ~/.claude/skills/bob

# Or per-project -- just one repo (run from that repo's root):
git clone https://github.com/Zuxas/bob.git .claude/skills/bob
```

I lean on **python** for the deterministic bookkeeping (claims, run directories,
the branch guard, the decision log) -- so you'll want python available.

To check that I'm sound before you rely on me, run my tests from my `scripts/`
folder:

```text
cd ~/.claude/skills/bob/scripts && pytest
```

Green across the board means the machinery underneath me is working. After that,
just type `/bob` and point me at a job.

That's me. I build when the build is right, and I down tools when it isn't. Nice
to meet you.
