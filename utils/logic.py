import smtplib
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
import mimetypes
from email import encoders, message_from_bytes
import ssl
import imaplib
from html import unescape
import base64
import quopri


class SendEmail:
    def __init__(
        self, senderAddress: str, senderPassword: str, recipientAddress: str
    ) -> object:
        self.context = ssl.create_default_context()
        self.senderAddress = senderAddress
        self.recipientAddress = recipientAddress
        self.senderPassword = senderPassword

    def create_message(self, subject: str, content: str) -> None:
        self.msg = MIMEMultipart()
        self.msg["Subject"] = subject
        self.msg["From"] = self.senderAddress
        self.msg["To"] = self.recipientAddress
        body = MIMEText(content, "plain")
        return self.msg.attach(body)

    def attachment(self, file_path):
        content_type = mimetypes.guess_type(file_path)[0]
        filename = basename(file_path)
        if content_type is None:
            content_type = "application/octet-stream"
        main_type, sub_type = content_type.split("/", 1)
        with open(file_path, "rb") as attachment:
            mime_base = MIMEBase(main_type, sub_type)
            mime_base.set_payload((attachment).read())
            encoders.encode_base64(mime_base)
            mime_base.add_header("Content-Disposition", "attachment", filename=filename)
            return self.msg.attach(mime_base)

    def send_mail(self):
        try:
            with smtplib.SMTP_SSL(
                "smtp.gmail.com", 465, context=self.context
            ) as server:
                server.login(self.senderAddress, self.senderPassword)
                server.sendmail(
                    self.senderAddress, self.recipientAddress, self.msg.as_string()
                )
                print("Email sent successfully!")
        except Exception as e:
            print("An error occurred while sending the email:", str(e))


class ReceiveEmail:
    def __init__(self, emailData, passwordData):
        self.emailData = emailData
        self.passwordData = passwordData
        self.imapServer = "imap.gmail.com"
        self.imapSSL = imaplib.IMAP4_SSL(self.imapServer)
        self.imapSSL.login(self.emailData, self.passwordData)

    def decode_subject(self, encoded_value):
        # Decoding subject(titles) for your printing mailbox method
        if "?" in encoded_value:
            try:
                self.decoded_parts = []
                parts = encoded_value.split("?")

                for i in range(1, len(parts), 4):
                    encoding = parts[i]
                    encoding_type = parts[i + 1]
                    encoded_text = parts[i + 2]
                    if encoding_type == "B":
                        decoded_text = base64.b64decode(encoded_text).decode(encoding)
                    else:
                        decoded_text = quopri.decodestring(
                            encoded_text.replace("_", " ")
                        ).decode(encoding)

                    self.decoded_parts.append(decoded_text)

                self.decoded_header = "".join(self.decoded_parts)
                return self.decoded_header
            except Exception as e:
                print("Occurred error has apeared" + str(e))
        else:
            return encoded_value

    def mailbox_printer(self, folderSelected):
        self.mailList = []
        self.imapSSL.select(folderSelected)
        _, searchReturn = self.imapSSL.search(None, "ALL")
        mailList = searchReturn[0].split()
        for mail in mailList:
            _, data = self.imapSSL.fetch(mail, "(RFC822)")
            self.email_message = message_from_bytes(data[0][1])
            try:
                self.mailList.append(self.email_message)
            except Exception as e:
                print("Error name:" + str(e))
                continue
        return self.mailList
