# Google OAuth Authentication with OTP Verification

This is a module to test and verify Google authentication for web applications, ensuring that only Gmail-confirmed accounts are able to authenticate and access services. This way, any random email addresses won't be verified without proper Gmail confirmation.

## How does it work?
1. Created an API service in the Google Developer Console.
2. Implemented the API routes provided by Google in Flask.
3. Set up SMTP mailing configuration in Gmail to verify users via OTP.

## How to use this module locally?

### Prerequisites
- Python 3.x
- A Gmail account (for sending OTP emails via Gmail's SMTP server)
- MongoDB installed locally or on a cloud provider like MongoDB Atlas
- A Google Developer Console project to generate OAuth 2.0 credentials

### Steps

#### 1. Clone the repository

Clone the project to your local machine:

```bash
git clone https://github.com/your-repo/google-oauth-otp.git
```

#### 2. Set up the Python environment

Create a virtual environment and activate it:

```bash
python -m venv venv
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

#### 3. Set up Google OAuth credentials

generate client tokens ids, and keys frm the services apis, frm google console

#### 4. Set up the `.env` file
```ini
SECRET_KEY,
GOOGLE_CLIENT_ID,
GOOGLE_CLIENT_SECRET,
MAIL_USERNAME,
MAIL_PASSWORD,
MONGO_URI,
```

#### 5. run the application now.
``python app.py``
### User Flow

1. **Login Prompt**: Upon accessing the application, the user is prompted to log in via Google.
2. **Google Authentication**: The user is presented with a Google login screen, where they select the Gmail account they wish to authenticate with.
3. **OTP Verification**: After the user selects their Google account, an OTP is sent to their Gmail address.
4. **OTP Entry**: The user enters the OTP in the web application to complete the verification.
5. **Successful Registration**: If the OTP is correct, the user’s information is stored in the MongoDB database, and they are successfully authenticated.
6. **Subsequent Logins**: Users won’t need to go through the OTP process again once they are registered.

### How It Works Internally

- **Google OAuth Flow**: The app initiates the OAuth 2.0 flow, which redirects the user to Google's login page. After successful login, the user's Google account is authenticated.
- **OTP Generation and Sending**: After login, the app generates a unique OTP and sends it to the email address via Gmail’s SMTP service.
- **Database Registration**: After the user verifies the OTP, their details (such as email and name) are saved in the MongoDB database to track their authentication status.
