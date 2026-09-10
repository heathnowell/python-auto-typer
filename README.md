# Python Password Manager

A command-line password manager written in Python that stores account passwords in an encrypted local file.

The project uses **Fernet symmetric encryption** to encrypt and decrypt stored passwords and **bcrypt** to verify the master password.

## Features

- Add and store account credentials
- Encrypt passwords before saving them locally
- View and decrypt saved passwords after authentication
- Remove individual saved credentials
- Delete the local password file
- Protect access with a master password
- Validate the user-provided Fernet encryption key

## Technologies

- Python
- `cryptography` / Fernet
- `bcrypt`
- JSON
- Python `os` module

## Project Structure

```text
python-password-manager/
├── password_manager.py
├── README.md
├── requirements.txt
└── .gitignore
```

The program creates a local `passwords.json` file when credentials are saved.

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/python-password-manager.git
cd python-password-manager
```

Install the required packages:

```bash
pip install cryptography bcrypt
```

Or, if the repository includes a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Usage

Run the program:

```bash
python password_manager.py
```

The application will:

1. Ask for the master password.
2. Ask for a valid Fernet encryption key.
3. Allow you to add, view, remove, or delete stored credentials.
4. Save encrypted passwords to `passwords.json` when the program exits normally.

Available commands:

```text
view
add
remove
remove file
q
```

## How It Works

### Master Password Authentication

The entered master password is checked against a stored **bcrypt hash**:

```python
bcrypt.checkpw(entered_password, master_password_hash)
```

### Password Encryption

Passwords are encrypted before being stored:

```python
encrypted_password = fer.encrypt(password.encode())
```

They are decrypted only when the user chooses to view them:

```python
decrypted_password = fer.decrypt(encrypted_password).decode()
```

### Local Storage

Encrypted credentials are serialized into JSON and written to:

```text
passwords.json
```

## Security Notes

This project was built as a learning project and has **not been security-audited for production use**.

Before publishing or distributing the project:

- Do not upload your real `passwords.json` file.
- Do not publish a bcrypt hash tied to a master password that you use elsewhere.
- Consider changing the program so each user creates a master password during initial setup.
- Consider generating and securely storing or deriving the encryption key instead of requiring the user to manually paste it each time.

Recommended `.gitignore` entries:

```gitignore
passwords.json
__pycache__/
*.pyc
.venv/
venv/
```

## What I Learned

This project helped me practice:

- Symmetric encryption
- Password hashing and authentication
- Local data storage with JSON
- File handling
- Error handling
- Building a menu-driven Python application
- Applying cybersecurity concepts in a practical project

## Future Improvements

Possible future improvements include:

- First-run master password setup
- Secure key derivation from a master password
- Automatic encryption-key management
- Hidden password input using `getpass`
- Search and edit functionality
- Graphical user interface
- Stronger validation and error handling

## Disclaimer

This project is intended for educational and personal learning purposes. It should not be treated as a production-grade password manager without additional security review and development.
