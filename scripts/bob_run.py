"""bob_run.py -- deterministic helper for the /bob orchestrator skill.

Stdlib-only (global-safe). Owns the mechanics that must be exact rather than
prose-Claude-follows-vibes: run-dir scaffold, atomic claim/lockfile with
staleness, control-channel parsing, and the reversible decision log.

CLI: python bob_run.py <init|claim|check-claim|release|control|decision> ...
"""
import os
import json
import time
import argparse
import subprocess
from pathlib import Path


def _now():
    return time.strftime("%Y%m%d-%H%M%S")


# --- run directory -----------------------------------------------------------

def init_run(base_dir, doc_path):
    rid = f"bob-{_now()}-{os.urandom(2).hex()}"
    run = Path(base_dir) / "bob-runs" / rid
    (run / "agents").mkdir(parents=True)
    (run / "evidence").mkdir()
    (run / "STATUS.md").write_text(
        f"# BOB RUN {rid}\ndoc: {doc_path}\nphase: INIT\n", encoding="utf-8")
    (run / "control.md").write_text(
        "# control channel - write commands below, one per line, prefixed with !\n"
        "# e.g. !pause   !kill agent-03   !redirect agent-02 use the match APL   !stop\n",
        encoding="utf-8")
    (run / "decisions.md").write_text(
        "# decisions log (reversible)\n", encoding="utf-8")
    return rid


# --- claim / lockfile --------------------------------------------------------

def _claim_path(doc_path):
    return Path(str(doc_path) + ".bobclaim")


def check_claim(doc_path, ttl_min=90):
    """Return the LIVE claim dict, or None if absent/unreadable/stale."""
    cf = _claim_path(doc_path)
    if not cf.exists():
        return None
    try:
        data = json.loads(cf.read_text(encoding="utf-8"))
    except Exception:
        return None
    if time.time() - float(data.get("ts", 0)) > ttl_min * 60:
        return None  # stale -> invisible, may be reclaimed
    return data


def claim(doc_path, runid, ttl_min=90):
    """Claim the doc iff no LIVE claim exists. Returns True on success."""
    if check_claim(doc_path, ttl_min) is not None:
        return False
    _claim_path(doc_path).write_text(
        json.dumps({"runid": runid, "pid": os.getpid(), "ts": time.time()}),
        encoding="utf-8")
    return True


def release(doc_path, runid):
    """Release the claim iff it belongs to runid (ignoring staleness)."""
    data = check_claim(doc_path, ttl_min=10 ** 9)
    if not data or data.get("runid") != runid:
        return False
    _claim_path(doc_path).unlink(missing_ok=True)
    return True


# --- control channel + decision log -----------------------------------------

_CTRL = {"pause", "resume", "kill", "redirect", "rescope", "stop"}


def read_control(run_dir):
    """Parse control.md lines of form '!<cmd> <target?> <note?>'."""
    out = []
    for ln in (Path(run_dir) / "control.md").read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln.startswith("!"):
            continue
        parts = ln[1:].split(maxsplit=2)
        if not parts or parts[0] not in _CTRL:
            continue
        out.append({
            "cmd": parts[0],
            "target": parts[1] if len(parts) > 1 else None,
            "note": parts[2] if len(parts) > 2 else None,
        })
    return out


def append_decision(run_dir, what, why, source, reversal):
    """Append a structured, timestamped, reversible decision entry."""
    entry = (f"\n## {time.strftime('%Y-%m-%d %H:%M:%S')} [{source}]\n"
             f"- WHAT: {what}\n- WHY: {why}\n- REVERSAL: {reversal}\n")
    with open(Path(run_dir) / "decisions.md", "a", encoding="utf-8") as fh:
        fh.write(entry)


# --- branch guard (G3) -------------------------------------------------------

def current_branch(subproject):
    """Return the current git branch of subproject, or None on any failure."""
    try:
        out = subprocess.run(
            ["git", "-C", str(subproject), "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, timeout=15)
        return out.stdout.strip() if out.returncode == 0 else None
    except Exception:
        return None


def assert_branch(subproject, runid):
    """True iff subproject is currently on the run's dedicated bob/<runid> branch.

    The COMMIT phase MUST call this immediately before every commit so a stray
    checkout by a subagent/tool can never land a commit on main. Deterministic;
    do not replace with prose judgement.
    """
    return current_branch(subproject) == f"bob/{runid}"


# --- input mode (path vs free-text goal) -------------------------------------

def classify_input(arg):
    """Return 'path' if arg is an existing file (doc mode), else 'goal' (free-text).

    Lets `/bob <path>` and `/bob "describe what I want"` share one entry point:
    doc mode READS the definition-of-done; goal mode DRAFTS it in INTAKE.
    """
    try:
        return "path" if Path(str(arg)).is_file() else "goal"
    except Exception:
        return "goal"


# --- CLI ---------------------------------------------------------------------

def _main():
    p = argparse.ArgumentParser(prog="bob_run")
    sub = p.add_subparsers(dest="cmd", required=True)

    i = sub.add_parser("init")
    i.add_argument("--base", required=True)
    i.add_argument("--doc", required=True)

    c = sub.add_parser("claim")
    c.add_argument("--doc", required=True)
    c.add_argument("--runid", required=True)

    cc = sub.add_parser("check-claim")
    cc.add_argument("--doc", required=True)

    r = sub.add_parser("release")
    r.add_argument("--doc", required=True)
    r.add_argument("--runid", required=True)

    ct = sub.add_parser("control")
    ct.add_argument("--run", required=True)

    d = sub.add_parser("decision")
    d.add_argument("--run", required=True)
    d.add_argument("--what", required=True)
    d.add_argument("--why", required=True)
    d.add_argument("--source", required=True)
    d.add_argument("--reversal", required=True)

    ab = sub.add_parser("assert-branch")
    ab.add_argument("--subproject", required=True)
    ab.add_argument("--runid", required=True)

    ci = sub.add_parser("classify-input")
    ci.add_argument("--arg", required=True)

    a = p.parse_args()
    if a.cmd == "init":
        print(init_run(a.base, a.doc))
    elif a.cmd == "claim":
        print("OK" if claim(a.doc, a.runid) else "REFUSED")
    elif a.cmd == "check-claim":
        print(json.dumps(check_claim(a.doc)))
    elif a.cmd == "release":
        print("OK" if release(a.doc, a.runid) else "REFUSED")
    elif a.cmd == "control":
        print(json.dumps(read_control(a.run)))
    elif a.cmd == "decision":
        append_decision(a.run, a.what, a.why, a.source, a.reversal)
        print("OK")
    elif a.cmd == "assert-branch":
        ok = assert_branch(a.subproject, a.runid)
        print("OK" if ok else f"FAIL on {current_branch(a.subproject)}")
        raise SystemExit(0 if ok else 1)
    elif a.cmd == "classify-input":
        print(classify_input(a.arg))


if __name__ == "__main__":
    _main()
