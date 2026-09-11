"""Post-run verification only; never loads model weights or launches training.

Reconstructs metrics without using study11.metrics/analyze/direction. The audit was
written after outcomes existed and is not additional preregistered evidence.
"""
from __future__ import annotations

import hashlib
import json
import math
import statistics as st
import subprocess
import sys
from collections import defaultdict
from importlib.metadata import version
from pathlib import Path

import numpy as np
from transformers import AutoTokenizer

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
SEEDS = (6, 7, 8)
ARMS = ("spaced", "variable_gaps")
CHECKPOINTS = [50, 100, 200, 400, 800, 1200, 1500]


def sha(path):
    with Path(path).open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def git_bytes(commit, path):
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT)


def close(a, b):
    assert math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-10), (a, b)


def finite(obj):
    if isinstance(obj, float):
        assert math.isfinite(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            finite(v)
    elif isinstance(obj, list):
        for v in obj:
            finite(v)


def describe(values):
    return dict(values=list(values), mean=st.mean(values), sample_sd=st.stdev(values),
                min=min(values), max=max(values))


def metrics(x):
    es = [e for e in x["evals"] if e["phase"] == "interference"]
    assert [e["int_step"] for e in es] == CHECKPOINTS
    assert [e["step"] for e in es] == [800 + t for t in CHECKPOINTS]
    imm = next(e for e in x["evals"] if e["phase"] == "immediate")
    assert imm["step"] == 800
    g, steps = x["guards"], x["step_guards"]
    first = [min(int(t) for t, ids in x["target_schedule"].items() if i in ids)
             for i in range(200)]
    last = x["last_exposure"]
    return dict(
        first_exposure_step=st.mean(first),
        exposure_span=st.mean([b-a for a,b in zip(first,last)]),
        retention_accuracy=st.mean([e["acc"] for e in es]),
        retention_nll=st.mean([e["nll"] for e in es]),
        retention_discrimination=st.mean([e["disc"] for e in es]),
        terminal_accuracy=es[-1]["acc"], terminal_nll=es[-1]["nll"],
        at_last_accuracy=st.mean([e["correct"] for e in x["at_last_exposure"]]),
        at_last_nll=st.mean([e["nll"] for e in x["at_last_exposure"]]),
        window_accuracy=imm["acc"], window_nll=imm["nll"],
        last_exposure_step=st.mean(last),
        terminal_new_facts_accuracy=es[-1]["int_facts_acc"],
        terminal_new_facts_nll=es[-1]["int_facts_nll"],
        terminal_filler_loss=es[-1]["holdout_loss"],
        parameter_displacement=es[-1]["param_dist"],
        clip_fraction=st.mean([int(v["clip_scale"]<1) for v in steps]),
        mean_preclip_norm=st.mean([v["preclip_norm"] for v in steps]),
        target_coefficient_per_exposure=sum(v["target_coefficient_sum"] for v in steps)/1000,
        clipped_target_coefficient_per_exposure=sum(v["clipped_target_coefficient_sum"] for v in steps)/1000,
        floor_checkpoints=sum(e["acc"]<=.02 for e in es),
        ceiling_checkpoints=sum(e["acc"]>=.98 for e in es))


def audit():
    manifest = json.loads((OUT/"manifest.json").read_text())
    assert manifest == json.loads(git_bytes("90eda1f", "results/study11/manifest.json"))
    assert (ROOT/"docs/STUDY11_PREREGISTRATION.md").read_bytes() == git_bytes(
        "1aac057", "docs/STUDY11_PREREGISTRATION.md")
    for path, expected in manifest["source_sha256"].items():
        assert sha(ROOT/path) == expected, path
        assert hashlib.sha256(git_bytes("8c8eb15", path)).hexdigest() == expected, path
    assert sys.version == manifest["python"]
    for package, expected in manifest["packages"].items():
        assert version(package) == expected
    model = Path(manifest["order"][0]["model_name"])
    for path, expected in manifest["model_files_sha256"].items():
        assert sha(model/path) == expected, path
    assert sha(ROOT/"data/wikitext103_tokens.npy") == manifest["filler_sha256"]
    tokens = np.load(ROOT/"data/wikitext103_tokens.npy", allow_pickle=False)
    chunks = tokens[:len(tokens)//64*64].reshape(-1,64)
    digest = lambda a: hashlib.sha256(np.asarray(a,dtype="<i8").tobytes()).hexdigest()
    tok = AutoTokenizer.from_pretrained(str(model), local_files_only=True)
    configs = {(c["condition"],c["seed"]):c for c in manifest["order"]}
    assert list(configs) == [("spaced",6),("variable_gaps",6),("variable_gaps",7),
                             ("spaced",7),("spaced",8),("variable_gaps",8)]
    logs, values, checked_commits = {}, {}, set()
    for seed in SEEDS:
        order = np.random.default_rng(seed).permutation(len(chunks))
        stream = manifest["streams"][str(seed)]
        assert stream["train_chunks"] == 34500 and stream["heldout_chunks"] == 200
        assert digest(chunks[order[200:34700]]) == stream["train_sha256"]
        assert digest(chunks[order[:200]]) == stream["heldout_sha256"]
        last = np.random.default_rng(seed).integers(256,700,size=200).tolist()
        int_sched = defaultdict(list)
        rng = np.random.default_rng(seed+10000)
        for i in range(50):
            for t in rng.choice(1500,size=4,replace=False).tolist():
                int_sched[str(t)].append(i)
        for arm in ARMS:
            x = json.loads((OUT/f"{arm}_s{seed}"/"log.json").read_text())
            finite(x)
            logs[arm,seed] = x
            assert x["config"] == configs[arm,seed]
            assert len(x["facts"]) == len(x["at_last_exposure"]) == 200
            assert len(x["int_facts"]) == 50 and x["last_exposure"] == last
            p = x["provenance"]
            assert p["snapshot_pinned"] and not p["tracked_code_dirty"]
            assert p["filler_tokens"] == len(tokens)
            assert p["filler_tokens_sha256"] == digest(tokens)
            assert p["filler_file_sha256"] == manifest["filler_sha256"]
            assert p["model_revision"] == configs[arm,seed]["model_revision"]
            for k,v in stream.items():
                assert p[k] == v
            for k,v in p["packages"].items():
                assert manifest["packages"][k] == v
            commit = p["code_commit"]
            if commit not in checked_commits:
                subprocess.run(["git","merge-base","--is-ancestor","90eda1f",commit],cwd=ROOT,check=True)
                for path, expected in manifest["source_sha256"].items():
                    assert hashlib.sha256(git_bytes(commit,path)).hexdigest() == expected
                checked_commits.add(commit)
            expected_sched = defaultdict(list)
            rng = np.random.default_rng(seed+40000)
            for i, end in enumerate(last):
                times = ([end-j*64 for j in range(5)] if arm=="spaced" else
                         [end-256]+(end-256+np.cumsum(rng.permutation([32,32,64,128]))).tolist())
                assert len(set(times))==5 and min(times)==end-256 and max(times)==end
                for t in times:
                    assert 0 <= t < 700
                    expected_sched[str(t)].append(i)
            assert x["target_schedule"] == dict(expected_sched)
            assert x["interference_schedule"] == dict(int_sched)
            g = x["guards"]
            assert g["optimizer_steps"]==2300 and g["filler_tokens_seen"]==2208000
            assert g["exposures"]==1000 and g["int_exposures"]==200
            n_tokens = (5*sum(1+len(tok(f["text"])["input_ids"]) for f in x["facts"])
                       +4*sum(1+len(tok(f["text"])["input_ids"]) for f in x["int_facts"]))
            assert g["fact_tokens_seen"] == n_tokens
            assert len(x["step_guards"])==2300
            assert [a[0] for a in x["train_loss"]] == list(range(0,2300,25))
            for step,v in enumerate(x["step_guards"]):
                assert v["step"] == step
                nt = len(expected_sched.get(str(step-100),[])) if 100<=step<800 else 0
                ni = len(int_sched.get(str(step-800),[])) if step>=800 else 0
                assert (v["targets"],v["interference"]) == (nt,ni)
                scale = min(1.,1./(v["preclip_norm"]+1e-6))
                close(v["clip_scale"],scale)
                close(v["target_coefficient_sum"],nt/(15+nt+ni))
                close(v["clipped_target_coefficient_sum"],nt/(15+nt+ni)*scale)
            assert len(x["evals"]) == 10
            for e in x["evals"]:
                for key in ("per_fact_correct","per_fact_nll","per_fact_nll_foil"):
                    assert len(e[key])==200
                close(e["acc"],st.mean(e["per_fact_correct"]))
                close(e["nll"],st.mean(e["per_fact_nll"]))
                close(e["nll_foil"],st.mean(e["per_fact_nll_foil"]))
                close(e["disc"],st.mean([b-a for a,b in zip(e["per_fact_nll"],e["per_fact_nll_foil"])]))
            values[arm,seed] = metrics(x)
            close(g["acc_at_last_exposure"],values[arm,seed]["at_last_accuracy"])
            close(g["nll_at_last_exposure"],values[arm,seed]["at_last_nll"])
        a,b = logs["spaced",seed],logs["variable_gaps",seed]
        for key in ("facts","int_facts","interference_schedule","last_exposure"):
            assert a[key] == b[key]
        for key in ("optimizer_steps","fact_tokens_seen","filler_tokens_seen","exposures","int_exposures"):
            assert a["guards"][key] == b["guards"][key]
    summary = json.loads((OUT/"summary.json").read_text())
    blocks = 0
    assert set(summary["metrics"]) == set(values["spaced",6])
    for metric in values["spaced",6]:
        a = [values["spaced",s][metric] for s in SEEDS]
        b = [values["variable_gaps",s][metric] for s in SEEDS]
        for name, data in [("spaced",a),("variable_gaps",b),("variable_gaps_minus_spaced",[y-x for x,y in zip(a,b)])]:
            wanted = describe(data)
            saved = summary["metrics"][metric][name]
            for k in wanted:
                if k=="values":
                    for x,y in zip(wanted[k],saved[k]):
                        close(x,y)
                else:
                    close(wanted[k],saved[k])
            blocks += 1
    ds = [values["variable_gaps",s]["retention_accuracy"]-values["spaced",s]["retention_accuracy"] for s in SEEDS]
    d = describe(ds)
    direction = ("positive_directional_signal" if min(ds)>0 and d["mean"]>d["sample_sd"] else
                 "negative_directional_signal" if max(ds)<0 and abs(d["mean"])>d["sample_sd"] else
                 "mixed_or_inconclusive")
    assert summary["direction"] == direction
    assert summary["complete_runs"] == 6 and summary["screening_only"]
    expected_prediction = ("contradicted" if direction=="positive_directional_signal"
                           else "no_consistent_positive_signal_as_predicted")
    assert summary["prediction_status"] == expected_prediction
    dnll = st.mean([values["variable_gaps",s]["retention_nll"]-values["spaced",s]["retention_nll"] for s in SEEDS])
    assert summary["metrics_discordant"] == (st.mean(ds)*dnll > 0)
    for seed,saved in zip(SEEDS,summary["pre_intervention_guards"]):
        a,b = logs["spaced",seed],logs["variable_gaps",seed]
        diffs = [abs(x[1]-y[1]) for x,y in zip(a["train_loss"],b["train_loss"]) if x[0]<100]
        assert saved["seed"]==seed
        close(saved["max_pre_injection_training_loss_difference"],max(diffs))
        close(saved["pretrained_holdout_difference"],b["evals"][0]["holdout_loss"]-a["evals"][0]["holdout_loss"])
    report = (OUT/"REPORT.md").read_text()
    for metric, arms in summary["metrics"].items():
        fmt = lambda d: f"{d['mean']:.5f} ± {d['sample_sd']:.5f} [{d['min']:.5f}, {d['max']:.5f}]"
        assert f"| {metric} | {fmt(arms['spaced'])} | {fmt(arms['variable_gaps'])} | {fmt(arms['variable_gaps_minus_spaced'])} |" in report
    for seed in SEEDS:
        a,b = values["spaced",seed]["retention_accuracy"],values["variable_gaps",seed]["retention_accuracy"]
        assert f"| {seed} | {a:.6f} | {b:.6f} | {b-a:+.6f} |" in report
    return dict(status="PASS",summary_blocks=blocks,complete_runs=6,
                direction=direction,primary_difference=describe(ds),
                run_sha256={f"{c}_s{s}":sha(OUT/f"{c}_s{s}"/"log.json") for c,s in configs},
                wall_seconds={f"{c}_s{s}":logs[c,s]["guards"]["wall_seconds"] for c,s in configs},
                fact_token_budgets={str(s):logs["spaced",s]["guards"]["fact_tokens_seen"] for s in SEEDS},
                source_commits=sorted(checked_commits))


if __name__ == "__main__":
    print(json.dumps(audit(),indent=2))
