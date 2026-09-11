"""Read-only check of Study 13's published primary result; no dependencies or training."""
import json
import math
from pathlib import Path
from statistics import mean, stdev


def main():
    root = Path(__file__).resolve().parents[1] / 'results/study13'
    checkpoints = (200, 400, 800, 1200, 1500)
    values = {'uniform': [], 'prioritized': []}
    for seed in (12, 13, 14):
        for arm in values:
            log = json.loads((root / f'seed_{seed}' / arm / 'log.json').read_text())
            assert log['seed'] == seed and log['arm'] == arm
            records = {row['int_step']: row for row in log['evals']}
            assert len(records) == len(log['evals']), 'Duplicate evaluation steps'
            measured = []
            for step in checkpoints:
                row = records[step]
                correct = row['per_fact_correct']
                assert len(correct) == 200 and all(v in (0, 1) for v in correct)
                assert math.isclose(mean(correct), row['acc'], abs_tol=1e-12)
                measured.append(row['acc'])
            values[arm].append(mean(measured))
    delta = [p - u for p, u in zip(values['prioritized'], values['uniform'])]
    summary = json.loads((root / 'summary.json').read_text())['metrics']['retention_accuracy']
    for key, vector in {**values, 'prioritized_minus_uniform': delta}.items():
        saved = summary[key]
        assert len(vector) == len(saved['values']) == 3
        assert all(math.isclose(a, b, abs_tol=1e-12) for a, b in zip(vector, saved['values']))
        assert math.isclose(mean(vector), saved['mean'], abs_tol=1e-12)
        assert math.isclose(stdev(vector), saved['sample_sd'], abs_tol=1e-12)
        print(f'{key}: mean {100*mean(vector):.2f} pp, sample SD {100*stdev(vector):.2f} pp; '
              f'paired-seed values {[round(100*v, 2) for v in vector]}')
    print('PASS: published primary measurements agree with the summary. This is not a training replication or significance test.')


if __name__ == '__main__':
    main()
