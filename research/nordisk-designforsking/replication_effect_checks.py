#!/usr/bin/env python3
"""Fisher-z sensitivity check for published correlations in one design replication.

The inputs are *reported aggregate statistics*, not raw participant-level data.
The two cohorts are assumed independent. Measurement equivalence, adaptation
bias, attrition and multiple comparisons are NOT resolved by this calculation.
"""
from __future__ import annotations
import json
import math
from datetime import datetime, timezone

SOURCE_DOI = "10.1017/pds.2024.14"
CASES = [
    {
        "metric": "Verification frequency versus analysis success",
        "original_r": 0.63,
        "original_n": 24,
        "replication_r": 0.48,
        "replication_n": 16,
        "source_pdf_pages": "6–7 (printed pp. 120–121)",
        "source_reported_p_original": 0.001,
        "source_reported_p_replication": 0.060,
    },
    {
        "metric": "Evaluation frequency versus analysis success, extreme deciles",
        "original_r": 0.85,
        "original_n": 10,
        "replication_r": 0.34,
        "replication_n": 10,
        "source_pdf_pages": "7 (printed p. 121)",
        "source_reported_p_original": 0.002,
        "source_reported_p_replication": 0.337,
    },
]
Z95 = 1.959963984540054

def fisher_interval(r: float, n: int):
    if not (-1 < r < 1) or n <= 3:
        raise ValueError("Require -1 < r < 1 and sample n > 3")
    z = math.atanh(r)
    spread = Z95 / math.sqrt(n - 3)
    return [math.tanh(z - spread), math.tanh(z + spread)]

def compare_independent(r1: float, n1: int, r2: float, n2: int):
    z1, z2 = math.atanh(r1), math.atanh(r2)
    se = math.sqrt(1 / (n1 - 3) + 1 / (n2 - 3))
    z = (z1 - z2) / se
    p_two_sided = math.erfc(abs(z) / math.sqrt(2))
    return {
        "z_difference": z,
        "p_two_sided": p_two_sided,
        "original_r_ci95_fisher": fisher_interval(r1, n1),
        "replication_r_ci95_fisher": fisher_interval(r2, n2),
        "difference_significant_at_0_05": p_two_sided < 0.05,
    }

def main():
    checks = [
        dict(case, **compare_independent(case["original_r"], case["original_n"],
                                         case["replication_r"], case["replication_n"]))
        for case in CASES
    ]
    result = {
        "study_doi": SOURCE_DOI,
        "study_pdf": "https://publikationen.bibliothek.kit.edu/1000171833/153147840",
        "statistical_method": "Independent-samples Fisher r-to-z difference test; asymptotic 95% confidence intervals",
        "inference_scope": (
            "Illustrative, exploratory reanalysis of published summary numbers. "
            "Non-significant differences do not demonstrate equivalence; "
            "the underlying replication deliberately changed elements of its "
            "sample, apparatus and operationalisation. Do not infer population-level replicability."
        ),
        "checks": checks,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
if __name__ == "__main__":
    main()
