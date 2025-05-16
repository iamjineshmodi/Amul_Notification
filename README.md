# Amul_Notification
## Features

- Checks Amul's online store for protein products (lassi, paneer, whey)
- Notifies you via SMS (using Twilio) when at least two products are available

## Requirements

- Python 3.7+
- [requests](https://pypi.org/project/requests/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- Twilio account and credentials

## Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/Amul_Notification.git
    cd Amul_Notification
    ```

3. **Configure environment variables:**

    Create a `.env` file in the project root with:
    ```
    TWILIO_ACCOUNT_SID=your_account_sid
    TWILIO_AUTH_TOKEN=your_auth_token
    TWILIO_PHONE_NUMBER=your_twilio_number
    RECIPIENT_PHONE_NUMBER=your_mobile_number
    ```

4. **Run the script:**
    ```bash
    python amul_notify.py
    ```

## How it works

- The script fetches product data from Amul's API.
- It checks if at least two of the following are available: protein lassi, paneer, or whey.
- If available, it sends an SMS notification to your phone using Twilio.
