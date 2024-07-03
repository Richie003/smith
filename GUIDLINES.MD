# Hey Smith! Here's the guideline to run the software

## Installations

### Prerequisites

Please download and install

- Python 3.8 or versions above it.

### Steps

I have included a python installation file in the software folder so just right click on it and select run

## NB: Ensure you select the check box that say's Add python to path

1. **Create and Activate a Virtual Environment**

   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Linux/macOS use `source venv/bin/activate`
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

1. **Apply Migrations**

   ```bash
   python manage.py makemigrations
   ```

   and then

   ```bash
   python manage.py migrate
   ```

2. **Run the Local Server**

   ```bash
   python manage.py runserver
   ```

3. **Create a super admin to access the admin dashboard**

   - on your terminal enter `python manage.py createsuperuser` and follow the due process

4. **Access the Application**
   - Open your browser and navigate to `http://127.0.0.1:8000`.
