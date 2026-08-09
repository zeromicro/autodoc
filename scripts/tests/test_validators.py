import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import check_docs
import check_links


class DocumentationValidatorTests(unittest.TestCase):
    def test_frontmatter_value_rejects_empty_values(self):
        frontmatter = "title: Example\ndescription: null\nsidebar:\n  order: 1"
        self.assertEqual(check_docs.frontmatter_value(frontmatter, "title"), "Example")
        self.assertEqual(check_docs.frontmatter_value(frontmatter, "description"), "null")

    def test_unclosed_fence_reports_opening_line(self):
        self.assertEqual(check_docs.unclosed_fence_line("text\n```go\npackage main\n"), 2)
        self.assertIsNone(check_docs.unclosed_fence_line("```go\npackage main\n```\n"))

    def test_release_versions_are_extracted(self):
        content = "## v1.2.3 – 2026-01-01\n\n## Latest Releases\n"
        self.assertEqual(check_docs.release_versions(content), {"v1.2.3"})

    def test_heading_ids_match_repeated_markdown_headings(self):
        markdown = "---\ntitle: Test\n---\n\n## Hello, World!\n\n## Hello, World!\n"
        self.assertEqual(check_links.heading_ids(markdown), {"hello-world", "hello-world-1"})

    def test_heading_ids_include_unicode_and_explicit_ids(self):
        markdown = "## 配置参考\n\n<div id=\"custom-anchor\"></div>\n"
        self.assertEqual(check_links.heading_ids(markdown), {"配置参考", "custom-anchor"})


if __name__ == "__main__":
    unittest.main()
