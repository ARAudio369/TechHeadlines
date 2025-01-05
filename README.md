**Email Tech Headlines Script**

This Python script fetches the latest tech headlines from popular websites and sends them via email. It is designed to help you stay updated on the latest tech news with minimal effort.

Features:

Fetches headlines from:
- TechCrunch
- Ars Technica
- TechRadar

Randomly selects a set number of articles to include in the email.
Sends the compiled headlines via email in a neat HTML format.

Prerequisites:
- Python 3.6 or higher

Required libraries:
- requests
- beautifulsoup4
- smtplib
- Installation

Clone or download the repository.

Install the required dependencies:
- pip install -r requirements.txt

Configuration
Replace the placeholder values in the script with your own:

- Email credentials: from_email and password

- Recipient email: recipient_email

Alternatively, use environment variables for better security.

Usage

Run the script with:

- python script_name.py

Note

Ensure you use an app-specific password if you're using Gmail.
The User-Agent header in the script may need to be updated based on website requirements.
