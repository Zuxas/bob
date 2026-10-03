import json
import subprocess
import time
from pathlib import Path

import bob_run


def _git(cwd, *args):
    subprocess.run(["git", "-C", str(cwd), *args],
                   capture_output=True, text=True, check=True)


def test_init_creates_run_dir(tmp_path):
    runid = bob_run.init_run(str(tmp_path), "blueprint-07-03.md")
    run = tmp_path / "bob-runs" / runid
    assert run.is_dir()
    for f in ["STATUS.md", "control.md", "decisions.md"]:
        assert (run / f).is_file(), f
    for d in ["agents", "evidence"]:
        assert (run / d).is_dir(), d
    assert runid.startswith("bob-")


def test_claim_then_second_claim_refused(tmp_path):
    doc = tmp_path / "blueprint-07-03.md"
    doc.write_text("x")
    assert bob_run.claim(str(doc), "run-A") is True
    assert bob_run.check_claim(str(doc))["runid"] == "run-A"
    assert bob_run.claim(str(doc), "run-B") is False  # refused: live claim


def test_stale_claim_can_be_reclaimed(tmp_path):
    doc = tmp_path / "d.md"
    doc.write_text("x")
    bob_run.claim(str(doc), "run-A")
    cf = Path(str(doc) + ".bobclaim")
    data = json.loads(cf.read_text())
    data["ts"] = time.time() - 91 * 60
    cf.write_text(json.dumps(data))  # backdate 91 min
    assert bob_run.check_claim(str(doc)) is None  # stale -> invisible
    assert bob_run.claim(str(doc), "run-B") is True  # reclaim allowed


def test_release_only_by_owner(tmp_path):
    doc = tmp_path / "d.md"
    doc.write_text("x")
    bob_run.claim(str(doc), "run-A")
    assert bob_run.release(str(doc), "run-B") is False
    assert bob_run.release(str(doc), "run-A") is True
    assert bob_run.check_claim(str(doc)) is None


def test_read_control_parses_commands(tmp_path):
    run = tmp_path / "r"
    run.mkdir()
    c = run / "control.md"
    c.write_text("# header\n!pause\n!kill agent-03\n"
                 "!redirect agent-02 use the match APL\nnoise\n")
    cmds = bob_run.read_control(str(run))
    assert {"cmd": "pause", "target": None, "note": None} in cmds
    assert {"cmd": "kill", "target": "agent-03", "note": None} in cmds
    assert any(x["cmd"] == "redirect" and x["target"] == "agent-02"
               and x["note"] == "use the match APL" for x in cmds)
    assert len(cmds) == 3


def test_append_decision_is_reversible_and_tagged(tmp_path):
    run = tmp_path / "r"
    run.mkdir()
    (run / "decisions.md").write_text("# decisions\n")
    bob_run.append_decision(
        str(run), what="passed gate 2 for affinity",
        why="refute-council 2/3 could not break it", source="timeout-default",
        reversal="git revert <hash>; reopen gate 2")
    txt = (run / "decisions.md").read_text()
    assert "timeout-default" in txt and "REVERSAL:" in txt and "passed gate 2" in txt


def test_assert_branch_guards_commit_target(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    (repo / "f.txt").write_text("x")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "init")
    _git(repo, "switch", "-q", "-c", "bob/run-A")
    assert bob_run.assert_branch(str(repo), "run-A") is True   # on the run branch
    _git(repo, "switch", "-q", "-c", "other")
    assert bob_run.assert_branch(str(repo), "run-A") is False  # stray checkout -> refuse
    assert bob_run.assert_branch(str(tmp_path / "not-a-repo"), "run-A") is False


def test_classify_input_path_vs_goal(tmp_path):
    doc = tmp_path / "real.md"
    doc.write_text("x")
    assert bob_run.classify_input(str(doc)) == "path"                      # existing file
    assert bob_run.classify_input("add a dark-mode toggle to settings") == "goal"  # free text
    assert bob_run.classify_input(str(tmp_path / "nope.md")) == "goal"     # non-existent path


# --- #1: claims are atomic across processes ----------------------------------

import os
import sys

_SCRIPTS = Path(__file__).resolve().parent
_RACER = r"""
import sys, time
sys.path.insert(0, sys.argv[1])
import bob_run
doc, runid, start = sys.argv[2], sys.argv[3], float(sys.argv[4])
while time.time() < start:      # line every racer up on the same instant
    pass
print("OK" if bob_run.claim(doc, runid) else "REFUSED", flush=True)
"""


def _race(doc, n, tag):
    start = time.time() + 1.5    # leave time for every interpreter to boot
    procs = [subprocess.Popen([sys.executable, "-c", _RACER, str(_SCRIPTS), str(doc),
                               f"{tag}-{i}", repr(start)],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
             for i in range(n)]
    outs = [p.communicate(timeout=60) for p in procs]
    for (out, err), p in zip(outs, procs):
        assert p.returncode == 0, err
    return [o.strip() for o, _ in outs]


def test_concurrent_claims_exactly_one_wins(tmp_path):
    doc = tmp_path / "d.md"
    doc.write_text("x")
    for rnd in range(5):
        results = _race(doc, 8, f"r{rnd}")
        assert results.count("OK") == 1, results
        holder = bob_run.check_claim(str(doc))
        assert holder["runid"].startswith(f"r{rnd}-")
        assert bob_run.release(str(doc), holder["runid"]) is True


def test_concurrent_reclaim_of_stale_claim_exactly_one_wins(tmp_path):
    doc = tmp_path / "d.md"
    doc.write_text("x")
    cf = Path(str(doc) + ".bobclaim")
    for rnd in range(5):
        cf.write_text(json.dumps({"runid": "dead", "pid": 0, "ts": time.time() - 91 * 60}))
        results = _race(doc, 8, f"s{rnd}")
        assert results.count("OK") == 1, results
        assert bob_run.check_claim(str(doc))["runid"].startswith(f"s{rnd}-")


def test_refused_claimant_learns_the_live_holder(tmp_path):
    doc = tmp_path / "d.md"
    doc.write_text("x")
    assert bob_run.try_claim(str(doc), "run-A") == (True, bob_run.check_claim(str(doc)))
    ok, holder = bob_run.try_claim(str(doc), "run-B")
    assert ok is False and holder["runid"] == "run-A"


def test_cli_refusal_names_the_holder(tmp_path):
    doc = tmp_path / "d.md"
    doc.write_text("x")
    bob_run.claim(str(doc), "run-A")
    out = subprocess.run([sys.executable, str(_SCRIPTS / "bob_run.py"), "claim",
                          "--doc", str(doc), "--runid", "run-B"],
                         capture_output=True, text=True, check=True).stdout.strip()
    assert out.split(" ", 1)[0] == "REFUSED"
    assert json.loads(out.split(" ", 1)[1])["runid"] == "run-A"


def test_old_owner_cannot_release_the_reclaimed_claim(tmp_path):
    doc = tmp_path / "d.md"
    doc.write_text("x")
    bob_run.claim(str(doc), "run-A")
    cf = Path(str(doc) + ".bobclaim")
    data = json.loads(cf.read_text())
    data["ts"] = time.time() - 91 * 60
    cf.write_text(json.dumps(data))                  # A's claim goes stale
    assert bob_run.claim(str(doc), "run-B") is True  # B reclaims it
    assert bob_run.release(str(doc), "run-A") is False
    assert bob_run.check_claim(str(doc))["runid"] == "run-B"


def test_lock_is_released_when_the_holder_dies(tmp_path):
    lock = tmp_path / "x.lock"
    holder = subprocess.Popen(
        [sys.executable, "-c",
         "import sys,time; sys.path.insert(0, sys.argv[1]); import bob_run\n"
         "with bob_run.file_lock(sys.argv[2]):\n print('held', flush=True); time.sleep(60)",
         str(_SCRIPTS), str(lock)], stdout=subprocess.PIPE, text=True)
    assert holder.stdout.readline().strip() == "held"
    try:
        with bob_run.file_lock(lock, timeout_s=0.3):
            raise AssertionError("acquired a lock another process holds")
    except TimeoutError:
        pass
    holder.kill()
    holder.wait()
    with bob_run.file_lock(lock, timeout_s=5):      # the dead holder left nothing behind
        pass


def test_atomic_write_text_replaces_whole_file(tmp_path):
    p = tmp_path / "f.json"
    bob_run.atomic_write_text(p, "old")
    bob_run.atomic_write_text(p, "new")
    assert p.read_text(encoding="utf-8") == "new"
    assert [f.name for f in tmp_path.iterdir()] == ["f.json"]   # no temp files left
