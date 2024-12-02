# Fetch Backend Internship Project Instructions

This is a Python-based application built with Flask for handling API requests and SQLite3 for the database.

## Prerequisites

- Python 3.x installed
- `pip3` installed
- SQLite3 installed (installation steps below)

## Installation Steps

### Step 1: Install Flask
Run the following command to install Flask:
```bash
pip3 install Flask
```

### Step 2: Install SQLite3
This project uses SQLite3 for its database:
Check if SQLite3 is pre-installed
  ```bash
  sqlite3 --version
  ```

- **macOS/Linux**: 
  If not installed:
  ```bash
  sudo apt install sqlite3  # For Linux
  brew install sqlite3      # For macOS
  ```

- **Windows**: 
  Download from https://www.sqlite.org/download.html.

## Running the Application

### Step 1: Initialize the Database
Run the following command to create the SQLite database called points.db:
```bash
python3 database.py
```

### Step 2: Start the Application (Flask)
Run the following command:
```bash
python3 app.py
```

### Step 3: Accessing the Application
POST requests can be accessed using curl or Postman, while GET requests can be accessed using curl or Postman and also just a browser window.

### Note
Please contact me should you have any issues running the application. Thank you!

