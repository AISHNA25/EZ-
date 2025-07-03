# Django Secure File Share Project

## 1. Writing Test Cases

To ensure the reliability and security of your Django Secure File Share application, you should write test cases for the following components:

### a. Models
- Test file upload and storage.
- Test user associations with uploaded files.

### b. Views
- Test authentication and permissions for file access.
- Test secure download link generation (validity, expiry, single-use).
- Test file download endpoint (valid/invalid/expired links).

### c. Forms
- Test file upload form validation.
- Test user registration and login forms.

### d. Templates
- Test that the dashboard displays files correctly for each user.
- Test that the download modal and AJAX work as expected.

### Example: Running Tests

1. Create your tests in `core/tests.py` (or in a `tests/` directory).
2. Run tests using:

```bash
python manage.py test
```

---

## 2. Deployment Plan for Production

### a. Prepare for Production
- Set `DEBUG = False` in `secure_share/settings.py`.
- Set `ALLOWED_HOSTS` to your domain or server IP.
- Use a strong, unique `SECRET_KEY`.
- Configure static and media file serving (e.g., with AWS S3, Azure Blob, or local server with Nginx).
- Use HTTPS (TLS/SSL) for all traffic.
- Set up proper database (e.g., PostgreSQL) instead of SQLite for production.

### b. Deployment Steps

1. **Choose a Hosting Platform**
   - Options: DigitalOcean, AWS EC2, Heroku, PythonAnywhere, Azure, etc.

2. **Install Dependencies**
   - Set up a Python virtual environment.
   - Install requirements:
     ```bash
     pip install -r requirements.txt
     ```

3. **Apply Migrations**
   ```bash
   python manage.py migrate
   ```

4. **Collect Static Files**
   ```bash
   python manage.py collectstatic
   ```

5. **Configure Web Server**
   - Use Gunicorn or uWSGI as the WSGI server.
   - Use Nginx or Apache as a reverse proxy.

6. **Set Up Environment Variables**
   - Store sensitive settings (SECRET_KEY, DB credentials) in environment variables.

7. **Start the Application**
   - Example with Gunicorn:
     ```bash
     gunicorn secure_share.wsgi:application --bind 0.0.0.0:8000
     ```

8. **Monitor and Secure**
   - Set up monitoring/logging.
   - Regularly update dependencies.
   - Enable firewalls and security groups.

---


