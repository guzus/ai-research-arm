#!/usr/bin/env python3
"""Regression tests for market quote timestamp normalization."""

from __future__ import annotations

import math
import unittest
from datetime import datetime, timezone

from fetch_market_quotes import _epoch_seconds


class TimestampLike:
    """Minimal stand-in for pandas Timestamp without making tests require it."""

    def __init__(self, value: float) -> None:
        self.value = value

    def timestamp(self) -> float:
        return self.value


class MissingTimestampLike:
    """Matches pandas NaT's timestamp failure behavior."""

    def timestamp(self) -> float:
        raise ValueError("NaTType does not support timestamp")


class EpochSecondsTests(unittest.TestCase):
    def test_datetime_like_timestamp(self) -> None:
        value = datetime(2026, 9, 2, 4, 0, tzinfo=timezone.utc)
        self.assertEqual(_epoch_seconds(value), 1_788_321_600)
        self.assertEqual(_epoch_seconds(TimestampLike(value.timestamp())), 1_788_321_600)

    def test_numeric_epoch(self) -> None:
        self.assertEqual(_epoch_seconds(1_788_321_600), 1_788_321_600)
        self.assertEqual(_epoch_seconds(1_788_321_600.9), 1_788_321_600)

    def test_missing_and_non_finite_values(self) -> None:
        self.assertIsNone(_epoch_seconds(None))
        self.assertIsNone(_epoch_seconds(MissingTimestampLike()))
        self.assertIsNone(_epoch_seconds(math.nan))
        self.assertIsNone(_epoch_seconds(math.inf))


if __name__ == "__main__":
    unittest.main()
