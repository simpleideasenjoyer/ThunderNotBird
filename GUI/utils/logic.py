import smtplib
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import mimetypes
from email import encoders, message_from_bytes
from email.header import decode_header as _decode_header
import ssl
import imaplib

_FETCH_LIMIT = 100


class SendEmail:
    def __init__(
        self,
        senderAddress: str,
        senderPassword: str,
        smtpServer: str = "smtp.gmail.com",
        smtpPort: int = 465,
        smtpSsl: bool = True,
    ) -> None:
        self.context = ssl.create_default_context()
        self.senderAddress = senderAddress
        self.senderPassword = senderPassword
        self.smtpServer = smtpServer
        self.smtpPort = smtpPort
        self.smtpSsl = smtpSsl

    def create_message(self, subject: str, content: str, recipientAddress: str) -> None:
        self.recipientAddress = recipientAddress
        self.msg = MIMEMultipart()
        self.msg["Subject"] = subject
        self.msg["From"] = self.senderAddress
        self.msg["To"] = self.recipientAddress
        body = MIMEText(content, "plain")
        self.msg.attach(body)

    def create_reply(self, original_message, content: str) -> None:
        """Prepare a reply to an existing message."""
        self.recipientAddress = original_message.get("From", "")
        self.msg = MIMEMultipart()
        subject = original_message.get("Subject", "")
        if not subject.startswith("Re:"):
            subject = "Re: " + subject
        self.msg["Subject"] = subject
        self.msg["From"] = self.senderAddress
        self.msg["To"] = self.recipientAddress
        self.msg["In-Reply-To"] = original_message.get("Message-ID", "")
        self.msg["References"] = original_message.get("Message-ID", "")
        body = MIMEText(content, "plain")
        self.msg.attach(body)

    def create_forward(self, original_message, content: str, recipientAddress: str) -> None:
        """Prepare a forwarded message."""
        self.recipientAddress = recipientAddress
        self.msg = MIMEMultipart()
        subject = original_message.get("Subject", "")
        if not subject.startswith("Fwd:"):
            subject = "Fwd: " + subject
        self.msg["Subject"] = subject
        self.msg["From"] = self.senderAddress
        self.msg["To"] = self.recipientAddress
        body = MIMEText(content, "plain")
        self.msg.attach(body)

    def attachment(self, file_path: str) -> None:
        content_type = mimetypes.guess_type(file_path)[0]
        filename = basename(file_path)
        if content_type is None:
            content_type = "application/octet-stream"
        main_type, sub_type = content_type.split("/", 1)
        with open(file_path, "rb") as f:
            mime_base = MIMEBase(main_type, sub_type)
            mime_base.set_payload(f.read())
            encoders.encode_base64(mime_base)
            mime_base.add_header("Content-Disposition", "attachment", filename=filename)
            self.msg.attach(mime_base)

    def send_mail(self) -> None:
        if self.smtpSsl:
            with smtplib.SMTP_SSL(self.smtpServer, self.smtpPort, context=self.context) as server:
                server.login(self.senderAddress, self.senderPassword)
                server.sendmail(self.senderAddress, self.recipientAddress, self.msg.as_string())
        else:
            with smtplib.SMTP(self.smtpServer, self.smtpPort) as server:
                server.ehlo()
                server.starttls(context=self.context)
                server.login(self.senderAddress, self.senderPassword)
                server.sendmail(self.senderAddress, self.recipientAddress, self.msg.as_string())


class ReceiveEmail:
    def __init__(
        self,
        emailData: str,
        passwordData: str,
        imapServer: str = "imap.gmail.com",
        imapPort: int = 993,
        smtpServer: str = "smtp.gmail.com",
        smtpPort: int = 465,
        smtpSsl: bool = True,
    ) -> None:
        self.emailData = emailData
        self.passwordData = passwordData
        self.imapServer = imapServer
        self.imapPort = imapPort
        self.smtpServer = smtpServer
        self.smtpPort = smtpPort
        self.smtpSsl = smtpSsl
        self.imapSSL = imaplib.IMAP4_SSL(self.imapServer, self.imapPort)
        self.imapSSL.login(self.emailData, self.passwordData)

    def decode_subject(self, encoded_value: str) -> str:
        """Decode an RFC 2047 encoded email header value."""
        if not encoded_value:
            return ""
        parts = _decode_header(encoded_value)
        decoded = []
        for part, charset in parts:
            if isinstance(part, bytes):
                decoded.append(part.decode(charset or "utf-8", errors="replace"))
            else:
                decoded.append(part)
        return "".join(decoded)

    def get_folders(self) -> list[str]:
        """Return a list of mailbox folder names available on the server."""
        _, folder_list = self.imapSSL.list()
        folders = []
        for item in folder_list:
            if item:
                parts = item.decode().split(' "/" ')
                if len(parts) >= 2:
                    name = parts[-1].strip().strip('"')
                else:
                    name = item.decode().split()[-1].strip('"')
                folders.append(name)
        return folders

    def get_unread_uids(self, folderSelected: str) -> set:
        """Return a set of UIDs that are NOT marked as Seen in the given folder."""
        self.imapSSL.select(folderSelected)
        _, data = self.imapSSL.search(None, "UNSEEN")
        if data[0]:
            return set(data[0].split())
        return set()

    def mailbox_printer(self, folderSelected: str, limit: int = _FETCH_LIMIT):
        """Fetch the latest *limit* messages from *folderSelected*, newest first.

        Returns a list of (uid_bytes, email.message.Message) tuples.
        """
        self.imapSSL.select(folderSelected)
        _, searchReturn = self.imapSSL.search(None, "ALL")
        uid_list = searchReturn[0].split()
        uid_list = uid_list[-limit:]  # keep only the latest N
        result = []
        for uid in uid_list:
            _, data = self.imapSSL.fetch(uid, "(RFC822)")
            if data and data[0]:
                email_message = message_from_bytes(data[0][1])
                result.append((uid, email_message))
        result.reverse()  # newest first
        return result

    def delete_message(self, folderSelected: str, uid: bytes) -> None:
        """Flag a message as deleted and expunge it from *folderSelected*."""
        self.imapSSL.select(folderSelected)
        self.imapSSL.store(uid, "+FLAGS", "\\Deleted")
        self.imapSSL.expunge()

    def mark_read(self, folderSelected: str, uid: bytes) -> None:
        """Mark a message as Seen."""
        self.imapSSL.select(folderSelected)
        self.imapSSL.store(uid, "+FLAGS", "\\Seen")

    def mark_unread(self, folderSelected: str, uid: bytes) -> None:
        """Remove the Seen flag from a message."""
        self.imapSSL.select(folderSelected)
        self.imapSSL.store(uid, "-FLAGS", "\\Seen")
