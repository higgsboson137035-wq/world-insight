import unittest
from pathlib import Path


PROMPT_PATH = Path(__file__).parents[1] / "prompts" / "daily_run_phase1.md"


class PromptContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prompt = PROMPT_PATH.read_text(encoding="utf-8")

    def test_version_and_placeholder_contract(self):
        self.assertEqual(self.prompt.count("Prompt-Version: phase1-0.4"), 2)
        self.assertEqual(self.prompt.count("Prompt-SHA256: INJECTED_BY_ORCHESTRATOR"), 1)

    def test_metadata_first_and_self_check_contract(self):
        self.assertIn("Candidate-Countを決定した後、Candidate Listや`## Recommended Candidate` sectionより先に、Required Metadata blockを完成させてください", self.prompt)
        self.assertIn("Required Metadata block内の`Recommended-Candidate` metadata lineは必須であり、省略してはいけません", self.prompt)
        self.assertIn("Required Metadata block内の各必須metadata lineが正しい形式で存在することを生成側で確認", self.prompt)
        self.assertIn("このself-checkはvalidatorの代替ではありません", self.prompt)
        self.assertIn("chain-of-thought、内部推論、self-checkの思考過程は出力しない", self.prompt)

    def test_considered_candidates_are_not_formal_blocks(self):
        self.assertIn("considered candidates", self.prompt)
        self.assertIn("formal Candidate blockではありません", self.prompt)
        self.assertIn("Candidate-Countにも含めないでください", self.prompt)
        self.assertIn("弱いCandidateをformal Candidateとして推薦してはいけません", self.prompt)

    def test_zero_formal_candidate_semantics(self):
        self.assertIn("Candidate-Countが0の場合はformal Candidate blockを1件も出力しない", self.prompt)
        self.assertIn("Candidate-Count: 0\nDaily-Candidate-Outcome: NO_PUBLISH_CANDIDATE\nRecommended-Candidate: NONE\nGate-1-Follow-Up: NONE", self.prompt)
        self.assertIn("Daily-Candidate-Outcome: NO_PUBLISH_CANDIDATE", self.prompt)
        self.assertIn("Recommended-Candidate: NONE", self.prompt)
        self.assertIn("Gate-1-Follow-Up: NONE", self.prompt)

    def test_positive_formal_candidate_semantics(self):
        self.assertIn("Candidate-Countが1〜3の場合", self.prompt)
        self.assertIn("Candidate-Count: <actual count>\nDaily-Candidate-Outcome: CANDIDATES_FOR_HUMAN_REVIEW\nRecommended-Candidate: Candidate <selected formal candidate number>\nGate-1-Follow-Up: SOURCE_VERIFICATION_REQUIRED", self.prompt)
        self.assertIn("Daily-Candidate-Outcome: CANDIDATES_FOR_HUMAN_REVIEW", self.prompt)
        self.assertIn("<selected formal candidate number>`は、実在するformal CandidateからLLMが選択する番号", self.prompt)
        self.assertIn("Candidate 1を機械的に推薦してはいけません", self.prompt)
        self.assertIn("Gate-1-Follow-Up: SOURCE_VERIFICATION_REQUIRED", self.prompt)

    def test_recommended_candidate_metadata_is_separate_from_section(self):
        self.assertIn("Required Metadata内の`Recommended-Candidate: ...` lineと`## Recommended Candidate` sectionは別物", self.prompt)
        self.assertIn("両方を必ず出力し", self.prompt)
        self.assertIn("section見出しやsection本文でmetadata lineを代用してはいけません", self.prompt)

    def test_comparison_and_light_evaluations_use_formal_candidates(self):
        self.assertIn("formal candidatesなし", self.prompt)
        self.assertIn("Candidate Light EvaluationsではGate-1-worthy candidateなし", self.prompt)
        self.assertIn("formal CandidateだけをCandidate ComparisonとCandidate Light Evaluationsの比較対象", self.prompt)


if __name__ == "__main__":
    unittest.main()
