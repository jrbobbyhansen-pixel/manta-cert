"""Tests for manta-cert."""

from manta_cert import format_date, days_remaining


def test_format_date():
    result = format_date("Jan 15 10:30:00 2026 GMT")
    assert "2026-01-15" in result


def test_days_remaining_future():
    # A date far in the future should return positive days
    d = days_remaining("Jan 15 10:30:00 2030 GMT")
    assert d > 0


def test_days_remaining_past():
    # A date in the past should return negative days
    d = days_remaining("Jan 15 10:30:00 2020 GMT")
    assert d < 0
