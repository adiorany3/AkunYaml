from ai_adblock_telemetry import build_report


def test_false_positive_candidates_require_more_allowed_than_blocked():
    events = [
        {"domain": "ads.example.com", "outcome": "allowed"},
        {"domain": "ads.example.com", "outcome": "allowed"},
        {"domain": "ads.example.com", "outcome": "allowed"},
        {"domain": "ads.example.com", "outcome": "blocked"},
        {"domain": "safe.example.com", "outcome": "allowed"},
    ]
    report = build_report(events)
    assert report["events"] == 5
    assert report["telemetry_state"] == "observed"
    assert report["confidence_ceiling"] == 1.0
    assert report["false_positive_candidates"] == [
        {"domain": "ads.example.com", "allowed": 3, "blocked": 1}
    ]


def test_missing_telemetry_never_claims_false_positive():
    report = build_report([])
    assert report["telemetry_state"] == "missing"
    assert report["confidence_ceiling"] == 0.0
    assert report["false_positive_candidates"] == []
