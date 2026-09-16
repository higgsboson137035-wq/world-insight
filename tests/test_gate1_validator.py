import unittest

from scripts.gate1_validator import validate_gate1_output


DATE = "2026-09-15"
VERSION = "phase1-0.2"
SHA = "a" * 64


def candidate_block(number: int, *, missing=None, duplicate=None):
    fields = {
        "Brief item": "Brief item text",
        "Initial Question": "Initial question text",
        "Reader Transformation BEFORE": "Before text",
        "Reader Transformation AFTER": "After text",
        "Structural Question": "Structural question text",
        "Insight Shift": "Insight shift text",
        "Take One Thing": "Take one thing text",
        "Human Context / Responsibility conflict": "Context text",
        "Decision Space": "Decision space text",
        "Evidence feasibility": "Evidence feasibility text",
        "Overlap / Independence": "Overlap text",
        "Provisional evaluation": "Provisional evaluation text",
    }
    if missing:
        fields.pop(missing)
    lines = [f"### Candidate {number}"]
    for field, value in fields.items():
        lines.append(f"{field}: {value}")
        if field == duplicate:
            lines.append(f"{field}: duplicate")
    return "\n".join(lines)


def package(count=0, *, outcome=None, recommendation=None, follow_up=None, blocks=None):
    if outcome is None:
        outcome = "NO_PUBLISH_CANDIDATE" if count == 0 else "CANDIDATES_FOR_HUMAN_REVIEW"
    if recommendation is None:
        recommendation = "NONE" if count == 0 else "Candidate 1"
    if follow_up is None:
        follow_up = "NONE" if count == 0 else "SOURCE_VERIFICATION_REQUIRED"
    blocks = blocks if blocks is not None else [candidate_block(number) for number in range(1, count + 1)]
    sections = [
        "## World Brief Confirmation",
        "## Candidate List",
        *blocks,
        "## Candidate Comparison",
        "## Recommended Candidate",
        "## Candidate Light Evaluations",
        "## Confirmed",
        "## Claims",
        "## Analysis",
        "## Hypothetical",
        "## Unknown",
        "## Evidence Boundary",
        "## Candidate Discovery Convergence Observation",
        "## Measurement",
        "Machine elapsed: 1.0",
        "Human active time: UNKNOWN",
        "Rework count: 0",
    ]
    metadata = [
        f"Run-Date: {DATE}",
        "Run-Start: 2026-09-15T07:14:22+09:00",
        "Brief-Readiness: READY",
        f"Candidate-Count: {count}",
        f"Daily-Candidate-Outcome: {outcome}",
        f"Recommended-Candidate: {recommendation}",
        "Source-Verification: NOT_STARTED",
        f"Gate-1-Follow-Up: {follow_up}",
        "Human-Decision: PENDING",
        f"Prompt-Version: {VERSION}",
        f"Prompt-SHA256: {SHA}",
    ]
    return "\n".join(metadata + sections)


class Gate1ValidatorTests(unittest.TestCase):
    def validate(self, raw):
        return validate_gate1_output(
            raw,
            requested_date=DATE,
            prompt_version=VERSION,
            prompt_sha256=SHA,
        )

    def assert_malformed(self, raw, code):
        result = self.validate(raw)
        self.assertFalse(result.valid)
        self.assertEqual(result.status, "FAIL")
        self.assertEqual(result.failure_kind, "MALFORMED_GATE1")
        self.assertIn(code, result.errors)

    def test_valid_candidate_counts_zero_to_three(self):
        for count in range(4):
            with self.subTest(count=count):
                result = self.validate(package(count))
                self.assertTrue(result.valid, result.errors)
                self.assertEqual(result.failure_kind, "NONE")

    def test_candidate_heading_provides_identity_without_candidate_field(self):
        raw = package(1)
        self.assertIn("### Candidate 1", raw)
        self.assertNotIn("Candidate: Candidate 1", raw.splitlines())
        result = self.validate(raw)
        self.assertTrue(result.valid, result.errors)

    def test_empty_raw_output(self):
        self.assert_malformed("", "EMPTY_RAW_OUTPUT")

    def test_missing_metadata(self):
        self.assert_malformed(package().replace("Human-Decision: PENDING\n", ""), "MISSING_METADATA:Human-Decision")

    def test_duplicate_metadata(self):
        self.assert_malformed(package() + "\nHuman-Decision: PENDING", "DUPLICATE_METADATA:Human-Decision")

    def test_invalid_candidate_count(self):
        self.assert_malformed(package().replace("Candidate-Count: 0", "Candidate-Count: 4"), "INVALID_CANDIDATE_COUNT")

    def test_requested_date_mismatch(self):
        self.assert_malformed(package().replace(f"Run-Date: {DATE}", "Run-Date: 2026-09-14"), "RUN_DATE_MISMATCH")

    def test_invalid_run_start(self):
        self.assert_malformed(package().replace("Run-Start: 2026-09-15T07:14:22+09:00", "Run-Start: tomorrow"), "INVALID_RUN_START")

    def test_brief_readiness_mismatch(self):
        self.assert_malformed(package().replace("Brief-Readiness: READY", "Brief-Readiness: BRIEF_NOT_READY"), "INVALID_BRIEF_READINESS")

    def test_prompt_version_mismatch(self):
        self.assert_malformed(package().replace(f"Prompt-Version: {VERSION}", "Prompt-Version: phase1-0.1"), "PROMPT_VERSION_MISMATCH")

    def test_prompt_sha_mismatch(self):
        self.assert_malformed(package().replace(f"Prompt-SHA256: {SHA}", "Prompt-SHA256: b" * 64), "PROMPT_SHA256_MISMATCH")

    def test_source_verification_must_be_not_started(self):
        self.assert_malformed(package().replace("Source-Verification: NOT_STARTED", "Source-Verification: PASS"), "INVALID_SOURCE_VERIFICATION")

    def test_human_decision_must_be_pending(self):
        self.assert_malformed(package().replace("Human-Decision: PENDING", "Human-Decision: APPROVED"), "INVALID_HUMAN_DECISION")

    def test_missing_candidate_block(self):
        self.assert_malformed(package(1, blocks=[]), "CANDIDATE_BLOCK_COUNT_MISMATCH")

    def test_extra_candidate_block(self):
        self.assert_malformed(package(1, blocks=[candidate_block(1), candidate_block(2)]), "CANDIDATE_BLOCK_COUNT_MISMATCH")

    def test_duplicate_candidate_block(self):
        self.assert_malformed(package(2, blocks=[candidate_block(1), candidate_block(1)]), "DUPLICATE_CANDIDATE_BLOCK")

    def test_numbering_gap(self):
        self.assert_malformed(package(2, blocks=[candidate_block(1), candidate_block(3)]), "CANDIDATE_BLOCK_NUMBERING_MISMATCH")

    def test_candidate_four(self):
        self.assert_malformed(package(1, blocks=[candidate_block(4)]), "INVALID_CANDIDATE_BLOCK_NUMBER")

    def test_required_candidate_field_missing(self):
        self.assert_malformed(package(1, blocks=[candidate_block(1, missing="Insight Shift")]), "MISSING_CANDIDATE_FIELD:Candidate 1:Insight Shift")

    def test_required_candidate_field_duplicate(self):
        self.assert_malformed(package(1, blocks=[candidate_block(1, duplicate="Decision Space")]), "DUPLICATE_CANDIDATE_FIELD:Candidate 1:Decision Space")

    def test_zero_candidate_wrong_outcome(self):
        self.assert_malformed(package(outcome="CANDIDATES_FOR_HUMAN_REVIEW"), "ZERO_CANDIDATE_OUTCOME_MISMATCH")

    def test_zero_candidate_wrong_recommendation(self):
        self.assert_malformed(package(recommendation="Candidate 1"), "ZERO_CANDIDATE_RECOMMENDATION_MISMATCH")

    def test_positive_candidate_wrong_outcome(self):
        self.assert_malformed(package(1, outcome="NO_PUBLISH_CANDIDATE"), "POSITIVE_CANDIDATE_OUTCOME_MISMATCH")

    def test_recommendation_references_missing_candidate(self):
        self.assert_malformed(package(1, recommendation="Candidate 2"), "RECOMMENDED_CANDIDATE_NOT_PRESENT")

    def test_wrong_follow_up(self):
        self.assert_malformed(package(1, follow_up="NONE"), "POSITIVE_CANDIDATE_FOLLOW_UP_MISMATCH")

    def test_missing_required_section(self):
        self.assert_malformed(package().replace("## Evidence Boundary\n", ""), "MISSING_SECTION:Evidence Boundary")

    def test_duplicate_required_section(self):
        self.assert_malformed(package() + "\n## Measurement", "DUPLICATE_SECTION:Measurement")

    def test_human_active_time_must_be_unknown(self):
        self.assert_malformed(package().replace("Human active time: UNKNOWN", "Human active time: 1 minute"), "INVALID_HUMAN_ACTIVE_TIME")

    def test_rework_count_must_be_zero(self):
        self.assert_malformed(package().replace("Rework count: 0", "Rework count: 1"), "INVALID_REWORK_COUNT")

    def test_ordinary_boundary_word_mentions_are_not_boundary_violations(self):
        raw = package().replace("## Analysis", "## Analysis\nGit, Publish, and Source Verification are mentioned as terms.")
        result = self.validate(raw)
        self.assertTrue(result.valid, result.errors)
        self.assertNotEqual(result.failure_kind, "BOUNDARY_VIOLATION")

    def test_forbidden_human_approved_no_publish_is_structural_failure(self):
        self.assert_malformed(package() + "\nNO_PUBLISH / HUMAN APPROVED", "FORBIDDEN_HUMAN_APPROVED_NO_PUBLISH")

    def test_no_files_or_network_are_needed(self):
        result = self.validate(package())
        self.assertTrue(result.valid)
        self.assertNotIn("raw_output", result.as_dict())


if __name__ == "__main__":
    unittest.main()
