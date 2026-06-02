"""Unit tests for utils/logic.py.

All IMAP and SMTP calls are mocked so no real server is needed.
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock, call
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import message_from_bytes

# Allow importing from the top-level utils package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.logic import SendEmail, ReceiveEmail  # noqa: E402


# ---------------------------------------------------------------------------
# SendEmail tests
# ---------------------------------------------------------------------------


class TestSendEmailCreateMessage(unittest.TestCase):
    def _make_sender(self, **kwargs):
        return SendEmail("sender@example.com", "secret", **kwargs)

    def test_create_message_sets_fields(self):
        sender = self._make_sender()
        sender.create_message("Hello", "Body text", "recipient@example.com")
        self.assertEqual(sender.msg["Subject"], "Hello")
        self.assertEqual(sender.msg["From"], "sender@example.com")
        self.assertEqual(sender.msg["To"], "recipient@example.com")

    def test_create_message_stores_recipient(self):
        sender = self._make_sender()
        sender.create_message("Subj", "Body", "to@example.com")
        self.assertEqual(sender.recipientAddress, "to@example.com")

    def test_create_reply_adds_re_prefix(self):
        original = MIMEText("original body")
        original["Subject"] = "Original subject"
        original["From"] = "alice@example.com"
        original["Message-ID"] = "<abc123@example.com>"

        sender = self._make_sender()
        sender.create_reply(original, "My reply")
        self.assertEqual(sender.msg["Subject"], "Re: Original subject")
        self.assertEqual(sender.recipientAddress, "alice@example.com")

    def test_create_reply_no_double_re(self):
        original = MIMEText("body")
        original["Subject"] = "Re: Already a reply"
        original["From"] = "bob@example.com"
        original["Message-ID"] = "<xyz@example.com>"

        sender = self._make_sender()
        sender.create_reply(original, "Replying again")
        self.assertEqual(sender.msg["Subject"], "Re: Already a reply")

    def test_create_forward_adds_fwd_prefix(self):
        original = MIMEText("original")
        original["Subject"] = "News"
        original["From"] = "carol@example.com"
        original["Message-ID"] = "<fwd123@example.com>"

        sender = self._make_sender()
        sender.create_forward(original, "FYI", "dave@example.com")
        self.assertEqual(sender.msg["Subject"], "Fwd: News")
        self.assertEqual(sender.recipientAddress, "dave@example.com")


class TestSendEmailSendMail(unittest.TestCase):
    def _prepared_sender(self, ssl=True, port=465, smtp_server="smtp.gmail.com"):
        sender = SendEmail(
            "sender@example.com",
            "secret",
            smtpServer=smtp_server,
            smtpPort=port,
            smtpSsl=ssl,
        )
        sender.create_message("Subj", "Body", "recipient@example.com")
        return sender

    @patch("utils.logic.smtplib.SMTP_SSL")
    def test_send_mail_uses_ssl(self, mock_smtp_ssl):
        mock_server = MagicMock()
        mock_smtp_ssl.return_value.__enter__ = lambda s: mock_server
        mock_smtp_ssl.return_value.__exit__ = MagicMock(return_value=False)

        sender = self._prepared_sender(ssl=True)
        sender.send_mail()
        mock_smtp_ssl.assert_called_once()
        mock_server.login.assert_called_once_with("sender@example.com", "secret")

    @patch("utils.logic.smtplib.SMTP")
    def test_send_mail_uses_starttls(self, mock_smtp):
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__ = lambda s: mock_server
        mock_smtp.return_value.__exit__ = MagicMock(return_value=False)

        sender = self._prepared_sender(ssl=False, port=587, smtp_server="smtp.office365.com")
        sender.send_mail()
        mock_smtp.assert_called_once()
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with("sender@example.com", "secret")


# ---------------------------------------------------------------------------
# ReceiveEmail tests
# ---------------------------------------------------------------------------


class TestReceiveEmailDecodeSubject(unittest.TestCase):
    def _make_receiver(self):
        with patch("utils.logic.imaplib.IMAP4_SSL") as mock_imap:
            mock_imap.return_value.login.return_value = ("OK", [])
            return ReceiveEmail("user@example.com", "pass")

    def test_plain_ascii_subject(self):
        r = self._make_receiver()
        self.assertEqual(r.decode_subject("Hello World"), "Hello World")

    def test_empty_subject(self):
        r = self._make_receiver()
        self.assertEqual(r.decode_subject(""), "")

    def test_base64_encoded_subject(self):
        r = self._make_receiver()
        # "Cześć" encoded as UTF-8 base64
        encoded = "=?utf-8?b?Q3plxZvEhw==?="
        result = r.decode_subject(encoded)
        self.assertEqual(result, "Cze\u015b\u0107")

    def test_quoted_printable_subject(self):
        r = self._make_receiver()
        # "Héllo" encoded as ISO-8859-1 QP
        encoded = "=?iso-8859-1?q?H=E9llo?="
        result = r.decode_subject(encoded)
        self.assertIn("H", result)
        self.assertIn("llo", result)


class TestReceiveEmailGetFolders(unittest.TestCase):
    def _make_receiver_with_folders(self, folder_lines):
        with patch("utils.logic.imaplib.IMAP4_SSL") as mock_imap_cls:
            mock_imap = MagicMock()
            mock_imap.login.return_value = ("OK", [])
            mock_imap.list.return_value = ("OK", folder_lines)
            mock_imap_cls.return_value = mock_imap
            r = ReceiveEmail("user@example.com", "pass")
            r.imapSSL = mock_imap
            return r

    def test_get_folders_returns_names(self):
        lines = [
            b'(\\HasNoChildren) "/" INBOX',
            b'(\\HasNoChildren) "/" "Sent"',
            b'(\\HasNoChildren) "/" "Trash"',
        ]
        r = self._make_receiver_with_folders(lines)
        folders = r.get_folders()
        self.assertIn("INBOX", folders)
        self.assertIn("Sent", folders)
        self.assertIn("Trash", folders)


class TestReceiveEmailMailboxPrinter(unittest.TestCase):
    def _build_raw_email(self, subject="Test", from_="sender@example.com"):
        msg = MIMEText("Hello body")
        msg["Subject"] = subject
        msg["From"] = from_
        return msg.as_bytes()

    def _make_receiver(self):
        with patch("utils.logic.imaplib.IMAP4_SSL") as mock_imap_cls:
            mock_imap = MagicMock()
            mock_imap.login.return_value = ("OK", [])
            mock_imap_cls.return_value = mock_imap
            r = ReceiveEmail("user@example.com", "pass")
            r.imapSSL = mock_imap
            return r

    def test_mailbox_printer_returns_newest_first(self):
        r = self._make_receiver()
        uids = [b"1", b"2", b"3"]
        r.imapSSL.search.return_value = ("OK", [b" ".join(uids)])
        r.imapSSL.select.return_value = ("OK", [b"3"])

        raw_emails = {
            b"1": self._build_raw_email("Email 1"),
            b"2": self._build_raw_email("Email 2"),
            b"3": self._build_raw_email("Email 3"),
        }

        def fetch_side_effect(uid, spec):
            return ("OK", [(b"data", raw_emails[uid])])

        r.imapSSL.fetch.side_effect = fetch_side_effect

        result = r.mailbox_printer("INBOX")
        subjects = [msg["Subject"] for _uid, msg in result]
        self.assertEqual(subjects[0], "Email 3")
        self.assertEqual(subjects[-1], "Email 1")

    def test_mailbox_printer_respects_limit(self):
        r = self._make_receiver()
        uids = [str(i).encode() for i in range(1, 11)]  # 10 emails
        r.imapSSL.search.return_value = ("OK", [b" ".join(uids)])
        r.imapSSL.select.return_value = ("OK", [b"10"])
        r.imapSSL.fetch.return_value = ("OK", [(b"data", self._build_raw_email())])

        result = r.mailbox_printer("INBOX", limit=5)
        self.assertLessEqual(len(result), 5)


class TestReceiveEmailActions(unittest.TestCase):
    def _make_receiver(self):
        with patch("utils.logic.imaplib.IMAP4_SSL") as mock_imap_cls:
            mock_imap = MagicMock()
            mock_imap.login.return_value = ("OK", [])
            mock_imap_cls.return_value = mock_imap
            r = ReceiveEmail("user@example.com", "pass")
            r.imapSSL = mock_imap
            return r

    def test_delete_message_flags_and_expunges(self):
        r = self._make_receiver()
        r.delete_message("INBOX", b"42")
        r.imapSSL.store.assert_called_once_with(b"42", "+FLAGS", "\\Deleted")
        r.imapSSL.expunge.assert_called_once()

    def test_mark_read_sets_seen_flag(self):
        r = self._make_receiver()
        r.mark_read("INBOX", b"7")
        r.imapSSL.store.assert_called_once_with(b"7", "+FLAGS", "\\Seen")

    def test_mark_unread_removes_seen_flag(self):
        r = self._make_receiver()
        r.mark_unread("INBOX", b"7")
        r.imapSSL.store.assert_called_once_with(b"7", "-FLAGS", "\\Seen")


if __name__ == "__main__":
    unittest.main()
