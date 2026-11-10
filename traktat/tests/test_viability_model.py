"""Synthetic tests for the multiscale viability propositions."""
import unittest

from viability_model import (
    initial_grammar,
    is_viable,
    meta_grammar_operation,
    partial_observation_candidates,
    robust_under_partial_observation,
    viable_rules,
    weighted_choice,
)


class ViabilityModelTests(unittest.TestCase):
    def test_scalar_weighting_can_choose_a_rule_that_harms_another_agent(self):
        chosen = weighted_choice(initial_grammar(), (0.8, 0.1, 0.1))
        self.assertEqual(chosen.name, "local-1-priority")
        self.assertFalse(is_viable(chosen))
        self.assertGreater(chosen.outcome.agent_2, 1.0)

    def test_legacy_grammar_has_an_empty_viability_kernel(self):
        self.assertEqual(viable_rules(initial_grammar()), ())

    def test_meta_grammar_operation_opens_a_viable_transition(self):
        expanded = meta_grammar_operation(initial_grammar())
        self.assertEqual([rule.name for rule in viable_rules(expanded)],
                         ["coordinated-feedback"])

    def test_collective_average_cannot_hide_a_local_threshold_breach(self):
        chosen = weighted_choice(initial_grammar(), (0.8, 0.1, 0.1))
        self.assertLess((chosen.outcome.agent_1 + chosen.outcome.agent_2) / 2, 1.3)
        self.assertFalse(is_viable(chosen))

    def test_partial_observation_requires_one_policy_safe_in_every_hidden_state(self):
        self.assertEqual(robust_under_partial_observation(partial_observation_candidates(False)), ())
        self.assertEqual(robust_under_partial_observation(partial_observation_candidates(True)),
                         ("shared-feedback",))


if __name__ == "__main__":
    unittest.main()
