# SecureNote

SecureNote is a simple web application for securely creating and sharing notes. The notes are encrypted, and the generated links can be shared. Once opened, the note is deleted automatically.

## Features

- Securely create and share notes.
- Encryption using AES encryption.
- Automatic deletion of notes after 24 hours.
- A generated link to access the note.

## Requirements

- Python 3.x
- Virtualenv

## Setup Instructions

Follow the steps below to set up and run the project:

### 1. Clone the repository

```bash
git clone https://your-repository-url.git
cd your-project-directory
```

### 2. Create a Virtual Environment

Run the following command to create a virtual environment:

```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment

Activate the virtual environment using the following command:

- On macOS/Linux:

```bash
source venv/bin/activate
```

- On Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

Install all the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### 5. Running the Application

Once the dependencies are installed, you can start the Flask server by running the following:

```bash
python3 main.py
```

This will start the server at `http://127.0.0.1:5000/` by default.

### 6. Stopping the Application

To stop the Flask application, simply press `CTRL+C` in your terminal.

## Notes

- The project uses AES encryption to encrypt the notes before storing them.
- Notes are automatically deleted after 24 hours to ensure security.
- You can change the duration for file deletion by adjusting the `TWENTY_FOUR_HOURS` variable in the `main.py` file.

## Dependencies

The dependencies are listed in the `requirements.txt` file. To install them, run:

```bash
pip install -r requirements.txt
```
