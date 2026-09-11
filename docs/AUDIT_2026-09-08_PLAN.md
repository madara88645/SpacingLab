# Data-stream provenance audit (2026-09-08)

Registered after reading the external review, the loader, and the Git list of cache
revisions; before computing snapshot sizes, permutations, or run comparisons below.
This is a retrospective software/provenance audit, not a new confirmatory ML study.
Previously reported outcome numbers are already known. Historical registrations stand.

## One question

Did Study 6 random placement and its Study 1 spaced comparator actually use the same
filler/held-out token stream, as required by their cross-study interpretation?

## Prediction and test

The loader returns the entire cached token array. `FillerStream` permutes all chunks
in that array. I predict a longer cache therefore changes both training and held-out
chunks under the same seed. Study 5's longer run may have grown this cache before
Study 6, invalidating that particular data-matching assumption.

1. Read every Git-tracked version of the token cache, hash its bytes, and record size.
2. On seeds 0, 1, 2 reconstruct train and held-out selections for those snapshots;
   compare hashes for the same requested number of training tokens.
3. Compare the logged *pretrained* held-out loss and pre-injection training-loss
   prefix for Study 1 vs Study 6. Different fingerprints before any fact injection
   cannot be attributed to the fact exposure schedule. Do not use later outcomes
   to identify a stream. Git snapshot timing is provenance evidence, not proof of
   the exact bytes loaded by a historical process: those hashes were not logged.
4. Inventory actual complete main runs, pilot runs and incomplete folders separately.
5. Publish all results, including if the suspected issue does not occur.

## Interpretation and traps

- Changed deterministic stream hashes prove the loader failure mode. Changed
  pre-intervention logs strengthen historical mismatch evidence, but do not identify
  an unknown model/library change; note absent provenance explicitly.
- Same token *counts*, seeds, or average losses do not establish identical data.
- A cache extension may preserve every earlier token and still change the permutation.
- Same-seed kernels may have numerical noise; hashes of CPU integer token selections
  have none. Tiny floating-point loss differences alone are not a conclusive test.
- The audit cannot estimate how much of the observed random-minus-spaced score gap
  is caused by data changes, nor disprove the within-study massed/spaced result.
- If a mismatch is supported, withdraw 'ordinary shuffling suffices' as an isolated
  causal comparison pending a newly paired experiment with immutable input hashes.
- No model training, hyperparameter tuning, publication or external writes in this audit.
