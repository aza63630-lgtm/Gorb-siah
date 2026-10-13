"""Regression checks for the checked-in lottery summary artifacts."""

from html.parser import HTMLParser
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "index.html"
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

    def test_summary_is_only_a_lottery_ledger(self):
        summary = SUMMARY.read_text(encoding="utf-8")

        self.assertEqual(1, summary.count("<table>"))
        self.assertIn("سامری کامل اطلاعات بلیت‌ها", summary)
        self.assertNotIn("batchexecute", summary)
        self.assertNotIn("Response headers", summary)

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

    def test_lottery_summary_is_complete_without_inventing_values(self):
        summary = SUMMARY.read_text(encoding="utf-8")

        expected_fields = (
            "شناسه / سریال بلیت",
            "شناسهٔ قرعه‌کشی",
            "تاریخ و ساعت خرید بلیت",
            "تاریخ و ساعت قرعه‌کشی",
            "تاریخ اعلام نتیجه / برنده‌شدن",
            "تاریخ انقضا یا مهلت دریافت جایزه",
            "قیمت بلیت",
            "مبلغ جک‌پات",
            "مبلغ برد ناخالص",
            "مالیات / کسورات",
            "مبلغ برد خالص و ارز",
            "وضعیت و تاریخ پرداخت",
            "شماره‌های روی بلیت",
            "شماره‌های برنده",
            "توپ ویژه / بونوس",
            "ضریب",
            "تعداد تطبیق و ردهٔ برد",
        )
        for field in expected_fields:
            with self.subTest(field=field):
                self.assertIn(field, summary)

        self.assertIn("هیچ شناسه، تاریخ، مبلغ یا شمارهٔ توپی حدس زده نشده است", summary)

    def test_summary_launcher_is_available(self):
        launcher = ROOT / "open_summary.py"
        result = subprocess.run(
            [sys.executable, str(launcher), "--help"],
            capture_output=True,
            check=False,
            text=True,
        )

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("--no-browser", result.stdout)
        self.assertIn("--port", result.stdout)

    def test_pages_workflow_publishes_the_summary(self):
        workflow = (ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")

        self.assertIn("actions/upload-pages-artifact@v4", workflow)
        self.assertIn("actions/deploy-pages@v4", workflow)
        self.assertIn("pages: write", workflow)
        self.assertIn("id-token: write", workflow)


if __name__ == "__main__":
    unittest.main()
