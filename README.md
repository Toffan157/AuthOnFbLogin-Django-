📌 Django Facebook OAuth Integration with Pages API

This project demonstrates how to integrate Facebook Login (OAuth2) with a Django application, fetch user profile details, and retrieve all Facebook Pages the user manages, along with their access tokens and granted permissions.

🚀 Features

🔑 Facebook Login using OAuth2 (without django-allauth).

👤 Fetch user profile details (ID, Name, Email).

📄 Fetch all Facebook pages managed by the user.

🔒 Store page details (page name, page ID, page access token, permissions) in PostgreSQL.

🔐 Generate Django REST Framework Auth Tokens for API authentication.

🌐 API Endpoints for login, profile, and pages.

🎨 Basic Bootstrap UI for login and home page.

🛠️ Tech Stack

Backend: Django, Django REST Framework

Database: PostgreSQL

Authentication: Facebook OAuth 2.0

Frontend: Bootstrap (HTML Templates)

API Client: Postman / cURL

⚙️ Setup Instructions
1️⃣ Clone the Repository
git clone https://github.com/Toffan157/AuthOnFbLogin-Django-.git
cd AuthOnFbLogin-Django

2️⃣ Create Virtual Environment & Install Dependencies
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

pip install -r requirements.txt

3️⃣ Configure PostgreSQL

Create a database in PostgreSQL:

CREATE DATABASE fb_auth_db;


Update settings.py with your DB credentials:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fb_auth_db',
        'USER': 'postgres',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

4️⃣ Set up Facebook App

Go to Facebook Developer Console.

Create an App → Add Facebook Login product.

Set Valid OAuth Redirect URI → http://localhost:8000/api/facebook/callback/

Copy App ID and App Secret into .env:

FACEBOOK_CLIENT_ID=your_app_id
FACEBOOK_CLIENT_SECRET=your_app_secret
FACEBOOK_REDIRECT_URI=http://localhost:8000/api/facebook/callback/
FACEBOOK_API_VER=v23.0

5️⃣ Apply Migrations & Run Server
python manage.py migrate
python manage.py runserver

📡 API Endpoints
🔹 Facebook Login Redirect
GET /api/facebook/login/

🔹 Facebook Callback (after login)
GET /api/facebook/callback/?code=xxxx


Returns user token, profile, and pages info.

🔹 User Profile
GET /api/profile/
Authorization: Token <your_auth_token>

🔹 User Pages
GET /api/pages/
Authorization: Token <your_auth_token>

🗄️ Database (PostgreSQL Table)

Table: facebookpage

id (PK)

user_id (FK → auth_user)

page_id

page_name

page_access_token

granted_permissions (JSON)

created_at, updated_at

🎨 UI Screens

login.html → Login with Facebook button

home.html → Displays user info + API token

📌 Future Improvements

✅ Refresh expired access tokens

✅ Add support for Page Insights API

✅ Store user profile picture
