#  Spam Detector API

This project is a REST API for a spam detection application, that identify spam numbers or allow users to find a person's name by searching for their phone number.

## Features

User registration and authentication
Contact management
Spam reporting
Name and phone number search with spam likelihood
Email visibility based on user relationships

## Technologies Used

Django 4.2.5
Django Rest Framework
django-phonenumber-field
Faker (for generating sample data)

##  Setup and Installation

### Installation

```bash
cd spam_detector
```

### Create a virtual environment and activate it:

```bash 
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
###  Install the required packages:

```bash
pip install -r requirements.txt
```

###  Apply the database migrations:

```bash
python manage.py migrate
```

###  Create a superuser:

```bash
python manage.py createsuperuser
```

###  (Optional) Populate the database with sample data:

```bash
python populate_db.py
```

###  Run the development server:

```bash
python manage.py runserver
```
##  API Endpoints

*/api/users/-->User management
*/api/contacts/--> Contact management
*/api/spam-reports/-->Spam reporting
*/api/search/-->Search functionality

##  Authentication

Most endpoints require authentication. Include the authentication token in the header of your requests:
You can obtain a token by sending a POST request to /api-token-auth/ with your username and password.