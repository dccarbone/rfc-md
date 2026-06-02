import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_rfc.py"
SPEC = importlib.util.spec_from_file_location("validate_rfc", MODULE_PATH)
validate_rfc = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_rfc)


class ValidateRfcTest(unittest.TestCase):
    def test_frontmatter_uses_capitalized_title_field(self):
        body = """---
Title: RFC - IAM Authoritative Source
review_status: draft
design_review:
comments_until:
review_until:
required_approvers: []
---

# RFC - IAM Authoritative Source
"""

        data, markdown = validate_rfc.split_frontmatter(body)
        validate_rfc.validate_h1(markdown, data.get("Title"))
        approvers = validate_rfc.validate_status_requirements(data, markdown)

        self.assertEqual(approvers, [])


if __name__ == "__main__":
    unittest.main()
