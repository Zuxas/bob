# .bob-convention.md -- your project's site rules for Bob
#
# Copy this file to `.bob-convention.md` in your project root and
# fill in the blanks. Bob reads it before starting work. Anything you
# leave blank falls back to Bob's careful defaults (ask before
# anything irreversible, keep scratch work in bob-runs/, redact
# obvious secrets). The more you tell him here, the less he has to
# guess.
#
# Lines starting with # are comments/instructions to you and can be
# deleted once you've filled things in. ASCII-only, please.

## Hot zones -- ask before touching
#
# List the files, folders, or systems where Bob must STOP and ask for
# a yes before changing anything. These are the expensive-to-get-wrong
# places. Be specific: a path, a glob, or a named system is better
# than a vague description.
#
# Common examples to consider:
#   - authentication / login code
#   - database schemas and migrations
#   - anything touching secrets, keys, or credentials
#   - production deploy scripts or config
#   - payment / billing code
#   - public API contracts other people depend on
#
# Fill in yours:
#   - <path/or/system>   # why it's a hot zone (blast radius)
#   - <path/or/system>   # why it's a hot zone (blast radius)


## Redaction rules -- keep this out of notes and outputs
#
# Tell Bob what must never appear in his working notes, logs, or any
# file he writes. He'll scrub these from everything.
#
# Consider:
#   - personal names / usernames:  <list them>
#   - internal project or codenames: <list them>
#   - secrets, tokens, API keys:    never write these, ever
#   - internal hostnames / paths:   <patterns to avoid>
#   - anything else private:        <describe>
#
# Fill in yours:
#   - <thing to redact>
#   - <thing to redact>


## Where scratch work lives
#
# Bob keeps his working notes and run outputs in one folder so they
# never clutter your real code. Default is bob-runs/. Change it here
# if you want it elsewhere (and remember to gitignore it).
#
#   runs_dir: bob-runs/


## Preferred tools and skills
#
# If you have scripts, commands, or skills you'd rather Bob use for
# certain kinds of work, point him at them here and he'll favor them
# over improvising his own approach.
#
# Examples:
#   - for tests:        <how you run tests>
#   - for linting:      <your linter / command>
#   - for formatting:   <your formatter>
#   - for builds:       <your build command>
#   - preferred skills: <names of skills to reach for first>
#
# Fill in yours:
#   - <task>: <tool/skill/command to prefer>
#   - <task>: <tool/skill/command to prefer>


## Anything else Bob should know
#
# Free space. House style, things that have bitten people before,
# conventions you care about. Say it here and Bob will honor it.
#
#   - <note>
