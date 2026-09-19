# Playground verification

## English UI publication check (19 September 2026)

- The page, architecture explanations, controls, model metadata and displayed
  error messages are English. A small footer credits GPT Astra for building the
  playground for the author's experiments, without claiming the research idea.
- Four Node tests cover page language, credit, metadata/error translation and
  preservation of prompt, answer and generated-text rendering. The first three
  tests were observed failing before translation and passing afterward.
- All 28 playground Python tests pass, including real tiny-model generation,
  plain-input behavior, route allowlists and local-only request protections.
- Browser checks confirmed English model/stage labels, historical records,
  prefix search, the length-limit error, and a four-token generation through the
  saved Study 13 seed 12 common checkpoint. Its receipt confirmed model and
  checkpoint checksums, plain input, and English token/probability explanations.
- Translation is browser-only. The existing Python modules, model weights and
  experimental records were not changed. Raw JSON remains raw. These checks are
  software verification, not new research trials.
- Publication means source code on GitHub, not a public inference endpoint.

## Original local verification (11 September 2026)

11 September 2026. These are software and manual interface checks, not additional
experimental runs or a new research finding.

## Observed checks

- Original regression suite plus playground tests: 106 passed (80 research-code
  tests and 26 local-app tests).
- JavaScript syntax check passed. The actual HTML's two assets resolve through
  the server; a regression test guards against incorrect asset URLs.
- Saved Study 13 seed 12 common model generated a real continuation through the
  HTTP/UI path; the pretrained model generated a different continuation for the
  same prefix. Responses retained their own model/stage labels.
- Local model/tokenizer hashes matched the original Study 13 manifest. The saved
  seed 12 fork hash matched the common record before loading.
- Review caught inconsistent required-file sets in availability versus loading.
  Both now use the same seven-file manifest; a partial-snapshot regression was
  observed failing before the fix and passing afterward.
- Direct inference and browser inference succeeded on MPS. This does not mean
  every saved checkpoint, operating system or possible prompt was exercised.
- Desktop records drawer closes and reflows the layout. On a 390px viewport,
  content width and scroll width were both 375px (remaining width is scrollbar),
  with no horizontal overflow. A fresh mobile load starts with both side panels
  closed. The viewport override was reset after checking.
- Switching the historical drawer to Study 12, seed 10, prioritized loaded the
  corresponding real record without changing the live-model selection.
- Length 65 was visibly rejected without a generation request. Length 12 produced
  an actual answer; later changing the control to 24 did not change that answer's
  stored settings receipt.
- Input-token pieces and actual first-next-token probabilities were visible in
  the answer details. Expected answer stayed behind its reveal control.
- Browser console check returned no errors or warnings after the integrated load.
- Imported research source/tests and numeric JSON values remained intact, verified
  against the public export manifest. No original model, result or registration
  file was written by this feature.

## Scope and limits

The recorded final uniform/prioritized policies are not live models: their weights
were not saved. Only pretrained and retained common-prefix models are offered.
There is no training, activation probing, model editing, result mutation, remote
API call or deployment. Architecture is a schematic; exact GPT-2 dimensions come
from the local config. No claim of scientific replication is made by this check.

At that time the new files lived on the local `feat/local-playground` branch. Research originals
are outside the app's write scope; unrelated local README/image changes observed
in the original research directory were left untouched.
