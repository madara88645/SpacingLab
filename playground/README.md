# SpacingLab local playground

A local English-language interface for directly running a saved GPT-2 model, inspecting
its architecture and reading recent experimental records. No cloud API or key is
used. Nothing here trains the model or modifies research results.

This playground was built by GPT Astra to help me explore my SpacingLab experiments.
The credit is for the playground implementation, not authorship of the research idea.

The source is published on GitHub; this is not an internet-hosted inference service.

## Start

From the repository root, with the existing locked environment installed:

```sh
uv run --no-sync python -m playground.server
```

Open **http://127.0.0.1:8765**. Stop the server with Ctrl+C in its terminal.
The browser's unload button releases model memory but does not stop the server.
For a new clone, first run `uv sync --locked --group dev`.

## First example

1. Select **Study 13 · Common checkpoint · Seed 12**, if its local weights are available.
2. Choose a learned sentence. Only the prefix is inserted into the input; the
   expected answer remains hidden until you explicitly reveal it.
3. Press the generation button. The continuation comes from the actual model,
   not from the stored answer. Change the prefix and try again if you wish.
4. Click an architecture block for a short explanation. Input token pieces and
   the first next-token probabilities are real model outputs; the layer diagram
   itself is only a schematic, not a live activation visualization.
5. Open the records drawer to compare saved uniform/prioritized measurements.
   These are historical measurements, not a score for the current prompt.

Each message is an independent completion. Previous messages are not silently
added to the prompt. GPT-2 is not an instruction-following chat assistant; the
experiments taught English sentence completions, so conversational Turkish
questions are not expected to work like ChatGPT.

### Plain input (2026-09-12)

The playground no longer silently prepends the EOS boundary token. It sends
exactly the encoded user text; EOS is still used for stopping and masked padding.
New response receipts include `input_format: "plain"`. This is an inference-only
change: no checkpoint or historical research measurement has been altered.

Removing this trigger reduces the measured trained-topic intrusions, but also
reduces retrieval of the facts taught with that prefix. It is a partial workaround,
not a general model-quality fix or evidence that spacing caused the intrusion.
The original research measurements used EOS and should not be compared directly
with the new playground's fact accuracy.

The English UI translates labels and error messages in the browser. It does not
translate prompts, generated text, token pieces, answers or raw experimental JSON.
The Python inference and data modules remain unchanged, preserving their recorded
source hashes. Direct API clients still receive the original metadata language.

## Which model is running?

There are four explicit selections: pretrained GPT-2 and three saved Study 13
common-prefix models (seeds 12,13,14). The saved experimental checkpoint is after
800 updates, **before** the two replay policies diverge. Final uniform/prioritized
weights were not saved, so they are not offered as live inference models.

The labels preserve this distinction. Choosing a final arm in the records drawer
does not change the live model. There is no hidden rerun to recover missing models.

For the pretrained model and every checkpoint load, the model/tokenizer files are
checked against the Study 13 manifest's original hashes. The saved checkpoint
itself is checked against its common record, then loaded read-only with safe
tensor-only deserialization. The optimizer is never restored for this app.

## Local files

The public repository intentionally does not contain model weights. By default,
the app looks for the pinned GPT-2 snapshot in the standard local Hugging Face
cache, revision `607a30d783dfa663caf39e06633721c8d4cfcd7e`. It reads saved forks from
the sibling original research directory, `SpacingLab/results/study13/seed_*/fork.pt`.
It never downloads or replaces missing inputs automatically.

For a different local arrangement, supply trusted directories explicitly:

```sh
uv run --no-sync python -m playground.server \
  --research-root /absolute/path/to/original/SpacingLab \
  --model-dir /absolute/path/to/pinned/gpt2/snapshot
```

Without those files, the architecture and saved-record views still work; inference
is unavailable. The main publication's [reproduction boundaries](../PUBLICATION.md)
still apply. The UI should not be interpreted as making archived training fully
reproducible from a public clone.

## Controls and limits

- Maximum 64 generated tokens and 512 input tokens, with a 2,000-character input
  cap. A token is a text fragment, not necessarily a whole word.
- Temperature 0 uses the most likely next token. Positive temperature samples;
  this changes the answer selection, **not** the model's learned weights.
- Only one model and one generation request are active at a time. Loading a fork
  takes a few seconds and consumes local RAM. The app uses Apple MPS if available,
  otherwise CPU. A seed aids repeatability but is not a cross-device guarantee.
- First-next-token probabilities are the model's distribution before temperature
  sampling; they are not a truth score or confidence for the entire sentence.
- No training, layer editing, background runs, telemetry, remote calls, filesystem
  picker endpoint, result editing or persistent prompt history. Clear history
  removes the visible transcript; reload also clears it.
- The server binds loopback only, validates Host/Origin and requires a per-session
  token for generation/unload. This is a personal development tool, not a hardened
  multi-user or internet-hosted service. Do not expose it through a public tunnel.

## Checks

```sh
uv run --no-sync pytest -q tests playground/test_playground.py
uv run --no-project python scripts/check_public_results.py
node --check playground/static/app.js
node --test playground/ui_english.test.cjs
```

Software tests and manual inference checks do not extend the scientific study.
