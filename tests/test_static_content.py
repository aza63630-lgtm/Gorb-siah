"""Regression checks for the checked-in DevTools summary artifacts."""

from html.parser import HTMLParser
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "devtools_batchexecute_summary.html"
TRANSCRIPT = ROOT / "devtools_what_can_you_help_me_with.md"
SENSITIVE_MARKERS = (
    "f.sid=",
    "authuser=",
    "photos.google.com/",
    "usercontent.google.com",
    "SAPISID",
)


class DocumentParser(HTMLParser):
    """Record the opening HTML tag so document metadata can be asserted."""

    def __init__(self):
        super().__init__()
        self.html_attributes = None

    def handle_starttag(self, tag, attrs):
        if tag == "html" and self.html_attributes is None:
            self.html_attributes = dict(attrs)


class StaticContentTests(unittest.TestCase):
    def test_summary_has_persian_right_to_left_document_metadata(self):
        parser = DocumentParser()
        parser.feed(SUMMARY.read_text(encoding="utf-8"))

        self.assertEqual({"lang": "fa", "dir": "rtl"}, parser.html_attributes)

    def test_summary_describes_the_response_headers_consistently(self):
        summary = SUMMARY.read_text(encoding="utf-8")

        self.assertIn("content-type: application/json; charset=utf-8", summary)
        self.assertIn("content-encoding: br", summary)
        self.assertIn("محتوای decode‌شده JSON", summary)
        self.assertNotIn("پاسخ باینری/فشرده‌شده", summary)

    def test_transcript_uses_the_canonical_filename_and_spelling(self):
        transcript = TRANSCRIPT.read_text(encoding="utf-8")

        self.assertTrue(TRANSCRIPT.is_file())
        self.assertFalse((ROOT / "devtools_what_can_you_help_me_with.md 2950").exists())
        self.assertIn("## Breakdown", transcript)
        self.assertNotIn("Breakdwon", transcript)

    def test_checked_in_artifacts_do_not_contain_sensitive_capture_data(self):
        contents = "\n".join(
            path.read_text(encoding="utf-8") for path in (SUMMARY, TRANSCRIPT)
        )

        for marker in SENSITIVE_MARKERS:
            with self.subTest(marker=marker):
                self.assertNotIn(marker, contents)


if __name__ == "__main__":
    unittest.main()
