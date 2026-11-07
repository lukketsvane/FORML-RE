"""Strengare regresjonstestar for choice_benchmark.py.

Alle forsøksutfall er syntetiske. Dei testar kodens reglar og evna
til å motbevise Formlæra, ikkje empirisk sanningsverdi.
"""
from copy import deepcopy
import unittest

from choice_benchmark import (
    benchmark, bootstrap_difference, probs, rows_to_cases, synthetic_rows
)


class BenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.form = benchmark(rows_to_cases(synthetic_rows("form")))
        cls.uniform = benchmark(rows_to_cases(synthetic_rows("uniform")))
        cls.adversarial = benchmark(rows_to_cases(synthetic_rows("adversarial")))

    def test_valid_folds(self):
        self.assertEqual(self.form["case_counts"], {"train": 440, "validation": 120, "test": 240})

    def test_form_can_win_if_generating_mechanism_matches(self):
        losses = self.form["heldout_test"]
        self.assertLess(losses["form"]["mean_log_loss"], losses["grammar"]["mean_log_loss"])
        self.assertLess(losses["form"]["mean_log_loss"], losses["weight_only"]["mean_log_loss"])

    def test_form_cannot_claim_victory_against_flexible_model_without_evidence(self):
        losses = self.form["heldout_test"]
        self.assertLess(abs(losses["form"]["mean_log_loss"] - losses["conditional_logit"]["mean_log_loss"]), 0.05)
        interval = self.form["paired_ci95"]["conditional_logit"]["ci95_cluster_bootstrap"]
        self.assertLess(interval[0], 0)
        self.assertGreater(interval[1], 0)

    def test_uniform_can_beat_form(self):
        loss = self.uniform["heldout_test"]
        self.assertLess(loss["uniform"]["mean_log_loss"], loss["form"]["mean_log_loss"])

    def test_rival_can_beat_form_by_large_margin(self):
        loss = self.adversarial["heldout_test"]
        self.assertLess(loss["conditional_logit"]["mean_log_loss"], loss["form"]["mean_log_loss"] - 0.3)

    def test_nonnegative_beta_under_wrong_estimates(self):
        self.assertEqual(self.adversarial["fitted_parameters"]["form_beta"], 0.0)

    def test_wrong_choice_count_is_rejected(self):
        rows = synthetic_rows("form")[:12]
        rows[1]["chosen"] = "1"
        with self.assertRaisesRegex(ValueError, "nøyaktig eitt"):
            rows_to_cases(rows)

    def test_holdout_group_leakage_is_rejected(self):
        rows = synthetic_rows("form")
        train_group = rows[0]["group_id"]
        for row in rows:
            if row["case_id"] == "form-0440":
                row["group_id"] = train_group
        with self.assertRaisesRegex(ValueError, "LEKKASJE"):
            rows_to_cases(rows)

    def test_unreachable_choice_is_rejected(self):
        rows = synthetic_rows("form")
        first = next(r for r in rows[:4] if r["chosen"] == "1")
        first["feasible"] = "0"
        with self.assertRaisesRegex(ValueError, "utanfor D"):
            rows_to_cases(rows)

    def test_non_normalized_agent_weights_are_rejected(self):
        rows = synthetic_rows("form")
        for row in rows[:4]:
            row["w1"] = "0.8"
        with self.assertRaisesRegex(ValueError, "summere til éin"):
            rows_to_cases(rows)

    def test_probabilities_normalize_for_each_model(self):
        case = rows_to_cases(synthetic_rows("form"))[0]
        for name, params in [
            ("uniform", {}), ("grammar", {}),
            ("form", {"beta": 1.0}), ("weight_only", {"beta": 1.0}),
            ("conditional_logit", {"theta": [1.0, -0.5]}),
        ]:
            p = probs(case, name, **params)
            self.assertAlmostEqual(sum(p), 1.0, places=12)

    def test_cluster_bootstrap_counts_independent_groups(self):
        outcome = bootstrap_difference(
            [0.1, 0.1, 0.9, 0.9], [0.2, 0.2, 0.6, 0.6],
            ["project_A", "project_A", "project_B", "project_B"],
            draws=300, seed=123,
        )
        self.assertEqual(outcome["independent_groups"], 2)
        self.assertEqual(len(outcome["ci95_cluster_bootstrap"]), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
