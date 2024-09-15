
# Simple TrueCaller Backend API

This project manages contacts system and provides API endpoints for user registration, login, and managing contact-related functionalities.

## Setup Instructions

### 1. Unzip the Project
Unzip the downloaded project files.

### 2. Install Dependencies
Install the required dependencies by running the following command:  
`pip install -r requirements.txt`

### 3. Set up the Database and Migrations
Run the following commands in the terminal to set up the database:

1. `python manage.py makemigrations`  
2. `python manage.py migrate`  
3. `python manage.py populate_db`   # This will populate the database with test data

**Note:** You can view the SQLite3 database using an online tool like [SQLite Viewer](https://sqliteviewer.app/#/).

## Test Environment

The test environment is now ready to use. Below are the available API endpoints and example payloads:

### API Endpoints and Payloads

#### 1. **User Registration**  
**Method**: POST  
**URL**: `http://127.0.0.1:8000/api/register/`  
**Payload**:
```json
{
  "name": "rakshitWalia",
  "username": {
    "username": "rakshitTest",
    "password": "000000"
  },
  "registeredUserNumber": "01031010",
  "userEmailId": "rakshit@instahyre.com"
}
```

#### 2. **User Login**  
**Method**: POST  
**URL**: `http://127.0.0.1:8000/api/login/`  
**Payload**:
```json
{
  "username": "user0",
  "password": "pass0"
}
```
After login, use the token from the response in the headers for subsequent authenticated requests:  
`{ "Authentication": "Bearer <token_key>" }`

#### 3. **Mark Contact as Spam**  
**Method**: GET  
**URL**: `http://127.0.0.1:8000/api/mark_contact_spam/`  
**Payload**:
```json
{
  "contact_number": "1000000002"
}
```

#### 4. **Search by Name**  
**Method**: GET  
**URL**: `http://127.0.0.1:8000/api/search_by_name/`  
**Payload**:
```json
{
  "name": "name"
}
```
*(The value can be any name, e.g., `name0`, `nam`, etc.)*

#### 5. **Search by Phone Number**  
**Method**: GET  
**URL**: `http://127.0.0.1:8000/api/search_by_phone/`  
**Payload**:
```json
{
  "phone_number": "1000000003"
}
```

#### 6. **Mark Contact as Spam (Authenticated User Only)**  
**Method**: POST  
**URL**: `http://127.0.0.1:8000/api/mark_contact_spam/`  
**Payload**:
```json
{
  "phone_number": "1000000003"
}
```
*(This action can only be performed by a registered user with the correct authentication header.)*

#### 7. **User Logout**  
**Method**: POST  
**URL**: `http://127.0.0.1:8000/api/logout/`  
**Payload**:
```json
{}
```
*(Include the authentication header from the login step.)*

---

## License
This project is licensed under the [MIT License](LICENSE).
