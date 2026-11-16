import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import control


class BudgetTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.state_file = Path(self.temporary.name) / "state.json"
        self.initial = control.read_state()
        self.state_file.write_text(json.dumps(self.initial), encoding="utf-8")

    def test_ten_reservations_are_the_maximum(self):
        with patch.object(control, "STATE", self.state_file):
            state = control.read_state()
            state.update(attempts=9, reserved_usd=72.0, estimated_usd=71.0, no_gain=0)
            self.assertFalse(control.complete(state))
            state.update(attempts=10, reserved_usd=80.0)
            self.assertTrue(control.complete(state))

    def test_no_improvement_stops_early(self):
        state = dict(self.initial, no_gain=2)
        self.assertTrue(control.complete(state))

    def test_estimated_cost_stops_future_spending(self):
        state = dict(self.initial, attempts=8, reserved_usd=64.0, estimated_usd=74.0)
        self.assertTrue(control.complete(state))

    def test_candidate_cannot_access_files(self):
        candidate = Path(self.temporary.name) / "candidate.py"
        candidate.write_text("def predict(features, y_train):\n    return open('hidden.csv').read()\n", encoding="utf-8")
        with patch.object(control, "CANDIDATE", candidate):
            with self.assertRaisesRegex(ValueError, "external"):
                control.candidate_is_safe()

    def test_reference_candidate_is_allowed(self):
        control.candidate_is_safe()


if __name__ == "__main__":
    unittest.main()
