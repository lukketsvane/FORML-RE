"""Synthetic multiscale viability model for FORMLÆRE.

Two local agents are embedded in one collective agent. The model contrasts
compensatory weighted selection with non-compensatory viability constraints,
then adds a meta-grammar rule that enables shared feedback. It is a synthetic
stress-test, not empirical evidence about living systems.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping


@dataclass(frozen=True)
class Outcome:
    agent_1: float
    agent_2: float

    @property
    def collective(self) -> float:
        return max(self.agent_1, self.agent_2)


@dataclass(frozen=True)
class Rule:
    name: str
    outcome: Outcome


DISTURBANCES: tuple[tuple[float, float], ...] = (
    (0.0, 0.0), (0.2, 0.0), (0.0, 0.2), (0.2, 0.2),
)
LIMIT = 1.0


def stressed(outcome: Outcome, disturbance: tuple[float, float]) -> Outcome:
    return Outcome(outcome.agent_1 + disturbance[0],
                   outcome.agent_2 + disturbance[1])


def is_viable(rule: Rule,
              disturbances: Iterable[tuple[float, float]] = DISTURBANCES,
              limit: float = LIMIT) -> bool:
    for disturbance in disturbances:
        value = stressed(rule.outcome, disturbance)
        if value.agent_1 > limit or value.agent_2 > limit or value.collective > limit:
            return False
    return True


def viable_rules(rules: Iterable[Rule]) -> tuple[Rule, ...]:
    return tuple(rule for rule in rules if is_viable(rule))


def weighted_score(rule: Rule, weights: tuple[float, float, float]) -> float:
    w1, w2, wg = weights
    value = rule.outcome
    return w1 * value.agent_1 + w2 * value.agent_2 + wg * value.collective


def weighted_choice(rules: Iterable[Rule],
                    weights: tuple[float, float, float]) -> Rule:
    return min(rules, key=lambda rule: weighted_score(rule, weights))


def initial_grammar() -> tuple[Rule, ...]:
    return (
        Rule("local-1-priority", Outcome(0.0, 2.4)),
        Rule("local-2-priority", Outcome(2.4, 0.0)),
        Rule("balanced-legacy", Outcome(1.2, 1.2)),
    )


def meta_grammar_operation(rules: Iterable[Rule]) -> tuple[Rule, ...]:
    return tuple(rules) + (Rule("coordinated-feedback", Outcome(0.4, 0.4)),)


@dataclass(frozen=True)
class HiddenStateOutcome:
    state_1: Outcome
    state_2: Outcome


def robust_under_partial_observation(
    candidates: Mapping[str, HiddenStateOutcome],
) -> tuple[str, ...]:
    viable: list[str] = []
    for name, outcomes in candidates.items():
        if is_viable(Rule(name, outcomes.state_1)) and is_viable(Rule(name, outcomes.state_2)):
            viable.append(name)
    return tuple(viable)


def partial_observation_candidates(include_feedback: bool = False) -> dict[str, HiddenStateOutcome]:
    candidates = {
        "respond-to-agent-1": HiddenStateOutcome(Outcome(0.2, 1.6), Outcome(2.0, 0.2)),
        "respond-to-agent-2": HiddenStateOutcome(Outcome(1.6, 0.2), Outcome(0.2, 2.0)),
    }
    if include_feedback:
        candidates["shared-feedback"] = HiddenStateOutcome(Outcome(0.4, 0.4), Outcome(0.4, 0.4))
    return candidates


def demonstration() -> dict[str, object]:
    legacy = initial_grammar()
    choice_1 = weighted_choice(legacy, (0.8, 0.1, 0.1))
    choice_2 = weighted_choice(legacy, (0.1, 0.8, 0.1))
    expanded = meta_grammar_operation(legacy)
    return {
        "legacy_viable": [rule.name for rule in viable_rules(legacy)],
        "weighted_choice_agent_1_priority": {
            "rule": choice_1.name, "outcome": choice_1.outcome.__dict__, "viable": is_viable(choice_1)
        },
        "weighted_choice_agent_2_priority": {
            "rule": choice_2.name, "outcome": choice_2.outcome.__dict__, "viable": is_viable(choice_2)
        },
        "meta_grammar_viable": [rule.name for rule in viable_rules(expanded)],
        "partial_observation_before_feedback": list(robust_under_partial_observation(partial_observation_candidates(False))),
        "partial_observation_after_feedback": list(robust_under_partial_observation(partial_observation_candidates(True))),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(demonstration(), ensure_ascii=False, indent=2))
