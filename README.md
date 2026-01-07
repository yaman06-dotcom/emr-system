'''
# AI-Powered Electronic Medical Record (EMR) System

This project is a university-level full-stack web application for managing electronic medical records, featuring an AI component for health risk prediction.

## Core Features

*   **User Authentication:** Role-based access for Doctors and Admins.
*   **Patient Management:** Full CRUD (Create, Read, Update, Delete) functionality for patient records.
*   **Medical History:** Track patient visits, diagnoses, symptoms, and prescriptions.
*   **Prescription Management:** Basic alerts for drug allergies and potential conflicts.
*   **AI-Powered Risk Prediction:** A machine learning model to predict patient health risks (e.g., diabetes).
*   **Dashboard:** Visual overview of patient statistics and recent activities.

## Technical Stack

*   **Backend:** Django (Python)
*   **Database:** PostgreSQL
*   **AI/ML:** Scikit-learn
*   **Frontend:** Django Templates with Bootstrap 5

## Project Structure

```
/emr_system
|-- /accounts         # User authentication and roles
|-- /ai_prediction    # Health risk prediction model and views
|-- /emr_project      # Main Django project settings and URLs
|-- /medical          # Medical visits and prescriptions
|-- /patients         # Patient data management
|-- /templates        # HTML templates
|-- manage.py         # Django management script
|-- README.md         # This file
```

## Setup and Installation

### Prerequisites

*   Python 3.11+
*   PostgreSQL

### 1. Clone the Repository

```bash
git clone <repository_url>
cd emr_system
```

### 2. Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

*Note: A `requirements.txt` file will be generated in a later step.*

### 4. Configure PostgreSQL Database

1.  Start your PostgreSQL server.
2.  Create a database and a user for the project:

    ```sql
    CREATE DATABASE emr_db;
    CREATE USER emr_user WITH PASSWORD 'emr_password123';
    ALTER ROLE emr_user SET client_encoding TO 'utf8';
    ALTER ROLE emr_user SET default_transaction_isolation TO 'read committed';
    ALTER ROLE emr_user SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE emr_db TO emr_user;
    ```

3.  The Django settings (`emr_project/settings.py`) are already configured to use these credentials.

### 5. Apply Database Migrations

```bash
python manage.py migrate
```

### 6. Create a Superuser (Admin)

This will be your first admin account to manage the system.

```bash
python manage.py createsuperuser
```

Follow the prompts to set a username, email, and password.

### 7. Train the AI Model

The first time you run the application, the AI model for risk prediction needs to be trained. You can do this from the admin interface or by running a command.

Log in to the admin panel, navigate to the "AI Prediction" section, and trigger the training process. Alternatively, you can run:

```bash
# This command will be implemented later
python manage.py train_ai_model
```

### 8. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`.

## Usage

1.  **Login:** Access the application and log in with your superuser credentials.
2.  **Create Users:** As an admin, you can create new user accounts for doctors from the "Add User" link in the sidebar.
3.  **Manage Patients:** Navigate to the "Patients" section to add, view, update, or delete patient records.
4.  **Record Visits:** From a patient's detail page, you can create a new medical visit, record diagnoses, and prescribe medications.
5.  **Predict Risk:** Use the "Predict Risk" feature on the patient detail page to get an AI-based health risk assessment.
'''
