import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"


def read(path):
    return path.read_text(encoding="utf-8")


def markdown_files():
    files = [ROOT / "README.md", ROOT / "AGENTS.md"]
    docs = sorted((ROOT / "docs").glob("*.md")) if (ROOT / "docs").exists() else []
    return [p for p in files + docs if p.exists()]


def all_markdown_text():
    return "\n\n".join(read(path) for path in markdown_files())


def slugify(heading):
    heading = heading.strip().lower()
    heading = re.sub(r"[^\w\s-]", "", heading)
    heading = re.sub(r"\s+", "-", heading)
    return heading


class DocumentContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.readme = read(README)
        cls.all_text = all_markdown_text()

    def assert_contains(self, *terms):
        text = self.all_text.lower()
        for term in terms:
            self.assertIn(term.lower(), text)

    def test_readme_exists(self):
        self.assertTrue(README.exists())

    def test_no_ai_vendor_dependency_claims(self):
        forbidden = [
            r"requires\s+(claude|codex|copilot|cursor|gemini|devin)",
            r"must\s+use\s+(claude|codex|copilot|cursor|gemini|devin)",
        ]
        for pattern in forbidden:
            self.assertIsNone(re.search(pattern, self.all_text, re.IGNORECASE))

    def test_model_agnostic_language_present(self):
        self.assert_contains("model-agnostic", "tool-agnostic", "model-neutral")

    def test_orchestrator_role_defined(self):
        self.assert_contains("Orchestrator", "decomposition", "verification", "approval")

    def test_worker_role_defined(self):
        self.assert_contains("Worker", "bounded execution labor")

    def test_orchestrator_worker_boundary_present(self):
        self.assert_contains("not security boundaries", "protocol roles")

    def test_worker_cannot_approve_own_work(self):
        self.assert_contains("MUST NOT approve its own work")

    def test_delegation_gate_section_exists(self):
        self.assert_contains("Delegation Decision Procedure")

    def test_gate_has_independence_axis(self):
        self.assert_contains("Gate 1: Independence", "shared mutable state")

    def test_gate_has_oracle_completeness_axis(self):
        self.assert_contains("Gate 2: Oracle Completeness")

    def test_gate_has_scale_cost_axis(self):
        self.assert_contains("Gate 3: Scale and Risk", "token/cost ceiling")

    def test_gate_requires_all_axes(self):
        self.assert_contains("Delegate only if all three gates pass")

    def test_failed_gate_fallback_defined(self):
        self.assert_contains("Do not delegate", "upgrade the oracle")

    def test_oracle_first_verification_present(self):
        self.assert_contains("machine oracle first", "LLM judgment second")

    def test_oracle_grades_present(self):
        self.assert_contains("Full", "Strong partial", "Weak partial", "None")

    def test_acceptance_criteria_requires_commands(self):
        self.assert_contains("acceptance_criteria", "oracle", "commands")

    def test_brief_schema_required_fields_present(self):
        for field in [
            "objective",
            "acceptance_criteria",
            "oracle",
            "out_of_scope",
            "relevant_context",
            "evidence_required",
        ]:
            self.assertIn(field, self.readme)

    def test_machine_readable_brief_present(self):
        self.assertRegex(self.readme, r"```(yaml|json|toml)\n")

    def test_worker_claim_evidence_separation(self):
        self.assert_contains("claim", "evidence", "Claims alone do not count")

    def test_final_oracle_output_required(self):
        self.assert_contains("command, exit code", "output excerpt")

    def test_bulky_artifact_path_hash_rule_present(self):
        for term in ["artifact path", "hash", "summary"]:
            self.assertIn(term, self.readme)

    def test_oracle_incomplete_tasks_are_not_delegated(self):
        self.assert_contains("If the oracle is incomplete", "shrink the task")

    def test_token_cost_warning_present(self):
        self.assert_contains("do not guarantee token savings", "token/cost ceiling")

    def test_redelegation_limit_present(self):
        self.assert_contains("Re-delegate at most twice")

    def test_loop_budget_caps_present(self):
        self.assert_contains("step caps", "token-budget", "loop detectors")

    def test_worker_taxonomy_section_or_list_present(self):
        self.assert_contains("Worker Taxonomy", "Search Worker", "Patch Worker", "Test Worker")

    def test_taxonomy_has_safe_mechanical_workers(self):
        self.assert_contains("mechanical patches", "Fixture Worker", "Cleanup Worker")

    def test_taxonomy_has_forbidden_workers(self):
        self.assert_contains("state machines", "concurrency", "timing")

    def test_high_risk_forbidden_work_present(self):
        for term in ["auth", "payment", "production", "data deletion"]:
            self.assertIn(term, self.readme)

    def test_local_llm_constraints_present(self):
        self.assert_contains("Low-Tier and Local LLM Policy", "local LLM")

    def test_local_llm_does_not_override_oracle(self):
        self.assert_contains("lower model tier only when oracle strength rises")

    def test_security_safeguards_present(self):
        self.assert_contains("secrets", "sandbox", "permissions", "unrestricted network")

    def test_exclusive_file_ownership_present(self):
        self.assert_contains("exclusive file ownership", "concurrent Workers touch the same file")

    def test_no_secret_exfiltration_rule_present(self):
        self.assert_contains("secret access: denied", "redact secrets")

    def test_prompt_injection_threat_present(self):
        self.assert_contains("setup scripts", "DNS calls", "network behavior")

    def test_evidence_references_section_exists(self):
        self.assertTrue((ROOT / "docs" / "evidence.md").exists())
        self.assert_contains("Evidence and References")

    def test_references_are_concrete(self):
        links = re.findall(r"https?://[^\s)]+", self.all_text)
        self.assertGreaterEqual(len(links), 8)

    def test_evidence_has_checked_date_and_secondary_source_limit(self):
        evidence = read(ROOT / "docs" / "evidence.md")
        self.assertIn("Checked as of 2026-07-03", evidence)
        self.assertIn("Community sources are used only as secondary signals", evidence)
        self.assertIn("MUST NOT be the sole support", evidence)

    def test_evidence_primary_rows_have_urls(self):
        evidence = read(ROOT / "docs" / "evidence.md")
        rows = [line for line in evidence.splitlines() if line.startswith("| ") and " | " in line]
        data_rows = [line for line in rows if not line.startswith("| Claim") and not line.startswith("|---")]
        for row in data_rows:
            cells = [cell.strip() for cell in row.strip("|").split("|")]
            self.assertGreaterEqual(len(cells), 4)
            primary = cells[1]
            self.assertIn("http", primary, row)

    def test_multi_agent_grill_protocol_present(self):
        self.assert_contains("Multi-Agent Grill Protocol", "Grill Worker", "blocking objections")

    def test_test_matrix_has_at_least_25_cases(self):
        matrix = read(ROOT / "docs" / "test-matrix.md")
        cases = re.findall(r"\bTC-\d{2}\b", matrix)
        self.assertGreaterEqual(len(set(cases)), 25)

    def test_running_tests_command_documented(self):
        self.assertIn("python -m unittest discover -s tests", self.readme)
        self.assertIn("python -m unittest discover -s tests", read(ROOT / "docs" / "test-matrix.md"))

    def test_markdown_headings_ordered(self):
        for path in markdown_files():
            levels = []
            for line in read(path).splitlines():
                match = re.match(r"^(#{1,6})\s+", line)
                if match:
                    levels.append(len(match.group(1)))
            for prev, current in zip(levels, levels[1:]):
                self.assertLessEqual(current - prev, 1, f"heading jump in {path}")

    def test_no_unfinished_markers(self):
        forbidden = ["TODO", "TBD", "FIXME", "<placeholder>"]
        for marker in forbidden:
            self.assertNotIn(marker, self.all_text)

    def test_no_mojibake_or_replacement_chars(self):
        self.assertNotIn("\ufffd", self.all_text)
        self.assertIsNone(re.search(r"\?\?(?!\?)", self.all_text))

    def test_internal_file_links_resolve(self):
        for path in markdown_files():
            text = read(path)
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                if target.startswith("http") or target.startswith("#"):
                    continue
                if "#" in target:
                    target_path, _anchor = target.split("#", 1)
                else:
                    target_path = target
                resolved = (path.parent / target_path).resolve()
                self.assertTrue(resolved.exists(), f"{path} links to missing {target}")

    def test_expected_doc_set_present(self):
        expected = [
            ROOT / "README.md",
            ROOT / "AGENTS.md",
            ROOT / "docs" / "evidence.md",
            ROOT / "docs" / "low-tier-local-workers.md",
            ROOT / "docs" / "test-matrix.md",
            ROOT / "tests" / "test_document_contract.py",
        ]
        for path in expected:
            self.assertTrue(path.exists(), str(path))


if __name__ == "__main__":
    unittest.main()
