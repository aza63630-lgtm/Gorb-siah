"""Regression checks for the checked-in DevTools summary artifacts."""

from html.parser import HTMLParser
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
FIRESTORE_SUMMARY = ROOT / "devtools_firestore_listen_summary.html"
BATCH_SUMMARY = ROOT / "devtools_batchexecute_summary.html"
SUMMARIES = (FIRESTORE_SUMMARY, BATCH_SUMMARY)
BUILD_SCRIPT = ROOT / "scripts" / "build_site.py"
SENSITIVE_MARKERS = (
    "f.sid=",
    "authuser=",
    "photos.google.com/",
    "usercontent.google.com",
    "SAPISID",
    "lottosocial-",
    "DFCI-",
    "resumeToken\"",
    "CgkIhNPi5ruKlwM=",
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
    def test_build_script_creates_entrypoint_and_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            subprocess.run(
                [sys.executable, BUILD_SCRIPT, "--output", output],
                check=True,
                cwd=ROOT,
            )

            self.assertEqual(
                FIRESTORE_SUMMARY.read_text(encoding="utf-8"),
                (output / "index.html").read_text(encoding="utf-8"),
            )
            self.assertEqual(
                BATCH_SUMMARY.read_text(encoding="utf-8"),
                (output / BATCH_SUMMARY.name).read_text(encoding="utf-8"),
            )

    def test_summaries_have_persian_right_to_left_document_metadata(self):
        for summary in SUMMARIES:
            with self.subTest(summary=summary.name):
                parser = DocumentParser()
                parser.feed(summary.read_text(encoding="utf-8"))
                self.assertEqual({"lang": "fa", "dir": "rtl"}, parser.html_attributes)

    def test_batch_summary_describes_response_headers_consistently(self):
        summary = BATCH_SUMMARY.read_text(encoding="utf-8")

        self.assertIn("content-type: application/json; charset=utf-8", summary)
        self.assertIn("content-encoding: br", summary)
        self.assertIn("محتوای decode‌شده JSON", summary)
        self.assertNotIn("پاسخ باینری/فشرده‌شده", summary)

    def test_firestore_summary_explains_listener_lifecycle(self):
        summary = FIRESTORE_SUMMARY.read_text(encoding="utf-8")

        for event in ("documentChange", "ADD", "CURRENT", "REMOVE", "noop"):
            with self.subTest(event=event):
                self.assertIn(event, summary)

    def test_summaries_do_not_contain_sensitive_capture_data(self):
        contents = "\n".join(
            summary.read_text(encoding="utf-8") for summary in SUMMARIES
        )

        for marker in SENSITIVE_MARKERS:
            with self.subTest(marker=marker):
                self.assertNotIn(marker, contents)


if __name__ == "__main__":
    unittest.main()
