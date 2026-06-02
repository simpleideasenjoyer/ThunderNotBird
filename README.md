# ThunderNotBird

ThunderNotBird is a desktop email client written in Python with a PyQt5 graphical interface.
The project provides a simple GUI for logging into a mailbox, browsing messages, reading message content, and composing emails.

## Status

This project is a hobby / learning project and should be treated as work in progress.

## Features

- login screen for mailbox access
- inbox-style message list
- message content preview
- create and send messages
- attachment support
- PyQt5 desktop GUI

## Technologies

- Python
- PyQt5
- IMAP
- SMTP

## Project structure

- `main.py` – application entry point
- `GUI/` – graphical interface widgets and generated UI files
- `utils/` – application email logic

## Requirements

- Python 3.10+
- PyQt5
- PyQtWebEngine

## Installation

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running

```bash
python main.py
```

## Security note

This application works with mailbox credentials entered by the user in the GUI.
No credentials are intended to be stored in the repository.
Before public release, review the code and configuration again to ensure no sensitive data was committed.

Depending on your email provider configuration, standard password login may not work without additional settings such as an app password.

## License

This project is licensed under the GNU GPL v3. See the `LICENSE` file for details.
