# Public snapshot and reproduction boundaries

Published from the local research state on 11 September 2026. The original local
repository and its chronological commits were left unchanged. This public repository
starts a new Git history; it does not manufacture a public registration date for past work.

## What changed for publication

- Original root README is preserved as `RESEARCH_REPORT.md`; a new navigation README
  introduces the full body of work rather than replacing it.
- Personal project-directory and home-directory prefixes in text metadata are
  replaced with `<PROJECT_ROOT>` and `<USER_HOME>`. These are explanatory placeholders,
  not executable filesystem paths. References to the private operational handoff
  are routed here. No experimental numeric values or training source were changed.
- Six files are omitted: a private operational handoff, two conversation handoffs,
  two operational launch plans and the third-party WikiText token cache. The exact
  list and original hashes are in `EXPORT_MANIFEST.json`.
- Ignored model checkpoints, environment files, lock receipts and untracked files
  were never exported. No new pretrained-model training or evaluation was performed
  to prepare this publication.

`EXPORT_MANIFEST.json` records the original local commit identifier, original file
hashes and hashes of exported copies. It is a publication receipt, not independent
proof of preregistration timing. It covers imported research files before adding
the public README, this note and the read-only result-checking script.

## Historical evidence versus checks you can run

The original preregistrations, amendments, negative findings and withdrawn claims
remain available. Reports referring to a PASS, a completed training run or an old
commit describe the original local research state. They are not claims that a fresh
public clone can reproduce every historical audit unchanged.

In particular, path redaction changes some JSON file hashes. Hash references inside
historical manifests and audits deliberately retain their original values. Do not
rewrite them to make a provenance check pass. Historical audits can also require
local Git commits and checkpoint files absent here.

The new `scripts/check_public_results.py` reads published measurements and verifies
the latest primary result without loading a model, accessing a dataset, or relying
on original machine paths. Existing unit tests exercise software behavior with
test fixtures; passing them is not a replication of the scientific experiment.

## Training inputs

The research used GPT-2 revision `607a30d783dfa663caf39e06633721c8d4cfcd7e` and a
WikiText-103 token snapshot. The frozen study manifests specify input hashes.
Weights and the token cache are not redistributed in this snapshot. Obtain
third-party inputs from their original providers under their applicable terms.

The historical training runners include machine-bound preflight checks and fixed
output locations. Do not run them over the published evidence directories. A future
replication needs a separate output directory, correctly verified inputs, and a
newly documented protocol. Simply downloading fresh WikiText or editing manifest
hashes would not reproduce the original experiment.
