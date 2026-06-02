"""Email provider presets for IMAP and SMTP configuration."""

PROVIDERS = {
    "Gmail": {
        "imap_server": "imap.gmail.com",
        "imap_port": 993,
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 465,
        "smtp_ssl": True,
    },
    "Outlook / Hotmail": {
        "imap_server": "outlook.office365.com",
        "imap_port": 993,
        "smtp_server": "smtp.office365.com",
        "smtp_port": 587,
        "smtp_ssl": False,
    },
    "Yahoo Mail": {
        "imap_server": "imap.mail.yahoo.com",
        "imap_port": 993,
        "smtp_server": "smtp.mail.yahoo.com",
        "smtp_port": 465,
        "smtp_ssl": True,
    },
    "Custom": {
        "imap_server": "",
        "imap_port": 993,
        "smtp_server": "",
        "smtp_port": 465,
        "smtp_ssl": True,
    },
}
