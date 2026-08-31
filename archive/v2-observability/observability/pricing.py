#!/usr/bin/env python3
"""
Model pricing for the Claude Agent Framework observability system.

Costs are USD per 1M tokens, matching current Anthropic first-party API rates.
Partner platforms (Bedrock, Vertex) bill separately and are not covered here.

Update RATES when pricing changes; `test_observability.py` checks the arithmetic,
not the rates themselves.
"""
from typing import Dict, NamedTuple, Optional


class Rate(NamedTuple):
    """USD per 1M tokens."""
    input: float
    output: float
    context_window: int


# Keyed by the short tier name used in REGISTRY.json and agent frontmatter.
RATES: Dict[str, Rate] = {
    'haiku':  Rate(input=1.00,  output=5.00,  context_window=200_000),
    'sonnet': Rate(input=2.00,  output=10.00, context_window=1_000_000),
    'opus':   Rate(input=5.00,  output=25.00, context_window=1_000_000),
    'fable':  Rate(input=10.00, output=50.00, context_window=1_000_000),
}

# Full model IDs map onto the same tiers, so either form can be logged.
MODEL_ALIASES: Dict[str, str] = {
    'claude-haiku-4-5':  'haiku',
    'claude-sonnet-5':   'sonnet',
    'claude-opus-5':     'opus',
    'claude-fable-5':    'fable',
}

# Cache reads are billed at roughly a tenth of the input rate. This is the single
# largest lever in a multi-agent system with a stable prompt prefix.
CACHE_READ_MULTIPLIER = 0.1

# Cache writes (creating the cached prefix) are billed at a premium over base
# input. Ignoring them makes a repeatedly-invalidated prefix look cheaper than a
# correctly-cached one - inverting the exact signal caching metrics exist to give.
CACHE_WRITE_MULTIPLIER = 1.25


def normalize_model(model: Optional[str]) -> Optional[str]:
    """Resolve a model id or tier name to a tier key. Returns None if unknown."""
    if not model:
        return None
    key = model.strip().lower()
    key = MODEL_ALIASES.get(key, key)
    return key if key in RATES else None


def get_rate(model: Optional[str]) -> Optional[Rate]:
    """Look up the rate for a model. Returns None if the model is unknown."""
    tier = normalize_model(model)
    return RATES[tier] if tier else None


def calculate_cost(
    model: Optional[str],
    tokens_input: int = 0,
    tokens_output: int = 0,
    tokens_cached: int = 0,
    tokens_cache_write: int = 0,
) -> Optional[float]:
    """
    Compute execution cost in USD.

    `tokens_cached` is cache *reads* — tokens served from a cached prefix at
    CACHE_READ_MULTIPLIER of the input rate. `tokens_cache_write` is cache
    *creation*, billed at CACHE_WRITE_MULTIPLIER (a premium over base input).
    Both are counted separately from `tokens_input`, not as subsets of it.

    Returns **None** for an unknown or unpriced model — never raises, so logging
    an unrecognized model cannot break a hook mid-execution. None is distinct
    from 0.0: it means "cost unknown", and callers must store it as NULL rather
    than as zero. Recording an unpriced run as $0.00 makes an expensive tier look
    free, which is worse than recording nothing.
    """
    rate = get_rate(model)
    if rate is None:
        return None

    cost = (
        tokens_input * rate.input
        + tokens_output * rate.output
        + tokens_cached * rate.input * CACHE_READ_MULTIPLIER
        + tokens_cache_write * rate.input * CACHE_WRITE_MULTIPLIER
    ) / 1_000_000
    return round(cost, 6)


def context_window(model: Optional[str]) -> Optional[int]:
    """Context window for a model, or None if unknown."""
    rate = get_rate(model)
    return rate.context_window if rate else None


def is_long_context_safe(model: Optional[str], estimated_tokens: int) -> bool:
    """
    Whether a model can hold this much context.

    Haiku is the only current model at 200K; everything else is 1M. Routing a
    long-context task to haiku is the most common tier mistake.
    """
    window = context_window(model)
    return window is not None and estimated_tokens <= window


if __name__ == '__main__':
    print(f"{'tier':<8} {'in $/1M':>9} {'out $/1M':>9} {'context':>12}")
    for tier, rate in RATES.items():
        print(f"{tier:<8} {rate.input:>9.2f} {rate.output:>9.2f} {rate.context_window:>12,}")
    print(f"\ncache reads  billed at {CACHE_READ_MULTIPLIER}x the input rate")
    print(f"cache writes billed at {CACHE_WRITE_MULTIPLIER}x the input rate")
